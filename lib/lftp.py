# -*- coding: utf-8 -*-
from lib.settings import *
from ftplib import FTP
from lib.Log import RecodeLog
import sys
import os


class FTPBackupForDB:
    def __init__(self, db="mysql"):
        self.host = FTP_CONFIG[db.lower()]['host']
        self.port = FTP_CONFIG[db.lower()]['port']
        self.user = FTP_CONFIG[db.lower()]['user']
        self.passwd = FTP_CONFIG[db.lower()]['password']
        self.ftp = FTP()

    def connect(self):
        try:
            self.ftp.connect(self.host, self.port)
            self.ftp.login(self.user, self.passwd)
        except Exception as error:
            RecodeLog.error(msg="登录FTP失败：{0}".format(error))
            sys.exit(1)

    def ls_dir(self, path):
        """
        :param path:
        :return:
        """
        self.ftp.cwd(dirname=path)
        return self.ftp.nlst()

    def download(self, remote_path, local_path, achieve):
        """
        :param remote_path:
        :param local_path:
        :param achieve:
        :return:
        """
        bufsize = 1024
        local_file = os.path.exists(os.path.join(local_path, achieve))
        achieve_list = self.ls_dir(path=remote_path)
        try:
            if not os.path.exists(local_path):
                raise Exception("本地目录不存在")
            if achieve not in achieve_list:
                raise Exception("远端不存在该文件")
            fp = open(local_file, 'wb')
            self.ftp.retrbinary('RETR ' + remote_path, fp.write, bufsize)
            self.ftp.set_debuglevel(0)  # 参数为0，关闭调试模式
            fp.close()
            return True
        except Exception as error:
            RecodeLog.error(msg="上传文件失败，{}，原因：{}".format(local_file, error))
            return False

    def run(self, remote, achieve):
        """
        :param remote:
        :param achieve:
        :return:
        """
        if not self.download(local_path=BACKUP_DIR, remote_path=remote, achieve=achieve):
            sys.exit(1)
        else:
            sys.exit(0)

    def rm_remote(self, remote, achieve):
        """
        :param remote:
        :param achieve:
        :return:
        """
        achieve_list = self.ls_dir(path=remote)
        remote_achieve = os.path.join(remote, achieve)
        try:
            if achieve not in achieve_list:
                raise Exception("远端不存在该文件")
            self.ftp.rmd(remote_achieve)
            RecodeLog.info(msg="删除远端文件成功，{}!".format(remote_achieve))
            return True
        except Exception as error:
            RecodeLog.error(msg="删除远端文件失败，{}，原因：{}".format(remote_achieve, error))
            return False