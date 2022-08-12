import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'top-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/ob1lab'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
