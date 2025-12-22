from app import db
from .basemodel import BaseModel
from .employee import Employee

class Vet(BaseModel):
    __tablename__ = 'vet'

    id_emp = db.Column(db.Integer, db.ForeignKey('employee.id_emp', ondelete='CASCADE'), primary_key=True)
    spec = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    license_num = db.Column(db.String(4), nullable=False)
    rating = db.Column(db.Float)

    # связь с Employee
    employee = db.relationship('Employee', backref='vet_info', lazy=True)

    def __repr__(self):
        return f"<Vet {self.id_emp} - {self.spec}>"