from datetime import date

from app import db
from flask import jsonify, request
from . import api_bp
from .utils import get_entity
from app.models.employee import Employee
from app.models.vet import Vet
from ..models.record_service import RecordService


#тут надо разобраться с тем как у меня распределяются веты и сотрудники
# Получить всех ветов
@api_bp.route('/vets', methods=['GET'])
def get_vets():
    vets = db.session.query(Vet, Employee).join(Employee).all()
    result = []
    for vet, emp in vets:
        result.append({
            "id_emp": vet.id_emp,
            "name_emp": emp.name_emp,
            "passport": emp.passport,
            "phone": emp.phone,
            "salary": emp.salary,
            "spec": vet.spec,
            "license_num": vet.license_num,
            "rating": vet.rating,
            "status": vet.status
        })
    return jsonify(result)

# Получить вета по айди
@api_bp.route('/vets/<int:id>', methods=['GET'])
def get_vet(id):
    return get_entity(Vet, id)

# Создать вета
@api_bp.route('/vets', methods=['POST'])
def create_vet():
    data = request.get_json()

    emp_data = {k: data[k] for k in ['id_account', 'id_post', 'name_emp', 'passport', 'phone', 'salary', 'bank_acc_number', 'contract_num']}
    vet_data = {k: data[k] for k in ['spec', 'status', 'license_num', 'rating']}

    # создаём сотрудника
    employee = Employee(**emp_data)
    db.session.add(employee)
    db.session.commit()  # чтобы появился id_emp

    # создаём вета
    vet = Vet(id_emp=employee.id_emp, **vet_data)
    db.session.add(vet)
    db.session.commit()

    return jsonify({"id_emp": vet.id_emp})


@api_bp.route('/vets/with-records', methods=['GET'])
def get_vets_with_records_safe():
    vets = db.session.query(Vet).all()
    result = []

    for v in vets:
        if not v.employee:
            continue

        # выбираем все записи, которые относятся к этому врачу
        future_records = []
        records = db.session.query(RecordService).filter_by(id_emp=v.id_emp).all()
        for r in records:
            if not r.date_service:
                continue
            record_date = r.date_service.date() if hasattr(r.date_service, 'date') else r.date_service
            if record_date >= date.today() and getattr(r, 'med_card', None) and getattr(r.med_card, 'pet', None):
                future_records.append({
                    "id_record": r.id_record,
                    "date_service": record_date.isoformat(),
                    "pet_id": r.med_card.id_pet,
                    "pet_name": r.med_card.pet.name,
                    "client_id": r.med_card.pet.id_client,
                    "client_name": r.med_card.pet.owner.name
                })

        result.append({
            "id_emp": v.id_emp,
            "name_emp": v.employee.name_emp,
            "spec": v.spec,
            "rating": v.rating,
            "future_records": future_records
        })

    return jsonify(result)

