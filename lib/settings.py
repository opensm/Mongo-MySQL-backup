BACKUP_DIR = '/data/db_backup'
LOG_DIR = "/tmp"
LOG_FILE = "db_back.log"
LOG_LEVEL = "INFO"
FTP_CONFIG = {
    "mongodb": {
        "host": "",
        "port": 2121,
        "user": "",
        "password": ""
    },
    "mysqldb": {
        "host": "",
        "port": 2121,
        "user": "",
        "password": ""
    }
}
MYSQL_CONFIG = {
    "pre": {
    },
    "prod": {
    },
    "dev": {
    }
}
MONGODB_CONFIG = {
    "pre": {

    },
    "prod": {
    },
    "dev": {

    }
}
NEXTCLOUD_URL = ""
NEXTCLOUD_USERNAME = ""
NEXTCLOUD_PASSWORD = ""
__all__ = [
    'BACKUP_DIR',
    'MONGODB_CONFIG',
    'MYSQL_CONFIG',
    'FTP_CONFIG',
    'LOG_FILE',
    'NEXTCLOUD_USERNAME',
    'NEXTCLOUD_PASSWORD',
    'NEXTCLOUD_URL'
]
