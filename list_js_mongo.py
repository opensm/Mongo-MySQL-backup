from lib.lftp import FTPBackupForDB
import sys,json

if __name__ == '__main__':
    f = FTPBackupForDB(db='mongo')
    f.connect()
    data = f.show_list(path='dev')
    print(json.dumps({"list": data}))
