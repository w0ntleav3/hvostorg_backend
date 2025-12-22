from flask import jsonify, request
from . import api_bp
from .utils import get_entity, create_entity, del_entity
from app.models.pet import Pet


# Получить всех питомцев
@api_bp.route('/pets', methods=['GET'])
def get_pets():
    return get_entity(Pet)

# Получить питомца по айди с медкартой и записями
@api_bp.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        return jsonify({"error": "Питомец не найден"}), 404
    return jsonify(pet.to_dict(include_records=True))


# Создать питомца
@api_bp.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    pet = create_entity(Pet, **data)
    return jsonify({"id_pet": pet.id_pet})