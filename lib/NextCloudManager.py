# -*- coding: utf-8 -*-
from nextcloud import NextCloud
from lib.Log import RecodeLog
from lib.settings import NEXTCLOUD_URL, NEXTCLOUD_PASSWORD, NEXTCLOUD_USERNAME
import sys


class NextCloudManager:
    def __init__(self):
        try:
            self.nxc = NextCloud(
                endpoint=NEXTCLOUD_URL,
                user=NEXTCLOUD_USERNAME,
                password=NEXTCLOUD_PASSWORD,
                json_output=True
            )
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
        try:
            data = self.nxc.upload_file(NEXTCLOUD_USERNAME, local_achieve, remote_achieve)
            RecodeLog.info(msg="上传到nextcloud成功！本地文件:{},远程文件:{},地址:{},用户:{}！".format(
                local_achieve, remote_achieve, NEXTCLOUD_URL, NEXTCLOUD_USERNAME
            ))
            if not data.is_ok:
                raise Exception(data.data)
        except Exception as error:
            RecodeLog.error(msg="上传到nextcloud失败，本地文件:{},远程文件:{},地址:{},用户:{},原因:{}".format(
                local_achieve, remote_achieve, NEXTCLOUD_URL, NEXTCLOUD_USERNAME, error
            ))
            sys.exit(1)

    def get_user(self):
        print(self.nxc.getapppassword())


__all__ = [
    'NextCloudManager'
]
