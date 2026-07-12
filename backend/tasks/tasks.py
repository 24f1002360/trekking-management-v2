from celery_worker import celery
from extensions import mail
from flask_mail import Message
from flask import render_template 
from models import Trek , Booking, User
from extensions import db
from datetime import date, timedelta, datetime
from sqlalchemy import func , extract 
from config import Config 
import csv 
import os 


@celery.task
def send_daily_reminder():
    tomorrow = date.today() + timedelta(days=1)
    treks = Trek.query.filter_by(
        start_date = tomorrow,
        status='OPEN'
    ).all()
    count = 0
    for trek in treks:
        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status='BOOKED'
        ).all()
        for booking in bookings:
            msg= Message(
                subject='Upcoming Trek Reminder',
                recipients=[booking.user.email]
            )
            msg.html=render_template(
                'reminder.html',
                name=booking.user.name,
                trek=trek.trek_name,
                location=trek.location,
                start_date=trek.start_date
            )
            mail.send(msg)
            count +=1
    return f'{count} reminder emails sent.'




@celery.task
def send_monthly_report():
    current_month = datetime.now().month
    current_year = datetime.now().year

    total_treks = Trek.query.filter(
        Trek.status == "COMPLETED",
        extract("month", Trek.end_date) == current_month,
        extract("year", Trek.end_date) == current_year
    ).count()

    total_participants = Booking.query.filter(
        Booking.status == "COMPLETED",
        extract("month", Booking.booking_date) == current_month,
        extract("year", Booking.booking_date) == current_year
    ).count()
    
    popular = (
        db.session.query(
            Trek.trek_name,
            func.count(Booking.id)
        )
        .join(Booking)
        .filter(
            Booking.status == "COMPLETED",
            extract("month", Booking.booking_date) == current_month,
            extract("year", Booking.booking_date) == current_year
        )
        .group_by(Trek.id)
        .order_by(func.count(Booking.id).desc())
        .first()
    )
    
    popular_trek = 'No Treks'
    if popular:
        popular_trek = popular[0]
        
    admin = User.query.filter_by(
        role='ADMIN'
    ).first()
    
    msg = Message(
        subject = 'Monthly Trekking Report',
        recipients=[admin.email]
    )
    msg.html = render_template(
        'monthly_report.html',
        month=datetime.now().strftime('%B %Y'),
        total_treks=total_treks,
        participants=total_participants,
        popular_trek = popular_trek
    )
    mail.send(msg)
    return 'Monthly Report Sent'
    
    
    
    
@celery.task
def export_trekking_history(user_id) :
    user = User.query.get(user_id)
    bookings =(
        Booking.query
        .filter_by(user_id= user_id)
        .all()
    )
    filename = f'trek_history_{user.id}.csv'
    filepath = os.path.join(
        Config.EXPORT_FOLDER,
        filename
    )
    os.makedirs(Config.EXPORT_FOLDER, exist_ok=True)
    with open(filepath, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            'Booking ID',
            'Trek',
            'Location',
            'Start Date',
            'End Date',
            'Booking Status'
        ])
        for booking in bookings:
            writer.writerow([
                booking.id,
                booking.trek.trek_name ,
                booking.trek.location,
                booking.trek.start_date,
                booking.trek.end_date ,
                booking.status
            ])
    msg = Message(
        subject='Your Trekking History CSV',
        recipients=[user.email]
    )
    msg.body = (
        'Your CSV export is ready, find attached .'
    )
    with open(filepath, 'rb') as fp:
        msg.attach(
            filename,
            "text/csv",
            fp.read()
        )
    mail.send(msg)
    return 'CSV Export Completed'