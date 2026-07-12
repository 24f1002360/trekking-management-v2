import os 
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = 'tma_v2_secretkey'
    JWT_SECRET_KEY = 'tma_v2_jwt_secretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASE_DIR, 'trek.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    REDIS_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND  = REDIS_URL
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "dalalgaurav554@gmail.com"
    MAIL_PASSWORD = "rmtbjikchiexvtpz"
    MAIL_DEFAULT_SENDER = "dalalgaurav554@gmail.com"
    EXPORT_FOLDER = os.path.join(BASE_DIR, 'exports')