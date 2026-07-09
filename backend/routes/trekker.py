from flask import Blueprint, jsonify 
from flask_jwt_extended import jwt_required, get_jwt_identity 
from models import User
trekker= Blueprint('trekker', __name__)
@trekker.route('/trekker/dashboard', methods=['GET'])
@jwt_required()
def trekker_dashboard():
    user_id = get_jwt_identity()
    user= User.query.get(user_id)
    if user.role != 'TREKKER':
        return jsonify({'message': 'Access Denied'}), 403
    return jsonify({
        'message': 'Welcome Trekker',
        'name': user.name,
        'role': user.role
    }), 200 