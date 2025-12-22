from app import db
from .basemodel import BaseModel


class Diagnosis_pet(BaseModel):
    id_diagnosis_record = db.Column(db.Integer, primary_key=True)
    id_med_card = db.Column(db.Integer, db.ForeignKey('med_card.id_med_card'), nullable=False)
    id_diagnosis = db.Column(db.String(10), db.ForeignKey('diagnosis.id_diagnosis'), nullable=False)
    date_diagnosis = db.Column(db.Date, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    comments = db.Column(db.Text)

    med_card = db.relationship('MedCard', backref='diagnoses', lazy=True)
    diagnosis_rel = db.relationship('Diagnosis', backref='diagnosis_records', lazy=True)  # <--- связь с диагнозом


    def __repr__(self):
        return f"<Diagnosis_pet {self.id_diagnosis_record}>"
