from lib.lftp import FTPBackupForDB

if __name__ == '__main__':
    f = FTPBackupForDB(db='mysql')
    print(f.ls_dir(path='dev'))
