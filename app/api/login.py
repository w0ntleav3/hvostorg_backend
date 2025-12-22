from flask import request, jsonify
from flask_jwt_extended import create_access_token
from app.models.account import Account
from app import db
from . import api_bp

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    account = Account.query.filter_by(login=login).first()
    if not account or not account.check_password(password):
        return jsonify({"error": "Неверные данные"}), 401

    # создаём токен с id_account
    access_token = create_access_token(identity=str(account.id_account))

    return jsonify({
        "token": access_token,
        "id_account": account.id_account,
        "id_role": account.id_role
    })
