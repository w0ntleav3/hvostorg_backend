from flask import jsonify, request
from . import api_bp
from .utils import get_entity, create_entity
from app.models.pet_type import PetType
from .. import db


# Получить все виды животных
@api_bp.route('/pet_types', methods=['GET'])
def get_pet_types():
    return get_entity(PetType)


# Создать новый вид (например, если в клинику принесли енота)
@api_bp.route('/pet_types', methods=['POST'])
def create_pet_type():
    data = request.get_json()
    if not data or 'name_type' not in data:
        return jsonify({"error": "Название вида обязательно"}), 400

    new_type = create_entity(PetType, **data)
    return jsonify(new_type.to_dict()), 201


# Удалить вид (опционально)
@api_bp.route('/pet_types/<int:id>', methods=['DELETE'])
def delete_pet_type(id):
    obj = PetType.query.get(id)
    if not obj:
        return jsonify({"error": "Вид не найден"}), 404
    db.session.delete(obj)
    db.session.commit()
    return jsonify({"message": "Удалено"}), 200