from flask import (
    Flask,
    render_template
)

from flask_restful import Api
from rest.Media import RestMedia

app = Flask(
    __name__,
    static_folder='./static'
)

api = Api(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/media')
def media():
    images = []
    return render_template('index.html', images=images)

api.add_resource(RestMedia, '/api/v1/media')

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=8080)
