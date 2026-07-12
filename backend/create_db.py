from app import app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role="ADMIN").first()
    if admin is None:
        admin = User( name="Admin",
            email='admintrek8810@gmail.com',
            password=generate_password_hash('admin8810'),
            role="ADMIN",
            status="ACTIVE"
        )

        db.session.add(admin)
        db.session.commit()

        print('Admin Created Successfully ')

    else:

        print('Admin Exists')
    print("Database Created ")