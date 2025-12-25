from flask import jsonify, request
from . import api_bp
from .utils import get_entity, create_entity
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

    med_cards_list = []
    if pet.med_card:
        mc = pet.med_card
        records_list = []
        for r in mc.records:
            records_list.append({
                "id_record": r.id_record,
                "date_service": r.date_service.isoformat() if r.date_service else None,
                "comment": r.comment or "",
                "file_link": r.file_link,
                "service": {
                    "id_service": r.service.id_service if r.service else None,
                    "name_service": r.service.name_service if r.service else "-",
                    "cost": r.service.cost if r.service else None
                },
                "employee": {
                    "id_emp": r.employee.id_emp if r.employee else None,
                    "name": r.employee.name_emp if r.employee else "-"
                }
            })
        med_cards_list.append({
            "id_med_card": mc.id_med_card,
            "records": records_list,
            "diagnoses": [d.to_dict() for d in getattr(mc, 'diagnoses', [])]

        })

    pet_dict = pet.to_dict()
    pet_dict["med_cards"] = med_cards_list
    return jsonify(pet_dict)


# Создать питомца
@api_bp.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    pet = create_entity(Pet, **data)
    return jsonify({"id_pet": pet.id_pet})