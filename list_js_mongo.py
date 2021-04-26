from lib.lftp import FTPBackupForDB

if __name__ == '__main__':
    f = FTPBackupForDB(db='mongo')
    f.connect()
    data = f.ls_dir(path='dev')
    print(111111111111111111111111111)
    print(data)
    print(111111111111111111111111111)
