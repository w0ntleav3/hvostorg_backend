from app import db
from .basemodel import BaseModel


class MedCard(BaseModel):
    __tablename__ = 'med_card'

    id_med_card = db.Column(db.Integer, primary_key=True)
    id_pet = db.Column(db.Integer, db.ForeignKey('pet.id_pet'), nullable=False)
    date_open = db.Column(db.Date, nullable=False)

    pet = db.relationship('Pet', backref=db.backref('med_card', uselist=False))

    records = db.relationship('RecordService', back_populates='med_card')


    def __repr__(self):
        return f"<Med_card {self.id_med_card}>"