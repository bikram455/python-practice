import jwt
import datetime
from application import app
from flask import request, jsonify
from application.utils import Utils
from application.service import Service, FutsalExists
import application.constants.errorconstants as ERROR_CONSTANTS

service = Service()
utils = Utils()


@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'hello'})

@app.route('/getusers', methods=['GET'])
def getUsers():
    try:
        encoded = request.headers['Authorization'].split(' ')[1]
        utils.checkTokenExpiry(encoded)
        return jsonify({'users':  service.getUsers()})
    except jwt.ExpiredSignature:
        return jsonify({'message':  ERROR_CONSTANTS.TOKEN_EXPIRED}), 401
    

@app.route('/getfutsals', methods=['GET'])
def getFutsals():
    try:
        encoded = request.headers['Authorization'].split(' ')[1]
        utils.checkTokenExpiry(encoded)
        return jsonify({'users':  service.getTodos()})
    except Exception as err:
        if type(err) == jwt.exceptions.ExpiredSignature:
            return jsonify({'message':  'Token expired, please login again'}), 409
        else:
            return jsonify({'message':  'Error while fetching user list'}), 500 

@app.route('/adduser', methods=['POST'])
def addUser():
    data = request.json
    if 'admin' not in data:
        data['admin'] = False
    res = service.adduser(data)
    return jsonify({'message': res['message']}), res['status']

@app.route('/addfutsal', methods=['POST'])
def addFutsal():
    try:
        encoded = request.headers['Authorization'].split(' ')[1]
        utils.checkTokenExpiry(encoded)
        data = request.json
        res = service.addFutsal(data)
        return jsonify({'message': res['message']})
    except Exception as err:
        if(type(err) == jwt.ExpiredSignature):
            return jsonify({'message': ERROR_CONSTANTS.TOKEN_EXPIRED}), 401
        elif(isinstance(err, FutsalExists)):
            return jsonify({'message': str(err)}), 409
        else:
            return jsonify({'message': ERROR_CONSTANTS.ADD_FUTSAL_ERROR}), 400

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

@app.route('/getfutsals', methods=['GET'])
def getFutsals():
    try:
        encoded = request.headers['Authorization'].split(' ')[1]
        utils.checkTokenExpiry(encoded)
        return jsonify({'futsals':  service.getFutsals()})
    except jwt.ExpiredSignature:
        return jsonify({'message':  'Token expired, please login again'}), 401

@app.route('/addfutsal', methods=['POST'])
def addfutsal():
    try:
        encoded = request.headers['Authorization'].split(' ')[1]
        utils.checkTokenExpiry(encoded)
        return jsonify({'futsals':  service.addFutsal(request.json)})
    except Exception as err:
        if(type(err) == jwt.ExpiredSignature):
            return jsonify({'message':  'Token expired, please login again'}), 401