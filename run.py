# -*- coding: utf-8 -*-
import getopt
import sys
from lib.mongodbexec import MongodbExec
from lib.mysqlexec import MySQLExec


def useage():
    print("%s -f\t#执行文件" % sys.argv[0])
    print("%s -e\t#执行环境" % sys.argv[0])
    print("%s -h\t#帮助文档" % sys.argv[0])


def main():
    if len(sys.argv) == 1:
        useage()
        sys.exit()
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "e:f:h"
        )
    except getopt.GetoptError:
        print("%s -h" % sys.argv[0])
        sys.exit(1)
    command_dict = dict(options)
    command_data = dict()
    # 帮助
    if '-h' in command_dict:
        useage()
        sys.exit()
    # 获取监控项数据
    elif "-f" in command_dict and '-e' in command_dict:
        command_data['achieve'] = command_dict.get('-f')
        command_data['env'] = command_dict.get('-e')
        sql_data = command_data['achieve'].split("#")
        if sql_data[1] == 'mysql':
            ff = MySQLExec()
            ff.run(sql=command_data['achieve'], env=command_data['env'])
        elif sql_data[1] == 'mongodb':
            ff = MongodbExec()
            ff.run(sql=command_data['achieve'], env=command_data['env'])
        else:
            print("error input db file")
            sys.exit(1)
    else:
        useage()
        sys.exit(1)


if __name__ == '__main__':
    main()
