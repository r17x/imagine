static_folder = './uploads'
CELERY_BROKER_URL = 'amqp://guest@localhost:5672/',
CELERY_RESULT_BACKEND = 'amqp://guest@localhost:5672/'
UPLOAD_FOLDER = static_folder

HOST = "localhost"
PORT  = 8080
DEBUG = True

