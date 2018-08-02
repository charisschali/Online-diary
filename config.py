import os

class Config(object):
    """
    Common configurations
    """
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    SECRET_KEY = os.getenv('SECRET_KEY ')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    host = os.getenv('DB_HOST')
    database_name = os.getenv('DB_NAME')
    user = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    database_name = os.getenv('DB_NAME')

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

class TestingConfig(Config):
    """
    Testing configurations
    """
    DEBUG = True
    TESTING = True
    database_name = os.getenv('TEST_DB')

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing':TestingConfig
}
