from flask import jsonify, request
from . import api_bp
from .utils import get_entity
from app.models.diagnosis_pet import Diagnosis_pet


@api_bp.route('/diagnosis_pets', methods=['GET'])
def get_diagnosis_pets():
    return get_entity(Diagnosis_pet)

@api_bp.route('/diagnosis_pets/<int:id>', methods=['GET'])
def get_diagnosis_pet():
    return get_entity(Diagnosis_pet, id)


@api_bp.route('/diagnosis_pets', methods=['POST'])
def create_diagnosis_pets():
    data = request.get_json()

    # проверяем обязательные поля
    required_fields = ['id_med_card', 'id_diagnosis', 'date_diagnosis', 'status']
    for f in required_fields:
        if f not in data:
            return jsonify({"error": f"'{f}' обязателен"}), 400

    diagnosis_pet = Diagnosis_pet(
        id_med_card=data['id_med_card'],
        id_diagnosis=data['id_diagnosis'],
        date_diagnosis=data['date_diagnosis'],
        status=data['status'],
        comments=data.get('comments')
    )

    from app import db
    db.session.add(diagnosis_pet)
    db.session.commit()

    return jsonify({"id_diagnosis_record": diagnosis_pet.id_diagnosis_record})


@api_bp.route('/diagnosis_pets/<int:id>', methods=['PATCH'])
def update_diagnosis_pet(id):
    diagnosis_pet = Diagnosis_pet.query.get_or_404(id)
    data = request.get_json()

    # проверяем есть ли статус в запросе
    if 'status' in data:
        diagnosis_pet.status = data['status']

    if 'comments' in data:
        diagnosis_pet.comments = data['comments']

    from app import db
    db.session.commit()
    return jsonify({"message": "Диагноз обновлён", "status": diagnosis_pet.status})
