from lib.lftp import FTPBackupForDB

f = FTPBackupForDB(db='mongo')
f.ls_dir(path='dev')
