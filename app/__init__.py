from flask import Flask
from .extensions import db, migrate, cors
from .api import api_bp
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager



def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/hvosstorg'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'admin'
    app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # ⚠ обязательно для JWT

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
    jwt = JWTManager(app)
    jwt.init_app(app)  # ⚠ инициализация JWTManager с приложением

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
