from flask import Flask 
from flask_cors import CORS
from config import Config
from extensions import db, jwt
from models import *
from routes.auth import auth
from routes.admin import admin
from routes.staff import staff
from routes.trekker import trekker

app=Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(staff)
app.register_blueprint(trekker)

 

if __name__=='__main__':
    app.run(debug=True)