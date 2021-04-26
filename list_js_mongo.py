from lib.lftp import FTPBackupForDB

if __name__ == '__main__':
    f = FTPBackupForDB(db='mongo')
    print(f.ls_dir(path='dev'))
