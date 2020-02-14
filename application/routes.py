import jwt
import datetime
from application import app
from flask import request, jsonify
from application.utils import Utils
from application.service import Service

service = Service()
utils = Utils()


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'hello'})

@app.route('/getusers', methods=['GET'])
def getUsers():
    return jsonify({'users':  service.getTodos()})

@app.route('/getfutsals', methods=['GET'])
def getFutsals():
    try:
        encoded = request.headers['Authorization'].split(' ')[1]
        utils.checkTokenExpiry(encoded)
        return jsonify({'futsals':  service.getFutsals()})
    except jwt.ExpiredSignature:
        print('token is expired')
        return jsonify({'message':  'Token expired, please login again'}), 401


@app.route('/adduser', methods=['POST'])
def addUser():
    data = request.json
    if 'admin' not in data:
        data['admin'] = False
    res = service.adduser(data)
    return jsonify({'message': res['message']}), res['status']

@app.route('/login', methods=['POST'])
def login():
    try:
        if service.login(request.json):
            token = utils.generateToken(request.json['username'])
            return jsonify({'message': 'successfully logged in', 'token': utils.bytesToString(token)}), 200
        else:
            raise Exception('User Not Found')
    except:
        return jsonify({'message': 'user not found'}), 401
        

@app.route('/updateuser/<id>', methods=['POST'])
def updateUser(id):
    flag = service.updateUser(request.json, id)
    data = {
        'message': 'successfully updated user' if flag else 'Error while updating user',
        'status': 200 if flag else 400
        }
    return jsonify({'message': data['message']}), data['status']