from application import app

if __name__ == '__main__':
    print('application started in port: 8080')
    app.run(port=8080, debug=True)