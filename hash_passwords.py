from app import create_app, db
from app.models.account import Account
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    batch_size = 50  # обрабатываем по 50 записей за раз
    offset = 0

    while True:
        accounts = Account.query.offset(offset).limit(batch_size).all()
        if not accounts:
            break

        for acc in accounts:
            if acc.password_hash and not acc.password_hash.startswith("pbkdf2:sha256"):
                acc.password_hash = generate_password_hash(acc.password_hash)
        db.session.commit()
        offset += batch_size

print("Все старые пароли теперь захэшированы!")
