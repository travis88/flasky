# import os
# from datetime import datetime
# from flask import Flask, request, make_response, redirect, abort, render_template, url_for, session, flash
# from flask_script import Manager, Shell
# from flask_moment import Moment
# from flask_wtf import Form
# from wtforms import StringField, SubmitField
# from wtforms.validators import Required
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, MigrateCommand
# from flask_mail import Mail, Message
# from threading import Thread
    
# printenv --see enivironment variables in terminal
# .bashrc --set environment variables
# | grep --is like search (printenv | grep POSTGRES)

# def get_env_variable(name):
#     try:
#         return os.environ[name]
#     except:
#         message = "Expected environment variable '{}' not set.".format(name)
#         raise Exception(message)

# POSTGRES_URL = get_env_variable("POSTGRES_URL")
# POSTGRES_USER = get_env_variable("POSTGRES_USER")
# POSTGRES_PW = get_env_variable("POSTGRES_PW")
# POSTGRES_DB = 'hello'
# DB_URL = 'postgres+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, 
#                                                              pw=POSTGRES_PW, 
#                                                              url=POSTGRES_URL, 
#                                                              db=POSTGRES_DB)

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'hard to quess string'
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True   
# app.config['MAIL_USERNAME'] = get_env_variable('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = get_env_variable('MAIL_PASSWORD')
# app.config['FLASKY_ADMIN'] = get_env_variable('FLASKY_ADMIN')
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
# app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
# manager = Manager(app)
# moment = Moment(app)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# manager.add_command('db', MigrateCommand)
# mail = Mail(app)

# class NameForm(Form):
#     name = StringField('What is your name?', validators=[Required()])
#     submit = SubmitField('Submit')

# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')

#     def __repr__(self):
#         return '<Role %r>' % self.name

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True, index=True)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

#     def __repr__(self):
#         return '<User %r>' % self.name

# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
# manager.add_command("shell", Shell(make_context=make_shell_context))

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

# def send_mail(to, subject, template, **kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
#                     sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     thr = Thread(target=send_async_email, args=[app, msg])
#     thr.start()
#     return thr

# @app.route('/')
# def main():
#     user_agent = request.headers.get('User-Agent')
#     return '<p>Your browser is %s</p>' % user_agent

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = NameForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(name=form.name.data).first()
#         if user is None:
#             user = User(name=form.name.data, role_id=1)
#             db.session.add(user)
#             session['known'] = False
#             if app.config['FLASKY_ADMIN']:
#                 send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
#         else:
#             session['known'] = True
#         session['name'] = form.name.data
#         form.name.data = ''
#         return redirect(url_for('index'))
#     return render_template('index.html', form=form, 
#                             name=session.get('name'), known=session.get('known', False))

# @app.route('/user/<name>')
# def get_user(name):
#     return render_template('user.html', name=name)

# @app.route('/badrequest')
# def bad():
#     return '<h1>Bad request</h1>', 400

# @app.route('/setcookie')
# def cookie():
#     response = make_response('<h1>This document carries a cookie!</h1>')
#     response.set_cookie('answer', '42')
#     return response

# @app.route('/redirect')
# def my_redirect():
#     return redirect('http://example.com')

# @app.route('/abort')
# def my_abort():
#     abort(404)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('500.html'), 500

# @app.cli.command('resetdb')
# def resetdb_command():
#     """Destroys and creates the database + tables."""

#     from sqlalchemy_utils import database_exists, create_database, drop_database
#     if database_exists(DB_URL):
#         print('Deleting database.')
#         drop_database(DB_URL)
#     if not database_exists(DB_URL):
#         print('Creating database.')
#         create_database(DB_URL)
#     print('Creating tables.')
#     db.create_all()
#     print('Success!')

# if __name__ == '__main__':
    # app.run(debug=True)
    # manager.run()