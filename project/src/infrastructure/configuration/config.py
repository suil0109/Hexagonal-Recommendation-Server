################################
# Configs for Redis & Mysql    #
################################

CONFIG = {
    "MAX_RECS": 3,
    "URL": "https://predict-ctr-pmj4td4sjq-du.a.run.app/",
    "REDIS_HOST": "hostname-redis",
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    "MYSQL_USERNAME": 'root',
    "MYSQL_PASSWORD": 'root',
    "MYSQL_HOSTNAME": 'hostname-mysql',
    "MYSQL_DATABASE": 'google_recs'
}

class GlobalConfig:
    def __init__(self):
        self.MAX_RECS = CONFIG["MAX_RECS"]
        self.REDIS_HOST = CONFIG["REDIS_HOST"]
        self.REDIS_PORT = CONFIG["REDIS_PORT"]
        self.REDIS_DB = CONFIG["REDIS_DB"]
        self.MYSQL_USERNAME = CONFIG["MYSQL_USERNAME"]
        self.MYSQL_PASSWORD = CONFIG["MYSQL_PASSWORD"]
        self.MYSQL_HOSTNAME = CONFIG["MYSQL_HOSTNAME"]
        self.MYSQL_DATABASE = CONFIG["MYSQL_DATABASE"]

global_config = GlobalConfig()