from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity 
from models import User, Trek ,Booking
from werkzeug.security import generate_password_hash
from extensions import db

admin= Blueprint('admin', __name__)

@admin.route('/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    return jsonify(
        {
            'total_users':
                User.query.filter_by(role='TREKKER').count(),
            'total_staff':
                User.query.filter_by(role='STAFF').count(),
            'total_treks':
                Trek.query.count(),
            'total_bookings':
                Booking.query.count(),    
            'completed_treks':
                Trek.query.filter_by(
                    status='COMPLETED'
                    ).count(),
            'open_treks':
                Trek.query.filter_by(
                    status='OPEN'
                    ).count(),
            'ongoing_treks':
                Trek.query.filter_by(
                    status='ONGOING'
                    ).count(),
            'cancelled_bookings':
                Booking.query.filter_by(
                    status='CANCELLED'
                    ).count()
        }
    ),200
    
    
    
    
@admin.route('/admin/staff', methods=['POST'])
@jwt_required()
def add_staff():
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    data = request.get_json()
    if not data.get("password"):
        return jsonify({
            "message": "Password is required"
        }), 400
    existing = User.query.filter_by(email=data['email']).first()
    if existing:
        return jsonify({'message': 'Email already Exists'}), 400
    staff= User(
        name=data['name'],
        email=data['email'],
        password= generate_password_hash(data['password']),
        phone = data['phone'],
        role='STAFF',
        status = data['status']
    )
    existing_phone = User.query.filter_by(
        phone=data["phone"],
        role="STAFF").first()
    if existing_phone:
        return jsonify({
            "message": "Phone already exists for another staff"
        }),400
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Staff Added'}), 201
    
@admin.route('/admin/staff', methods=['GET'])
@jwt_required()
def view_staff():
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    staff= User.query.filter_by(role='STAFF').all()
    result = []
    for s in staff:
        result.append({
            'id': s.id,
            'name': s.name,
            'email': s.email,
            'phone': s.phone, 
            'status': s.status,
        })   
    return jsonify(result),200

@admin.route('/admin/staff/<int:id>', methods=['PUT'])
@jwt_required()
def update_staff(id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'})
    staff = User.query.get(id)
    if staff is None or staff.role != 'STAFF':
        return jsonify({'message': 'Staff not found'}), 404
    
    data= request.get_json()
    existing_phone = User.query.filter(
        User.phone == data["phone"],
        User.role == "STAFF",
        User.id != id).first()
    if existing_phone:
        return jsonify({
            "message":"Phone already exists for another staff"
        }),400
    existing_email = User.query.filter(User.email == data["email"],User.id != id).first()
    if existing_email:
        return jsonify({
            "message": "Email already exists"
        }),400
    staff.name = data['name']
    staff.email = data['email']
    staff.phone = data['phone']
    db.session.commit()
    return jsonify({'message': 'Staff Updated'}), 200

@admin.route('/admin/staff/<int:id>/status', methods=['PUT'])
@jwt_required()
def change_staff_status(id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    staff= User.query.get(id)
    if staff is None  or staff.role != 'STAFF':
        return jsonify({'message': 'Staff not found'}), 404
    data = request.get_json()
    staff.status = data['status']
    db.session.commit()
    return jsonify({'message':'Staff Status Updated'}),200
    
    
    
    
    
@admin.route('/admin/treks/<int:id>/assign', methods=['PUT'])
@jwt_required()
def assign_staff(id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    trek = Trek.query.get(id)
    if trek is None :
        return jsonify({'message': 'Trek not found'}), 404
    data = request.get_json()
    staff = User.query.get(data['staff_id'])
    if staff is None or staff.role != 'STAFF':
        return jsonify({'message': 'Staff not found'}), 404
    existing = Trek.query.filter(
        Trek.assigned_staff_id == data["staff_id"],
        Trek.id != trek.id,
        Trek.start_date <= trek.end_date,
        Trek.end_date >= trek.start_date,
        Trek.status.in_(["APPROVED", "OPEN", "ONGOING"])
    ).first()
    if existing:
        return jsonify({
            "message":"Staff is already assigned to another trek during these dates."
        }),400
    trek.assigned_staff_id = staff.id 
    db.session.commit()
    return jsonify({'message': 'Staff Assigned Successfully'}), 200





@admin.route('/admin/users', methods=['GET'])
@jwt_required()
def view_users():
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}),403
    users = User.query.filter_by(role='TREKKER').all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'name':user.name,
            'email': user.email,
            'phone': user.phone,
            'status':user.status,
            
        })
    return jsonify(result),200

@admin.route('/admin/users/<int:id>/status', methods=['PUT'])
@jwt_required()
def update_user_status(id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}),403
    user= User.query.get(id)
    if user is None or user.role != 'TREKKER':
        return jsonify({'message': 'User not found'}),404
    data = request.get_json()
    user.status = data['status']
    db.session.commit()
    return jsonify({'message':'User status updated'}), 200





@admin.route('/admin/bookings', methods=['GET'])
@jwt_required()
def all_boookings():
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role !='ADMIN':
        return jsonify({'message': 'Access Denied'}),403
    bookings = Booking.query.all()
    result=[]
    for booking in bookings:
        result.append({
            'booking_id':booking.id,
            'user_name':booking.user.name,
            'trek_name':booking.trek.trek_name,
            'booking_status':booking.status,
            "trek_status":booking.trek.status,
            'booking_date':booking.booking_date.strftime("%Y-%m-%d %H:%M"),
            "completed_date":
                str(booking.trek.end_date)
                if booking.status=="COMPLETED"
                else "-"
        })
    return jsonify(result),200





