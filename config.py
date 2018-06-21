"""
[
    Config file
]
"""

import os


class Config(object):
    """[summary]
    
    Arguments:
        object {[type]} -- [description]
    """

    DEBUG = False
    CSRF_ENABLED = True
    TESTING = False
    JWT_SECRET_KEY = 'super-secret-key'
    JWT_BLACKLIST_ENABLED = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    SQLALCHEMY_DATABASE_URI = 'postgresql://dmwangi:postgres@localhost/hellobooks_db'


class DevelopmentConfig(Config):
    """[summary]
    
    Arguments:
        Config {[type]} -- [description]
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://dmwangi:postgres@localhost/hellobooks_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """[summary]
    
    Arguments:
        Config {[type]} -- [description]
    """

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/hellobooks_test'
    # SQLALCHEMY_DATABASE_URI = 'postgresql://dmwangi:postgres@localhost/hellobooks_test'


class StagingConfig(Config):
    """[summary]
    
    Arguments:
        Config {[type]} -- [description]
    """

    DEBUG = True


class ProductionConfig(Config):
    """[summary]
    
    Arguments:
        Config {[type]} -- [description]
    """

    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}