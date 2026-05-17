from flask import jsonify, request
from . import api_bp
from .utils import get_entity, create_entity
from app.models.pet import Pet
from app.models.diagnosis_pet import Diagnosis_pet  # Убедись, что путь импорта правильный!
from app.models.breed import Breed  # Импортируем новую модель


# Получить всех питомцев
@api_bp.route('/pets', methods=['GET'])
def get_pets():
    # Чтобы в списке сразу были вид и порода, можно переопределить to_dict в модели
    # или сформировать список здесь вручную.
    return get_entity(Pet)


# Получить питомца по айди с подробностями
@api_bp.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    pet = Pet.query.get(id)
    if not pet:
        return jsonify({"error": "Питомец не найден"}), 404

    # Собираем данные о породе и виде
    breed_info = {
        "id_breed": pet.id_breed,
        "name_breed": pet.breed_rel.name_breed if pet.breed_rel else "Неизвестно",
        "type": pet.breed_rel.pet_type.name_type
        if pet.breed_rel and pet.breed_rel.pet_type
        else "Неизвестно"
    }

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

        # Получаем диагнозы напрямую через запрос к Diagnosis_pet,
        # чтобы гарантировать, что SQLAlchemy подгрузит все связи (relationship)
        db_diagnoses = Diagnosis_pet.query.filter_by(id_med_card=mc.id_med_card).all()

        diagnoses_list = []
        for d in db_diagnoses:
            # Логируем в консоль бэкенда для проверки, что связи существуют
            print(f"DEBUG DIAGNOSIS: id={d.id_diagnosis}, rel={d.diagnosis_rel}")
            if d.diagnosis_rel:
                print(f"DEBUG CLASS: {getattr(d.diagnosis_rel, 'classs', None)}")

            name_diag = d.diagnosis_rel.name_diagnosis if d.diagnosis_rel else "Неизвестный диагноз"
            name_cls = "-"
            if d.diagnosis_rel and d.diagnosis_rel.classs:
                name_cls = d.diagnosis_rel.classs.name_class

            diagnoses_list.append({
                "id_diagnosis_record": d.id_diagnosis_record,
                "id_med_card": d.id_med_card,
                "id_diagnosis": d.id_diagnosis,
                "date_diagnosis": d.date_diagnosis.isoformat() if d.date_diagnosis else None,
                "status": d.status,
                "comments": d.comments,
                "diagnosis_rel": {
                    "id_diagnosis": d.id_diagnosis,
                    "name_diagnosis": name_diag,
                    "classs": {
                        "name_class": name_cls
                    }
                }
            })

        med_cards_list.append({
            "id_med_card": mc.id_med_card,
            "records": records_list,
            "diagnoses": diagnoses_list
        })

    pet_dict = pet.to_dict()
    pet_dict["breed_info"] = breed_info
    pet_dict["med_cards"] = med_cards_list

    pet_dict.pop('type', None)
    pet_dict.pop('breed', None)

    return jsonify(pet_dict)


# Создать питомца
@api_bp.route('/pets', methods=['POST'])
def create_pet():
    data = request.get_json()
    # Теперь фронтенд должен присылать id_breed вместо строк breed/type
    pet = create_entity(Pet, **data)
    return jsonify({"id_pet": pet.id_pet})