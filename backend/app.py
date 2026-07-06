from flask import Flask
from config import Config
from extensions import db, jwt
from models import *
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.staff import staff_bp
from routes.trekker import trekker_bp 

app=Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(trekker_bp)

 

if __name__=='__main__':
    app.run(debug=True)