from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User
staff=Blueprint("staff", __name__)

@staff.route('/staff/dashborad', methods=['GET'])
@jwt_required()
def staff_dashborad():
    user_id = get_jwt_identity()
    user= User.query.get(user_id)
    if user.role != 'STAFF':
        return jsonify({'message': 'Access Denied'}), 403
    return jsonify(
        {
            'message': 'Welcome Staff',
            'name': user.name,
            'role': user.role
        }
    ),200