class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = 'database/job.db'
    JOBS = 'database/jobs.json'
    SECRET_KEY = 'key'


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    DB_HOST = 'database/production/job.db'
