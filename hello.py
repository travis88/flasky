from datetime import datetime
from flask import Flask, request, make_response, redirect, abort, render_template
from flask_script import Manager
from flask_moment import Moment

app = Flask(__name__)
manager = Manager(app)
moment = Moment(app)

# @app.route('/')
# def main():
#     user_agent = request.headers.get('User-Agent')
#     return '<p>Your browser is %s</p>' % user_agent

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def get_user(name):
    return render_template('user.html', name=name)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()