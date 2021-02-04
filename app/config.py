import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTE_URL = os.getenv('POSTE_URL')
    POSTE_TOKEN = os.getenv('POSTE_TOKEN')
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')


class DevelopmentConfig(Config):
    ENV_TYPE = "development"


class ProductionConfig(Config):
    ENV_TYPE = "production"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
