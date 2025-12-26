import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # берём переменные из .env

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:admin@localhost/hvosstorg')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'admin')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
