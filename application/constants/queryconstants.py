GET_USERS = 'select * from dbo.users'     
GET_FUTSALS = 'select * from dbo.futsals'
CHECK_USER_EXISTS = 'select * from dbo.users where username=%s'
ADD_USER = 'INSERT INTO dbo.users(username, password, user_type) VALUES (%s, %s, %s)'