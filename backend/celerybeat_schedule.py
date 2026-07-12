from celery.schedules import crontab
from celery_worker import celery 

celery.conf.beat_schedule ={
    'daily-trek-reminder':{
        'task': 'tasks.tasks.send_daily_reminder',
        'schedule': crontab(hour=8 ,minute=0)
    },
    'monthly-admin-report':{
        'task':'tasks.tasks.send_monthly_report',
        'schedule':crontab(hour=8, minute=0, day_of_month='1')
    }
}
celery.conf.timezone ='Asia/Kolkata'