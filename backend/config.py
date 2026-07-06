import os 
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = 'tma_v2_secretkey'
    JWT_SECRET_KEY = 'tma_v2_jwt_secretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(BASE_DIR, 'trek.db')
    SqlAlCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = 86400
    REDIS_URI = 'redis://localhost:6379/0'
    CELERY_BROKER_URI = REDIS_URI
    CELERY_RESULT_BACKEND = REDIS_URI
    EXPORT_FOLDER = os.path.join(BASE_DIR, 'exports')