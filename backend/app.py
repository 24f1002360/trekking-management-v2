from flask import Flask 
from flask_cors import CORS
from config import Config
from extensions import db, jwt , mail
from models import *
from routes.auth import auth
from routes.admin import admin
from routes.staff import staff
from routes.trekker import trekker
from routes.trek import trek 

app=Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)
mail.init_app(app)
@jwt.invalid_token_loader
def invalid_token_callback(error):
    print("INVALID TOKEN:", error)
    return {"message": error}, 422


@jwt.unauthorized_loader
def missing_token(error):
    print("MISSING TOKEN:", error)
    return {"message": error}, 401


@jwt.expired_token_loader
def expired(jwt_header, jwt_payload):
    print("TOKEN EXPIRED")
    return {"message": "Expired"}, 401


app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(staff)
app.register_blueprint(trekker)
app.register_blueprint(trek)

 

if __name__=='__main__':
    app.run(debug=True)