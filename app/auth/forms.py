from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    ValidationError
from wtforms.validators import Required, Email, Length, Regexp, EqualTo
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64), 
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, '
                                                          'numbers, dots or underscores')])                                             
    password = PasswordField('Password', validators=[Required(), 
                                                     EqualTo('password2', message='Password must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])                                                                                                              
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use')