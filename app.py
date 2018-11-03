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

app = Flask(
    __name__,
    static_folder='./uploads'
)

app.config['UPLOAD_FOLDER'] = './uploads'

app.config.update(
    CELERY_BROKER_URL='amqp://guest@localhost:5672/',
    CELERY_RESULT_BACKEND='amqp://guest@localhost:5672/'
)

api = Api(app)

celery = make_celery(app)

@celery.task(name="tasks.image-resize")
def imageResize(width, filename):
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/problem')
def problem():
    return render_template('problem.html')

@app.route('/resolve')
def resolve():
    return render_template('resolve.html')

@app.route('/media/<int:width>/<string:imagename>')
def media(width, imagename):
    print(width, imagename)
    return render_template(
        'index.html'
    )
ALLOWED_EXTENSIONS = ['jpeg','jpg','png']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename)
            )
            return redirect(
                    url_for(
                        'upload_file',
                        filename=filename
                    )
            )
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

api.add_resource(RestMedia, '/api/v1/media')

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=8080)
