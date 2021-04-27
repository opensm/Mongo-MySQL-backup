# -*- coding: utf-8 -*-
import pymongo
import os
import datetime
from lib.settings import *
from lib.Log import RecodeLog
import sys
from lib.lftp import FTPBackupForDB
from lib.NextCloudManager import NextCloudManager
import copy
import platform
import time


class MongodbExec:
    def __init__(self, env="pre"):
        config = copy.deepcopy(MONGODB_CONFIG[env.lower()])
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.password = config['password']
        self.auth_dump_str = "--host {} --port {} -u {} -p {}  --authenticationDatabase admin ".format(
            self.host, self.port,
            self.user, self.password
        )
        if not os.path.exists(BACKUP_DIR):
            raise Exception(
                "{0} 不存在！".format(BACKUP_DIR)
            )
        if not os.path.exists("/usr/bin/mongodump") or not os.path.exists("/usr/bin/mongorestore"):
            raise Exception("mongo或者mongodump, mongorestore没找到可执行程序！")

        try:
            self.conn = pymongo.MongoClient(host=self.host, port=self.port, username=self.user, password=self.password)
        except Exception as error:
            RecodeLog.error(msg="链接Mongo,host:{},port:{}失败，原因:{}".format(config['host'], config['port'], error))
            sys.exit(1)

        if int(platform.python_version().strip(".")[0]) < 3:
            import commands

            self.exec_proc = commands
        else:
            import subprocess

            self.exec_proc = subprocess

    def cmd(self, cmd_str):
        """
        :param cmd_str:
        :return:
        """
        try:
            status, output = self.exec_proc.getstatusoutput(cmd_str)
            if status != 0:
                raise Exception(output)
            RecodeLog.info("执行:{0},成功!".format(cmd_str))
            return True
        except Exception as error:
            RecodeLog.error(msg="执行:{0},失败，原因:{1}".format(cmd_str, error))
            sys.exit(1)

    def check_db(self, db):
        res = self.conn.list_database_names()
        if db in res:
            return True
        else:
            RecodeLog.error(msg="数据库：{0},不存在！")
            return False

    def backup_all(self):
        cmd_str = "/usr/bin/mongodump {0} --gzip --archive={1}".format(
            self.auth_dump_str,
            os.path.join(
                BACKUP_DIR,
                "mongo-{0}-{1}-{2}-all-database.gz".format(
                    self.host, self.port, datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                )
            )

        )
        self.cmd(cmd_str=cmd_str)

    def backup_one(self, db, achieve):
        if not self.check_db(db=db):
            sys.exit(1)
        cmd_str = "/usr/bin/mongodump {0}  --gzip --archive={2}".format(
            self.auth_dump_str,
            db,
            os.path.join(
                BACKUP_DIR,
                "{}.gz".format(achieve)
            )
        )
        self.cmd(cmd_str=cmd_str)

    def exec_sql(self, db, sql):
        """
        :param db:
        :param sql:
        :return:
        """
        if not os.path.exists(
                os.path.join(BACKUP_DIR, sql)
        ):
            raise Exception("文件不存在：{0}".format(os.path.join(BACKUP_DIR, sql)))
        filename, filetype = os.path.splitext(sql)
        if filetype == ".js":
            cmd_str = "/usr/bin/mongo {0} {1}  {2}".format(
                self.auth_dump_str,
                db,
                os.path.join(BACKUP_DIR, sql)
            )
        elif filetype == ".gz":
            cmd_str = "zcat {2}|/usr/bin/mongorestore {0} {1} --archive".format(
                self.auth_dump_str,
                db,
                os.path.join(BACKUP_DIR, sql)
            )
        else:
            RecodeLog.error(msg="不能识别的文件类型:{}".format(sql))
            sys.exit(1)
        if not self.cmd(cmd_str=cmd_str):
            RecodeLog.error(msg="导入数据失败:{}".format(cmd_str))
            sys.exit(1)
        else:
            RecodeLog.info(msg="导入数据成功:{}".format(cmd_str))

    def run(self, sql, env):
        """
        :param sql:
        :param env:
        :return:
        """
        f = FTPBackupForDB(db='mongo')
        # n = NextCloudManager()
        filename, filetype = os.path.splitext(sql)
        f.connect()
        f.download(remote_path=env, local_path=BACKUP_DIR, achieve=sql)
        sql_data = filename.split("#")
        if sql_data[1] != 'mongodb' or sql_data[2] != env:
            RecodeLog.error(msg="请检查即将导入的文件的相关信息，{}".format(sql))
            sys.exit(1)
        if len(sql_data) != 4:
            RecodeLog.error(msg="文件格式错误，请按照：20210426111742#mongodb#pre#member.js")
            sys.exit(1)
        self.backup_one(
            db=sql_data[3],
            achieve=filename
        )
        self.exec_sql(sql=sql, db=sql_data[3])
        # print(os.path.join("/BU4-09项目文档-北汽越野2/06-运维/06-03-发版归档", "{}".format(sql)))
        # print(os.path.join("/BU4-09项目文档-北汽越野2/06-运维/06-03-发版归档", "{}.gz".format(filename)))
        # # n.upload(
        #     local_achieve=os.path.join(BACKUP_DIR, sql),
        #     remote_achieve=os.path.join("BU4-09项目文档-北汽越野2/06-运维/06-03-发版归档", sql)
        # )
        # time.sleep(10)
        # n.upload(
        #     local_achieve=os.path.join(BACKUP_DIR, "{}.gz".format(filename)),
        #     remote_achieve=os.path.join("BU4-09项目文档-北汽越野2/06-运维/06-03-发版归档", "{}.gz".format(filename))
        # )
        f.rm_remote(remote=env, achieve=sql)


__all__ = [
    'MongodbExec'
]
