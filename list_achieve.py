from lib.lftp import FTPBackupForDB
import getopt
import sys


def useage():
    print("%s -t\t#帮助文档" % sys.argv[0])
    print("%s -e\t#读取文件" % sys.argv[0])
    print("%s -h\t#是强制升级" % sys.argv[0])


def main():
    if len(sys.argv) == 1:
        useage()
        sys.exit()
    try:
        options, args = getopt.getopt(
            sys.argv[1:],
            "e:t:h"
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
    elif "-e" in command_dict and '-t' in command_dict:
        command_data['db_type'] = command_dict.get('-t')
        command_data['env'] = command_dict.get('-e')
        ff = FTPBackupForDB(db=command_data['db_type'])
        ff.connect()
        ff.show_list(path=command_data['env'])
        sys.exit(0)
    else:
        useage()
        sys.exit(1)


if __name__ == '__main__':
    main()
