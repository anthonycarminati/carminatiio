import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    POSTGRES_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class ProductionConfig(Config):
    POSTGRES_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}