# -*- coding: utf-8 -*-
from nextcloud import NextCloud
from lib.Log import RecodeLog
from lib.settings import *
import sys
import requests
import re


class NextCloudManager:
    def __init__(self):
        self.nxc = None

    def connect(self):
        token = self.get_password()
        try:
            self.nxc = NextCloud(
                endpoint=NEXTCLOUD_URL,
                user=NEXTCLOUD_ID,
                password=token,
                json_output=True
            )
            RecodeLog.info(msg="初始化nextcloud Success，地址:{},用户:{},TOKEN:{}".format(
                NEXTCLOUD_URL, NEXTCLOUD_USERNAME, token
            ))
        except Exception as error:
            RecodeLog.error(msg="初始化nextcloud失败，地址:{},用户:{},原因:{}".format(
                NEXTCLOUD_URL, NEXTCLOUD_USERNAME, error
            ))
            sys.exit(1)

    def upload(self, local_achieve, remote_achieve):
        """
        :param local_achieve:
        :param remote_achieve:
        :return:
        """
        self.connect()
        try:
            data = self.nxc.upload_file(NEXTCLOUD_USERNAME, local_achieve, remote_achieve)
            RecodeLog.info(msg="上传到nextcloud成功！本地文件:{},远程文件:{},地址:{},用户:{}！".format(
                local_achieve, remote_achieve, NEXTCLOUD_URL, NEXTCLOUD_ID
            ))
            if not data.is_ok:
                raise Exception(data.data)
        except Exception as error:
            RecodeLog.error(msg="上传到nextcloud失败，本地文件:{},远程文件:{},地址:{},用户:{},原因:{}".format(
                local_achieve, remote_achieve, NEXTCLOUD_URL, NEXTCLOUD_ID, error
            ))
            sys.exit(1)

    def get_password(self):
        headers = dict()
        headers['OCS-APIRequest'] = 'true'
        try:
            res = requests.get(
                url="{0}/ocs/v2.php/core/getapppassword".format(NEXTCLOUD_URL),
                auth=(NEXTCLOUD_USERNAME, NEXTCLOUD_PASSWORD),
                headers=headers
            )
            if res.status_code != 200:
                raise Exception(res.content)
            return re.findall(".*<apppassword>(.*)</apppassword>.*", res.content)[0]
        except Exception as error:
            RecodeLog.error("get passord faild :{}".format(error))
            assert False


__all__ = [
    'NextCloudManager'
]
