from application.connection import cur, conn
import application.constants.queryconstants as QEURY_CONSTANTS
import application.constants.appconstants as APP_CONSTANTS

class Service(object):
    def __init__(self):
        pass

    def getTodos(self):
        data = []   
        cur.execute(QEURY_CONSTANTS.GET_USERS)
        rows = cur.fetchall()
        for row in rows:
            data.append({'id': row[0], 'username': row[1], 'role': row[3]})           
        return data

    def adduser(self, userData):
        message = APP_CONSTANTS.ADD_USER_SUCCESS + userData['username']
        status = 200
        cur.execute(QEURY_CONSTANTS.CHECK_USER_EXISTS, (userData['username'],))
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute(QEURY_CONSTANTS.ADD_USER, (userData['username'], userData['password'], userData['user_type']))
            conn.commit()
        else:
            message = 'user ' + userData['username'] + ' already exists'
            status = 409
        return {'message': message, 'status': status}

    def login(self, userData):
        cur.execute('select * from dbo.users where username=%s and password=%s', (userData['username'], userData['password']))
        rows = cur.fetchall()
        return len(rows) == 1

    def updateUser(self, userData, id):
        try:
            cur.execute('select * from dbo.users where userid=%s', (id,))
            print('select * from dbo.users where userid=%s', (id,))
            rows = cur.fetchall()
            if len(rows) == 0:
                print(0/0)
            cur.execute('update dbo.users set username=%s where userid=%s', (userData['username'], id))
            conn.commit()
            return True
        except Exception:
            pass
            return False
    
    def getFutsals(self):
        try:
            data = []        
            cur.execute(QEURY_CONSTANTS.GET_FUTSALS)
            rows = cur.fetchall()
            for row in rows:
                data.append({'id': row[0], 'futsalName': row[1], 'address': row[2], 'opens': row[3], 'closes': row[4]})
            return data
        except Exception:
            pass
            return Exception
