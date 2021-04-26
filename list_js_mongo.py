from lib.lftp import FTPBackupForDB

if __name__ == 'main':
    f = FTPBackupForDB(db='mongo')
    print(f.ls_dir(path='dev'))
