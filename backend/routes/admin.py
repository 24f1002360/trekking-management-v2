from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity 
from models import User

admin= Blueprint('admin', __name__)

@admin.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    return jsonify(
        {
            'messgae':'Welcome Admin',
            'name': user.name,
            'role': user.role
        }
    ),200