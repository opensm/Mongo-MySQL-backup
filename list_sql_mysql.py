from lib.mongodbexec import FTPBackupForDB

f = FTPBackupForDB(db='mysql')
f.ls_dir(path='dev')
