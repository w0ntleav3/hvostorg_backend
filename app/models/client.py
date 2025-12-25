from app import db
from .basemodel import BaseModel

class Client(BaseModel):
    id_client = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    discount =db.Column(db.Integer)
    id_account = db.Column(
        db.Integer,
        db.ForeignKey('account.id_account')

    )
    pets = db.relationship('Pet', backref='owner', lazy=True)
    account = db.relationship('Account', backref='client', uselist=False)

    def __repr__(self):
        return f"<Client {self.name}>"

