from flask import Blueprint, jsonify , request
from flask_jwt_extended import jwt_required, get_jwt_identity 
from models import User, Trek, Booking
from extensions import db
from extensions import cache

trekker= Blueprint('trekker', __name__)


@trekker.route('/trekker/dashboard', methods=['GET'])
@jwt_required()
def trekker_dashboard():
    user= User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message":"Your account has been blacklisted. Contact Admin."
        }),403
    if user.role != 'TREKKER':
        return jsonify({'message': 'Access Denied'}), 403
    return jsonify({
        'available_treks': Trek.query.filter_by(status='OPEN').count(),
        'my_bookings': Booking.query.filter_by(user_id=user.id).count()
    }), 200 
    
    
    
@trekker.route("/trekker/treks", methods=["GET"])
@jwt_required()
@cache.cached(timeout=300)
def available_treks():
    user = User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message":"Your account has been blacklisted. Contact Admin."
        }),403
    if user.role != 'TREKKER':
        return jsonify({'message':'Access Denied'}),403
    treks = Trek.query.filter_by(status='OPEN').all()
    result=[]
    for trek in treks:
        result.append({
            'id':trek.id,
            'trek_name':trek.trek_name,
            "staff_name": trek.staff.name if trek.staff else "Not Assigned",
            'location':trek.location,
            'difficulty':trek.difficulty,
            'duration':trek.duration,
            'description':trek.description,
            'available_slots':trek.available_slots,
            'start_date':str(trek.start_date),
            'end_date':str(trek.end_date)
        })
    return jsonify(result),200

@trekker.route('/trekker/treks/<int:id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def trek_details(id):
    user = User.query.get(int(get_jwt_identity()))
    if user.status != 'ACTIVE':
        return jsonify({
            'message': 'Your account has been blacklisted. Contact Admin.'
        }),403
    if user.role!= 'TREKKER' :
        return jsonify({
            'message': 'Access Denied'
        }), 403
    trek = Trek.query.get(id)
    if trek is None:
        return jsonify({
            "message":"Trek not found"
        }),404
    return jsonify({
        'id':trek.id,
        'trek_name' :trek.trek_name,
        'location' :trek.location,
        'staff_name' : trek.staff.name if trek.staff else 'Not Assigned',
        'difficulty': trek.difficulty,
        'duration':trek.duration,
        'description':trek.description,
        'available_slots': trek.available_slots,
        'status': trek.status,
        'start_date': str(trek.start_date),
        'end_date': str(trek.end_date)
    }), 200


@trekker.route("/trekker/book/<int:id>", methods=["POST"])
@jwt_required()
def book_trek(id):
    user = User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message":"Your account has been blacklisted. Contact Admin."
        }),403
    if user.role != "TREKKER":
        return jsonify({"message":"Access Denied"}),403
    trek= Trek.query.get(id)
    if trek is None:
        return jsonify({'message':'Trek not found'}), 404
    if trek.status != "OPEN":
        return jsonify({
            'message':'Booking is closed'
        }),400
    if trek.available_slots <= 0:
        return jsonify({
            'message':'No slots available'
        }),400
    existing = Booking.query.filter_by(
        user_id=user.id,
        trek_id=id).first()
    if existing:
        if existing.status == "BOOKED":
            return jsonify({
                "message": "Already booked"
            }),400
        if existing.status == "CANCELLED":
            existing.status = "BOOKED"
            trek.available_slots -= 1
            db.session.commit()
            
            return jsonify({
                'message' : 'Booking Successful'
            }),200
    booking = Booking(
        user_id=user.id,
        trek_id=id,
        status='BOOKED')
    trek.available_slots -= 1
    db.session.add(booking)
    db.session.commit()
    return jsonify({
        "message":"Booking Successful"
    }),201
    
    
    
@trekker.route("/trekker/bookings", methods=['GET'])
@jwt_required()
def my_bookings():
    user = User.query.get(int( get_jwt_identity() ))
    if user.status != "ACTIVE":
        return jsonify({
            "message":"Your account has been blacklisted. Contact Admin."
        }),403
    if user.role != 'TREKKER':
        return jsonify({'message': 'Access Denied' }),403
    bookings = Booking.query.filter_by(
        user_id=user.id).all()
    result=[]
    for booking in bookings:
        result.append({
            'booking_id':booking.id,
            'trek_name':booking.trek.trek_name,
            'location':booking.trek.location,
            'difficulty':booking.trek.difficulty,
            'booking_status':booking.status,
            'trek_status':booking.trek.status,
            'booking_date':
            booking.booking_date.strftime("%Y-%m-%d %H:%M")
        })
    return jsonify(result),200

@trekker.route('/trekker/bookings/<int:id>', methods=['PUT'])
@jwt_required()
def cancel_booking(id) :
    user = User.query.get(int(get_jwt_identity()))
    if user.status != 'ACTIVE':
        return jsonify({
            'message' : 'Your account has been blacklisted. Contact Admin.'
        }),403
    if user.role != 'TREKKER':
        return jsonify({
            'message':'Access Denied'
        }),403
    booking = Booking.query.get(id)
    if booking is None or booking.user_id !=user.id :
        return jsonify({
            "message":"Booking not found"
        }), 404
    if booking.trek.status != 'OPEN':
        return jsonify({
            "message":"Booking cannot be cancelled now"
        }),400
    booking.status= "CANCELLED"
    if booking.trek.available_slots < booking.trek.total_slots:
        booking.trek.available_slots += 1
    db.session.commit()
    return jsonify({
        'message':'Booking Cancelled'
    }), 200




@trekker.route("/trekker/history", methods=["GET"])
@jwt_required()
def history():
    user = User.query.get(int(get_jwt_identity()))
    if user.status != "ACTIVE":
        return jsonify({
            "message":"Your account has been blacklisted. Contact Admin."
        }),403
    if user.role != 'TREKKER' :
        return jsonify({'message':'Access Denied'}), 403
    bookings = Booking.query.filter_by( user_id=user.id ).all()
    result=[]
    for booking in bookings:
        if booking.status == "COMPLETED":
            result.append({
                    'trek_name':booking.trek.trek_name,
                    'location':booking.trek.location,
                    'difficulty':booking.trek.difficulty,
                    'completed_on': str(booking.trek.end_date)
                })
    return jsonify(result),200


@trekker.route("/trekker/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user = User.query.get(int(get_jwt_identity()))

    if user.role != "TREKKER":
        return jsonify({'message':'Access Denied'}),403

    return jsonify({
        "name":user.name ,
        "email":user.email ,
        "phone":user.phone
    }),200

@trekker.route('/trekker/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user = User.query.get(int(get_jwt_identity()))
    if user.status != 'ACTIVE':
        return jsonify({
            'message': 'Your account has been blacklisted. Contact Admin.'
        }), 403
    if user.role!= 'TREKKER':
        return jsonify({
            "message":"Access Denied"
        }), 403
    data = request.get_json()
    existing = User.query.filter(
        User.phone ==data["phone"],
        User.role == "TREKKER",
        User.id != user.id).first()
    if existing:
        return jsonify({
            'message': 'Phone already exists'
        }),400
    user.name = data['name']
    user.phone = data['phone']
    db.session.commit()
    return jsonify({
        "message": "Profile Updated"
    }), 200 
    
    
    
@trekker.route('/trekker/export-history', methods=['POST'])
@jwt_required()
def export_history():
    from tasks.tasks import export_trekking_history
    user_id = int(get_jwt_identity())
    export_trekking_history.delay(user_id)
    return {
        'message': 'CSV export started. Check your email shortly.'
    }, 202