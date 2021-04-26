from lib.lftp import FTPBackupForDB

if __name__ == '__main__':
    f = FTPBackupForDB(db='mongo')
    f.connect()
    print(f.ls_dir(path='dev'))
