import os 
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)

from flask_restful import Api
from rest.Media import RestMedia
from celery import Celery
from werkzeug.utils import secure_filename
from PIL import Image
from resizeimage import resizeimage as reimage

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker= app.config['CELERY_BROKER_URL']
    )

    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_object('settings')

api = Api(app)
# Todo , Split Celery 

celery = make_celery(app)

@celery.task(name="tasks.image-resize")
def imageResize(width, filename, output):
    img = Image.open(filename)
    img = reimage.resize_width(img, width)
    img.save(output, img.format)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/media/<int:width>/<string:imagename>')
def media(width, imagename):
    originalImage = "./static/{}".format(imagename)
    outputImage =  "./static/{}/{}".format(width, imagename)
    imageResize.apply_async((width,imagename, outputImage))
    # imageResize.delay(width, filename)
    return redirect(url_for(outputImage))

"""
    Register Rest API
"""

api.add_resource(RestMedia, '/api/v1/media')

if __name__ == '__main__':
    app.run(
        host = app.config.get('HOST'),
        port = app.config.get('PORT')
    )
