
import pymongo
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId

from helpers.password_helper import password_regex

from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = "secretkey"
# api = Api(app)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/book_api_db'
# app.config['MONGODB_SETTINGS'] = {
#     'db': 'book_api_db',
#     'host': 'localhost',
#     'port': 27017
# }

# my_client = pymongo.MongoClient("mongodb://localhost:27017/")
# my_db = my_client["book_api_db"]


mongo = PyMongo(app)

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to my API'})


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404

    return response




@app.route('/user/signup/', methods=['POST'])
def signup():
    db = mongo.db.users
    errors = []
    username = request.json.get('username', None)
    if not username:
        errors.append('Username is required')

    email = request.json.get('email', None)
    if not email:
        errors.append('Email is required')

    password = request.json.get('password', None)
    if not password:
        errors.append('Password is required')
    
    if not password_regex(password):
        errors.append('Password must be between 6 and 12 characters with at least, one uppercase and one lowercase letter')
    
    
    if len(username) < 4 or len(username) > 10:
        errors.append('username must be between 4 and 10 characters')

    # check if username or email already exists
    if db.find_one({'username': username}) or db.find_one({'email': email}):
        errors.append('username or email already exists')


    if errors:
        return jsonify({'errors': errors}), 400

    if request.method == 'POST':
        hashed_password = generate_password_hash(password)

        id = db.insert_one({'email': email, 'password': hashed_password, 'username': username})
        response = jsonify({'message': 'registered successfully'})
        response.status_code = 201
        return response
    else:
        return not_found()


@app.route('/users', methods=['GET'])
def users():
    db = mongo.db.users
    output = []

    for q in db.find():
        output.append({'id': dumps(q['_id']) ,'email' : q['email'], 'username' : q['username']})

    return jsonify({'result' : output})






if __name__ == '__main__':
    app.run(debug=True)
    # host='0.0.0.0',