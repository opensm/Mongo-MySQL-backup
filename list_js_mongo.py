from lib.mongodbexec import FTPBackupForDB

f = FTPBackupForDB(db='mongo')
f.ls_dir(path='dev')
