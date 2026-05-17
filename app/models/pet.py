from app import db
from .basemodel import BaseModel


class Pet(BaseModel):
    __tablename__ = 'pet'

    id_pet = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_client = db.Column(
        db.Integer,
        db.ForeignKey('client.id_client'),
        nullable=False
    )

    name = db.Column(db.String(100))

    sex = db.Column(
        db.String(1),
        nullable=True
    )

    id_breed = db.Column(
        db.Integer,
        db.ForeignKey('breed.id_breed'),
        nullable=True
    )

    date_birth = db.Column(db.Date)

    photo = db.Column(db.Text)

    # CHECK constraint
    __table_args__ = (
        db.CheckConstraint(
            "sex IN ('M', 'F')",
            name='chk_pet_sex'
        ),
    )

    # Отношения
    breed_rel = db.relationship('Breed', backref='pets')

    def __repr__(self):
        return f"<Pet {self.name}>"

    def to_dict(self, include_records=False):
        # Получаем данные о породе и виде через связи
        breed_name = self.breed_rel.name_breed if self.breed_rel else None
        type_name = self.breed_rel.pet_type.name_type if (self.breed_rel and self.breed_rel.pet_type) else None

        data = {
            "id_pet": self.id_pet,
            "id_client": self.id_client,
            "name": self.name,
            "sex": self.sex,
            "id_breed": self.id_breed,
            "breed": breed_name,  # Для обратной совместимости с фронтом
            "type": type_name,  # Для обратной совместимости с фронтом
            "date_birth": self.date_birth.isoformat() if self.date_birth else None,
            "photo": self.photo,
            "owner": {
                "id_client": self.owner.id_client,
                "name": self.owner.name
            } if hasattr(self, 'owner') and self.owner else None
        }

        if include_records:
            # Твой существующий код обработки медкарты остается прежним, 
            # так как связи с медкартой не менялись.
            if hasattr(self, 'med_card') and self.med_card:
                mc = self.med_card
                data["med_cards"] = [
                    {
                        "id_med_card": mc.id_med_card,
                        "date_open": mc.date_open.isoformat() if mc.date_open else None,
                        "records": [
                            {
                                "id_record": r.id_record,
                                "date_service": r.date_service.isoformat() if r.date_service else None,
                                "service": {"name_service": r.service.name_service,
                                            "cost": r.service.cost} if r.service else None,
                                "employee": {"name_emp": r.employee.name_emp} if r.employee else None,
                                "comment": r.comment,
                                "file_link": r.file_link
                            }
                            for r in getattr(mc, 'records', [])
                        ],
                        "diagnoses": [
                            {
                                "id_diagnosis_record": d.id_diagnosis_record,
                                "diagnosis_rel": {
                                    "id_diagnosis": d.id_diagnosis,
                                    "name_diagnosis": getattr(d.diagnosis_rel, 'name_diagnosis', None),
                                    "classs": getattr(d.diagnosis_rel.classs, 'name_class', None) if getattr(
                                        d.diagnosis_rel, 'classs', None) else None
                                },
                                "date_diagnosis": d.date_diagnosis.isoformat() if d.date_diagnosis else None,
                                "status": d.status,
                                "comments": d.comments
                            }
                            for d in getattr(mc, 'diagnoses', [])
                        ]
                    }
                ]
            else:
                data["med_cards"] = []

        return data