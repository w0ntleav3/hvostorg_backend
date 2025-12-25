from datetime import date, datetime, time, timedelta

from app import db
from flask import jsonify, request
from . import api_bp
from .utils import get_entity
from app.models.employee import Employee
from app.models.vet import Vet
from app.models.record_service import RecordService


# НАСТРОЙКИ РАБОЧЕГО ДНЯ
WORK_START = time(10, 0)
WORK_END = time(18, 0)
SLOT_DURATION_MIN = 30


# ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ
def get_free_slots_for_day(vet_id: int, target_date: date):
    records = db.session.query(RecordService).filter(
        RecordService.id_emp == vet_id,
        db.func.date(RecordService.date_service) == target_date
    ).all()

    busy_times = set()

    for r in records:
        if not r.date_service:
            continue

        # если date
        if isinstance(r.date_service, date) and not isinstance(r.date_service, datetime):
            continue

        busy_times.add(r.date_service.strftime("%H:%M"))

    slots = []
    current = datetime.combine(target_date, WORK_START)
    end = datetime.combine(target_date, WORK_END)

    while current < end:
        t_str = current.time().strftime("%H:%M")
        if t_str not in busy_times:
            slots.append(t_str)
        current += timedelta(minutes=SLOT_DURATION_MIN)

    return slots


@api_bp.route('/vets', methods=['GET'])
def get_vets():
    vets = db.session.query(Vet, Employee).join(Employee).all()
    result = []

    for vet, emp in vets:
        result.append({
            "id_emp": vet.id_emp,
            "name_emp": emp.name_emp,
            "phone": emp.phone,
            "spec": vet.spec,
            "rating": vet.rating,
            "status": vet.status
        })

    return jsonify(result)


@api_bp.route('/vets/<int:id>', methods=['GET'])
def get_vet(id):
    return get_entity(Vet, id)


@api_bp.route('/vets', methods=['POST'])
def create_vet():
    data = request.get_json()

    emp_data = {k: data[k] for k in [
        'id_account', 'id_post', 'name_emp',
        'passport', 'phone', 'salary',
        'bank_acc_number', 'contract_num'
    ]}
    vet_data = {k: data[k] for k in ['spec', 'status', 'license_num', 'rating']}

    employee = Employee(**emp_data)
    db.session.add(employee)
    db.session.commit()

    vet = Vet(id_emp=employee.id_emp, **vet_data)
    db.session.add(vet)
    db.session.commit()

    return jsonify({"id_emp": vet.id_emp})


# ДОСТУПНЫЕ ДАТЫ
@api_bp.route('/vets/<int:id>/available_dates', methods=['GET'])
def get_vet_available_dates(id):
    days = int(request.args.get('days', 14))

    vet = db.session.query(Vet).filter_by(id_emp=id).first()
    if not vet:
        return jsonify({"error": "vet not found"}), 404

    today = date.today()
    available_dates = []

    for i in range(days):
        d = today + timedelta(days=i)
        slots = get_free_slots_for_day(id, d)
        if slots:
            available_dates.append(d.isoformat())

    return jsonify({"dates": available_dates})


# ДОСТУПНОЕ ВРЕМЯ
@api_bp.route('/vets/<int:id>/available_slots', methods=['GET'])
def get_vet_available_slots(id):
    date_str = request.args.get('date')
    if not date_str:
        return jsonify({"error": "date param required"}), 400

    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "invalid date format"}), 400

    vet = db.session.query(Vet).filter_by(id_emp=id).first()
    if not vet:
        return jsonify({"error": "vet not found"}), 404

    slots = get_free_slots_for_day(id, target_date)
    return jsonify({"slots": slots})
