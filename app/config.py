import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost/hvosstorg'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('admin') or 'admin'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

