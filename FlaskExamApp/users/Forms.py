from flask_wtf import FlaskForm
from FlaskExamApp.Models import User
from wtforms import StringField , PasswordField , SubmitField , BooleanField , SelectField
from wtforms.fields.html5 import DateTimeField , DateField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user

class RegistrationForm(FlaskForm) :
    name = StringField("Student Name" , validators=[DataRequired() , Length(min=2 , max=20)])
    email = StringField("School Email" , validators=[DataRequired() , Email()])
    password = PasswordField("Password" , validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password" , validators=[DataRequired() , EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_name(self , name) :
        user = User.query.filter_by(name=name.data).first()
        if user :
            raise ValidationError("That name is taken. Please choose another one")

    def validate_email(self , email) :
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError("An account with that email already exists")

class UpdateAccForm(FlaskForm) :
    name = StringField("Student Name" , validators=[DataRequired() , Length(min=2 , max=20)])
    email = StringField("School Email" , validators=[DataRequired() , Email()])
    pic = FileField("Update Profile Picture" , validators=[FileAllowed(["jpg" , "png"])])
    submit = SubmitField("Update")

    def validate_name(self , name) :
        if name.data != current_user.name :
            user = User.query.filter_by(name=name.data).first()
            if user :
                raise ValidationError("That name is taken. Please choose another one")

    def validate_email(self , email) :
        if email.data != current_user.email :
            user = User.query.filter_by(email=email.data).first()
            if user :
                raise ValidationError("An account with that email already exists")

class LoginForm(FlaskForm) :
    email = StringField("School Email" , validators=[DataRequired() , Email()])
    password = PasswordField("Password" , validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RequestResetForm(FlaskForm) :
    email = StringField("School Email" , validators=[DataRequired() , Email()])
    submit = SubmitField("Request Password Reset")
    def validate_email(self , email) :
        user = User.query.filter_by(email=email.data).first()
        if not user :
            raise ValidationError("An account with this email does not exist. Please create an account first")

class ResetPasswordForm(FlaskForm) :
    password = PasswordField("Password" , validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password" , validators=[DataRequired() , EqualTo("password")])
    submit = SubmitField("Reset Password")