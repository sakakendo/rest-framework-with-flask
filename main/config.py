import os

ENVIRONMENT = os.environ.get('ENV')

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

if ENVIRONMENT != None:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres-server-url'
    
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
