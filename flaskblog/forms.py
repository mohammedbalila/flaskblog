from flask_wtf import FlaskForm
from wtforms import (
    BooleanField, PasswordField, StringField,
    SubmitField, DateField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError)
from flask_login import current_user
from flaskblog.models.User import User


class SignupForm(FlaskForm):
    """
        This class will create a sign up form
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Username already taken please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        print("result: ", user)
        if user:
            raise ValidationError(
                'Email already taken please choose another one.')


class SigninForm(FlaskForm):
    """
        This class will create the login form
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class SignupPartTwo(FlaskForm):
    profile_image = FileField('Profile Image', validators=[
                              FileAllowed(['jpg', 'png'])])
    bio = StringField('Bio', validators=[Length(min=0, max=120)])


class UpdateUserForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = StringField('Bio', validators=[Length(min=0, max=120)])
    profile_image = FileField('Profile Image', validators=[
                              FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Done')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and current_user.username != username.data:
            raise ValidationError(
                'Username already taken please choose another one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and current_user.email != email.data:
            raise ValidationError(
                'Email already taken please choose another one.')


class PasswordResetForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Done')
