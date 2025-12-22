from flask import jsonify, request
from . import api_bp
from .utils import get_entity, create_entity, del_entity
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
    diagnosis_pet = create_entity(Diagnosis_pet, data)
    return jsonify({"id_diagnosis_pet": diagnosis_pet.id_diagnosis_pet})