import jwt
import datetime

class Utils(object):
    key = 'secret'
    def __init__(self):
        pass

    def bytesToString(self, token):
        return token.decode("utf-8")

    def stringToBytes(self, token):
        return token.encode("utf-8")

    def checkTokenExpiry(self, token):
        return jwt.decode(self.stringToBytes(token), self.key, algorithms=['HS256'])

    def generateToken(self, user):
        return jwt.encode({'user: ': user, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, self.key, algorithm='HS256')