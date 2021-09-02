from glob import glob
import os
from lib.CosUpdate import CosUpload
from lib.settings import BACKUP_DIR

c = CosUpload()

for data in glob(os.path.join(BACKUP_DIR, '*.gz')):
    c.upload(data)
for data in glob(os.path.join(BACKUP_DIR, '*.sql')):
    c.upload(data)
for data in glob(os.path.join(BACKUP_DIR, '*.js')):
    c.upload(data)
