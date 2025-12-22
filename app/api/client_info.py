"""from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api_bp
from app.models.client import Client
from app.models.account import Account

@api_bp.route('/clients/me', methods=['GET'])
@jwt_required()
def client_me():
    id_account = get_jwt_identity()
    account = Account.query.get(id_account)
    if not account or not account.client:
        return jsonify({"error": "Клиент не найден"}), 404

    client = account.client

    pets_list = []
    for pet in getattr(client, 'pets', []):
        records_list = []
        for med_card in getattr(pet, 'med_cards', []):
            for record in med_card.records_med_card:
                records_list.append({
                    "id_record": record.id_record,
                    "date_service": record.date_service.isoformat() if record.date_service else None,
                    "service": {"name": record.service.name} if record.service else {"name": "-"},
                    "employee": {"name": record.employee.name} if record.employee else {"name": "-"},
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
"""