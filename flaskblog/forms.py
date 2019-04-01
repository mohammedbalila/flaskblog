from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    Length, DataRequired, Email, EqualTo
    )


class SignupForm(FlaskForm):
    """
        This class will create a sign up form
    """
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

class SigninForm(FlaskForm):
    """
        This class will create the login form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')