from flask import Flask, request, make_response, redirect, abort
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent

@app.route('/user/<name>')
def get_user(name):
    return '<h1>Hello, %s!</h1>' % name

@app.route('/badrequest')
def bad():
    return '<h1>Bad request</h1>', 400

@app.route('/setcookie')
def cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/redirect')
def my_redirect():
    return redirect('http://example.com')

@app.route('/abort')
def my_abort():
    abort(404)

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()