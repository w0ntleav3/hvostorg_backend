from app import db
from .basemodel import BaseModel


class Service(BaseModel):
    id_service = db.Column(db.Integer, primary_key=True, nullable = False)
    name_service = db.Column(db.String(100), nullable = False)
    cost = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"<Service {self.name_service}>"