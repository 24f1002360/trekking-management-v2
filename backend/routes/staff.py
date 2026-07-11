from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Trek, Booking
from extensions import db 

staff=Blueprint("staff", __name__)

@staff.route('/staff/dashboard', methods=['GET'])
@jwt_required()
def staff_dashborad():
    user=User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message": "Your account has been blacklisted. Contact Admin."
        }),403
    if user.role != 'STAFF':
        return jsonify({'message': 'Access Denied'}), 403
    treks = Trek.query.filter_by(assigned_staff_id=user.id).all()
    result=[]
    for trek in treks:
        result.append({
            'trek_id':trek.id, 
            'trek_name':trek.trek_name,
            'status': trek.status,
            'available_slots':trek.available_slots,
            'registered_users':Booking.query.filter_by(trek_id=trek.id).count()
        })
    return jsonify(result),200




@staff.route('/staff/treks', methods=['GET'])
@jwt_required()
def assigned_treks():
    user=User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message": "Your account has been blacklisted. Contact Admin."
        }),403
    if user.role!='STAFF':
        return jsonify({'message': 'Access Denied'}),403
    treks=Trek.query.filter_by(assigned_staff_id=user.id).all()
    result=[]
    for trek in treks:
        result.append({
            'id':trek.id,
            'trek_name':trek.trek_name,
            'location':trek.location,
            'difficulty':trek.difficulty,
            'duration':trek.duration,
            'description': trek.description,
            'total_slots':trek.total_slots,
            'available_slots':trek.available_slots,
            'status':trek.status,
            'start_date':str(trek.start_date),
            'end_date':str(trek.end_date)
        })
    return jsonify(result),200


@staff.route('/staff/treks/<int:id>',methods=['PUT'])
@jwt_required()
def update_trek(id):
    user=User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message": "Your account has been blacklisted. Contact Admin."
        }),403
    if user.role!='STAFF':
        return jsonify({'message': 'Access Denied'}), 403
    trek=Trek.query.get(id)
    if trek is  None:
        return jsonify({'message': 'Trek not found'}),404
    if trek.assigned_staff_id != user.id:
        return jsonify({'message':'Not your trek'}),403
    data=request.get_json()
    if data["available_slots"] < 0:
        return jsonify({
        "message":"Invalid slots"
        }),400
    trek.available_slots = data["available_slots"]
    allowed = ["OPEN","ONGOING","COMPLETED"]
    if data["status"] not in allowed:
        return jsonify({
        "message":"Invalid status"
        }),400
    trek.status = data["status"]
    if trek.status == "COMPLETED":
        bookings = Booking.query.filter_by(trek_id=trek.id).all()
        for booking in bookings:
            if booking.status == "BOOKED":
                booking.status = "COMPLETED"
    db.session.commit()
    return jsonify({
        'message':'Trek Updated'
    }),200
    
    
@staff.route('/staff/<int:id>/participants', methods=['GET'])
@jwt_required()
def participants(id):
    user=User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message": "Your account has been blacklisted. Contact Admin."
        }),403
    if user.role !='STAFF':
        return jsonify({'message': 'Acess Denied'}),403
    trek=Trek.query.get(id)
    if trek is None:
        return jsonify({'message': 'Trek not found'}),404
    if trek.assigned_staff_id != user.id:
        return jsonify({'message':'Not your trek'}),403
    bookings=Booking.query.filter_by(trek_id=id).all()
    result=[]
    for booking in bookings:
        result.append({
            'booking_id':booking.id,
            'user_name':booking.user.name,
            'email':booking.user.email,
            'phone':booking.user.phone,
            'status':booking.status
        })
    return jsonify(result),200


@staff.route('/staff/treks/<int:id>', methods=['GET'])
@jwt_required()
def trek_details(id):
    user=User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message": "Your account has been blacklisted. Contact Admin."
        }),403
    if user.role!= 'STAFF':
        return jsonify({'message':'Access Denied'}),403
    trek=Trek.query.get(id)
    if trek is None:
        return jsonify({'message': 'Trek not found'}),404
    if trek.assigned_staff_id!=user.id:
        return jsonify({'message':'Not your trek'}),403
    return jsonify({
        'id':trek.id,
        'trek.name':trek.trek_name,
        'location': trek.location,
        'difficulty':trek.difficulty,
        'duration':trek.duration,
        'description':trek.description,
        'total_slots': trek.total_slots,
        'available_slots': trek.available_slots,
        'status':trek.status,
        'start_date':str(trek.start_date),
        'end_date':str(trek.end_date)
    }),200