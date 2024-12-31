from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, BooleanField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from application.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    fullname = StringField('fullname', validators=[DataRequired(), Length(min=2)])
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password =  PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])
    submit = SubmitField('submit')

    ## custom validation to catch intergrity error

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please Choose another')

    def validate_email(self, email):
        user  = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is taken. Please choose another')
        

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('remember me')
    submit = SubmitField('log in')


class UpdateAccountForm(FlaskForm):

    fullname = StringField('fullname', validators=[DataRequired(), Length(min=2)])
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    profile = FileField('Update Profile Picture :', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update Info')
    ## custom validation to catch intergrity error

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please Choose another')

    def validate_email(self, email):
       if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email is taken. Please Choose another')
            

class NewPostForm(FlaskForm):
    title = StringField('new post', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    post = SubmitField('Create post')

class UpdatePostForm(FlaskForm):
    title = StringField('update title', validators=[DataRequired()])
    content = TextAreaField('update content', validators=[DataRequired()])
    submit = SubmitField('Update post')









