from app import db
from .basemodel import BaseModel

class Account(BaseModel):
    id_account = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    id_role = db.Column(db.Integer, nullable=False)
    employees = db.relationship('Employee', backref='account', lazy=True)

    def __repr__(self):
        return f"<Account {self.login}>"

    # потом добавить хеш
    def check_password(self, password_input):
        return self.password == password_input
