"""
[
    Config file
]
"""

import os


class Config(object):
    """
    [
        Global configs
    ]
    """
    DEBUG = False
    CSRF_ENABLED = True
    TESTING = False
    JWT_SECRET_KEY = 'super-secret-key'
    JWT_BLACKLIST_ENABLED = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    SQLALCHEMY_DATABASE_URI = 'postgresql://dmwangi:postgres@localhost/hellobooks_db'


class DevelopmentConfig(Config):
    """
    [
        Development configs
    ]
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://dmwangi:postgres@localhost/hellobooks_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
    [
        Testing configs
    ]
    """
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/hellobooks_test'


class StagingConfig(Config):
    """
    [
        Staging configs
    ]
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    [
        Proguction configs
    ]
    """
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
