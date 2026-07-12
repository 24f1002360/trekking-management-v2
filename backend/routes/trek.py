from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Trek, Booking
from extensions import db 
from datetime import datetime

trek = Blueprint('trek', __name__)
@trek.route('/treks', methods=['POST'])
@jwt_required()
def create_trek():
    admin= User.query.get(int(get_jwt_identity()))
    if admin.role!= 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    data = request.get_json()
    staff_id = int(data["assigned_staff_id"]) if data.get("assigned_staff_id") else None
    start_date = datetime.strptime(
        data["start_date"],
        "%Y-%m-%d"
    ).date()
    end_date = datetime.strptime(
        data["end_date"],
        "%Y-%m-%d"
    ).date()
    if staff_id:
        existing_staff = Trek.query.filter(
            Trek.assigned_staff_id == staff_id,
            Trek.start_date <= end_date,
            Trek.end_date >= start_date,
            Trek.status.in_(["OPEN", "ONGOING", "APPROVED"])
        ).first()
        if existing_staff:
            return jsonify({
                "message": "Staff is already assigned to another trek during these dates."
            }), 400
    existing_trek = Trek.query.filter_by(
    trek_name=data['trek_name']).first()
    if existing_trek:
        return jsonify({
        "message":"Trek already exists"
    }),400
    new_trek = Trek(
        trek_name=data['trek_name'],
        location=data['location'],
        difficulty= data['difficulty'],
        duration=data['duration'],
        description=data['description'],
        total_slots= data['total_slots'],
        available_slots = data['total_slots'],
        assigned_staff_id = staff_id,
        status= data['status'],
        start_date = start_date,
        end_date = end_date
        
        )
    db.session.add(new_trek)
    db.session.commit()
    return jsonify({'message': 'Trek Created'}), 201
    
    
@trek.route('/treks', methods=['GET'])    
@jwt_required()
def all_treks():
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    treks = Trek.query.all()
    result = []
    for trek in treks:
        result.append({
            'id': trek.id,
            "trek_name": trek.trek_name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "description": trek.description,
            "total_slots": trek.total_slots,
            "available_slots": trek.available_slots,
            'assigned_staff_id': trek.assigned_staff_id,
            'assigned_staff_name': trek.staff.name if trek.staff else 'Not Assigned',
            "status": trek.status,
            "start_date": str(trek.start_date),
            "end_date": str(trek.end_date)
            
        }) 
    return jsonify(result), 200    



@trek.route('/treks/<int:id>', methods=['PUT'])
@jwt_required()
def update_trek(id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify ({'message': 'Access Denied'}), 403
    trek_data= Trek.query.get(id)
    if trek_data is None:
        return jsonify({ 'message': 'Trek not found'}), 404
    data= request.get_json()
    trek_data.trek_name = data['trek_name']
    trek_data.location = data['location']
    trek_data.difficulty= data['difficulty']
    trek_data.duration = data['duration']
    trek_data.description = data['description']
    trek_data.total_slots = data['total_slots']
    trek_data.available_slots = data['available_slots']
    staff_id = int(data["assigned_staff_id"]) if data.get("assigned_staff_id") else None
    new_start = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    new_end = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
    if staff_id:
        existing = Trek.query.filter(
            Trek.assigned_staff_id == staff_id,
            Trek.id != trek_data.id,
            Trek.start_date <= new_end,
            Trek.end_date >= new_start,
            Trek.status.in_(["OPEN", "ONGOING", "APPROVED"])
        ).first()
        if existing:
            return jsonify({
                "message": "Staff already assigned to another trek during these dates."
            }), 400
    trek_data.assigned_staff_id = staff_id
    trek_data.status = data['status']
    if trek_data.status == "COMPLETED":
        bookings = Booking.query.filter_by(
            trek_id=trek_data.id).all()
        for booking in bookings:
            if booking.status == "BOOKED":
                booking.status = "COMPLETED"
    trek_data.start_date = new_start
    trek_data.end_date = new_end
    db.session.commit()
    return jsonify({'message': 'Trek Updated'}), 200



@trek.route('/treks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_trek(id):
    admin = User.query.get(int(get_jwt_identity()))
    if admin.role != 'ADMIN':
        return jsonify({'message': 'Access Denied'}), 403
    trek_data = Trek.query.get(id)
    if trek_data.bookings:
        return jsonify({
        'message':'Cannot delete trek because bookings exist'
    }),400
    if trek_data is None :
        return jsonify({'message': 'Trek not found'}), 404
    db.session.delete(trek_data)
    db.session.commit()
    return jsonify({'message': 'Trek Deleted'}), 200