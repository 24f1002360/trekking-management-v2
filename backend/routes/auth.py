from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models import User 
from datetime import datetime
auth= Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data= request.get_json()
    existing_user= User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400
    existing_phone = User.query.filter_by(phone=data["phone"],role="TREKKER").first()
    if existing_phone:
        return jsonify({
            "message":"Phone already exists"
        }),400
    new_user= User(name=data['name'], email=data['email'], password=generate_password_hash(data['password']), phone=data['phone'], role='TREKKER', status='ACTIVE')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registration Successful'}), 201    



@auth.route('/login', methods=['POST'])
def login():
    data= request.get_json()
    user= User.query.filter_by(email=data['email']).first()
    if user is None:
        return jsonify({"message": "Invalid Emial "}), 401
    if not check_password_hash(user.password, data['password']):
        return jsonify({'message':'Invalid Password '}), 401
    if user.status !='ACTIVE':
        return jsonify({"message": 'Account is not active'}), 403
    access_token = create_access_token(identity=str(user.id))
    return jsonify(
        {
            'message': 'Login successful',
            'token': access_token,
            'role': user.role
        }
    ),200
        