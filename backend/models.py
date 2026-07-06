from datetime import datetime 
from extensions import db
class User(db.Model):
    __tablename__= 'users'
    id= db.Column(db.Integer, primary_key=  True )
    name= db.Column(db.String(100), nullable=False)
    email= db.Column(db.String(120), unique=True , nullable=False, index=True )
    password= db.Column(db.String(255), nullable=False)
    phone= db.Column(db.String(15), unique=True , nullable= True)
    role = db.Column(db.String(20), nullable= False, index= True )
    status = db.Column(db.String(20), nullable=False, default='ACTIVE', index=True)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True, cascade='all, delete-orphan')
    assigned_treks= db.relationship('Trek', backref='staff', lazy=True)
   
    
    
class Trek(db.Model):
    __tablename__='treks'
    id= db.Column(db.Integer, primary_key=True)
    trek_name= db.Column(db.String(100), nullable=False, index=True)
    location= db.Column(db.String(100), nullable=False, index=True)
    difficulty= db.Column(db.String(20),nullable=False)
    duration=db.Column(db.Integer, nullable=False)
    description=db.Column(db.Text, nullable=True)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots= db.Column(db.Integer, nullable=False)
    assigned_staff_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status= db.Column(db.String(20), nullable=False, default='PENDING', index=True)
    start_date= db.Column(db.Date, nullable=False)
    end_date= db.Column(db.Date, nullable=False)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    bookings= db.relationship('Booking', backref='trek', lazy=True, cascade='all, delete-orphan')
   
    
class Booking(db.Model):
    __tablename__= 'bookings'
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trek_id= db.Column(db.Integer, db.ForeignKey('treks.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status= db.Column(db.String(20), nullable=False, default='BOOKED', index=True)
    payment_status= db.Column(db.String(20), nullable=False, default='PENDING')
    