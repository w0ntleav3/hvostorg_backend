from flask import jsonify, request
from . import api_bp
from .utils import get_entity, create_entity
from app.models.diagnosis import Diagnosis


@api_bp.route('/diagnoses', methods=['GET'])
def get_diagnoses():
    return get_entity(Diagnosis)

@api_bp.route('/diagnoses/<int:id>', methods=['GET'])
def get_diagnosis():
    return get_entity(Diagnosis, id)

@api_bp.route('/diagnoses', methods=['POST'])
def create_diagnoses():
    data = request.get_json()
    diagnosis = create_entity(Diagnosis, data)
    return jsonify({"id_diagnosis": diagnosis.id_diagnosis})