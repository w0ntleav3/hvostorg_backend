from flask import jsonify, request
from . import api_bp
from .utils import get_entity, create_entity
from app.models.client import Client
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models.account import Account
from .. import db


@api_bp.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.order_by(Client.name.asc()).all()
    return jsonify([c.to_dict() for c in clients])


@api_bp.route('/clients/<int:id>', methods=['GET'])
def get_client(id):
    return get_entity(Client, id)

@api_bp.route('/clients', methods=['POST'])
def create_clients():
    data = request.get_json()
    client = create_entity(Client, data)
    return jsonify({"id_client": client.id_client})

@api_bp.route('/clients/<int:id>', methods=['PUT'])
@jwt_required()
def update_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Клиент не найден"}), 404

    data = request.get_json()

    client.name = data.get('name', client.name)
    client.phone = data.get('phone', client.phone)
    client.email = data.get('email', client.email)
    client.discount = data.get('discount', client.discount)

    db.session.commit()

    return jsonify({"message": "Клиент обновлён"})



@api_bp.route('/clients/me', methods=['GET'])
def client_me():
    try:
        verify_jwt_in_request()  # проверяем токен вручную
        id_account = int(get_jwt_identity())
        print("JWT валиден, id_account:", id_account)
    except Exception as e:
        print("JWT ошибка:", e)
        return jsonify({"error": "Токен не валиден"}), 401

    account = Account.query.get(id_account)
    if not account or not account.client:
        return jsonify({"error": "Клиент не найден"}), 404

    client_list = getattr(account, "client", [])
    if not client_list:
        return jsonify({"error": "Клиент не найден"}), 404

    client = client_list[0]  # берем первого клиента

    pets_list = []
    for pet in getattr(client, 'pets', []):
        med_cards_list = []
        records_list = []

        # приводим к массиву, даже если одна карточка
        pet_med_cards = getattr(pet, 'med_cards', None) or (
            [getattr(pet, 'med_card', None)] if getattr(pet, 'med_card', None) else [])

        for med_card in pet_med_cards:
            if not med_card:
                continue
            med_cards_list.append({
                "id_med_card": med_card.id_med_card,
                "date_open": med_card.date_open.isoformat() if med_card.date_open else None
            })

            for record in getattr(med_card, 'records', []):
                records_list.append({
                    "id_record": record.id_record,
                    "date_service": record.date_service.isoformat() if record.date_service else None,
                    "service": {"name": record.service.name_service} if record.service else {"name": "-"},
                    "employee": {
                        "id": record.employee.id_emp,
                        "name": record.employee.name_emp
                    } if record.employee else {"id": None, "name": "-"},
                    "comment": record.comment,
                    "file_link": record.file_link
                })

        pets_list.append({
            "id_pet": pet.id_pet,
            "name": pet.name,
            "sex": pet.sex,
            "type": pet.type,
            "breed": pet.breed,
            "date_birth": pet.date_birth.isoformat() if pet.date_birth else None,
            "photo": pet.photo,
            "med_cards": med_cards_list,
            "records": records_list
        })

    return jsonify({
        "client": {
            "id_client": client.id_client,
            "name": client.name,
            "phone": client.phone,
            "email": client.email,
            "discount": client.discount
        },
        "pets": pets_list
    })

@api_bp.route('/clients/me', methods=['PUT'])
@jwt_required()
def update_client_me():
    id_account = int(get_jwt_identity())

    account = Account.query.get(id_account)
    if not account or not account.client:
        return jsonify({"error": "Клиент не найден"}), 404

    client_list = getattr(account, "client", [])
    if not client_list:
        return jsonify({"error": "Клиент не найден"}), 404

    client = client_list[0]

    data = request.get_json()
    if not data or 'phone' not in data:
        return jsonify({"error": "Номер телефона не передан"}), 400

    client.phone = data['phone']
    db.session.commit()

    return jsonify({
        "message": "Телефон обновлён",
        "phone": client.phone
    })



@api_bp.route('/clients/admin/<int:id>', methods=['GET'])
@jwt_required()
def admin_get_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Клиент не найден"}), 404

    pets_list = []

    for pet in getattr(client, 'pets', []):
        records_list = []
        med_cards_list = []

        med_card = getattr(pet, 'med_card', None)

        if med_card:
            med_cards_list.append({
                "id_med_card": med_card.id_med_card,
                "date_open": med_card.date_open.isoformat() if med_card.date_open else None
            })

            records = med_card.records.all() if hasattr(med_card.records, 'all') else med_card.records

            for record in records:
                records_list.append({
                    "id_record": record.id_record,
                    "date_service": record.date_service.isoformat() if record.date_service else None,
                    "service": {
                        "id_service": record.service.id_service,
                        "name_service": record.service.name_service,
                        "cost": record.service.cost
                    } if record.service else None,
                    "employee": {
                        "id_emp": record.employee.id_emp,
                        "name_emp": record.employee.name_emp
                    } if record.employee else None,
                    "comment": record.comment,
                    "file_link": record.file_link
                })
        pets_list.append({
            "id_pet": pet.id_pet,
            "name": pet.name,
            "sex": pet.sex,
            "type": pet.type,
            "breed": pet.breed,
            "date_birth": pet.date_birth.isoformat() if pet.date_birth else None,
            "photo": pet.photo,
            "med_cards": med_cards_list,
            "records": records_list
        })

    return jsonify({
        "client": {
            "id_client": client.id_client,
            "name": client.name,
            "phone": client.phone,
            "email": client.email,
            "discount": client.discount
        },
        "pets": pets_list
    })

