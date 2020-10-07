from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms import StringField , PasswordField , SubmitField , BooleanField , SelectField
from wtforms.fields.html5 import DateTimeField , DateField
from wtforms.validators import DataRequired , Length , Email , EqualTo
from FlaskExamApp.Models import User
from wtforms.validators import ValidationError
from flask_login import current_user
from FlaskExamApp.Variables import subjects

classes = [(f"Grade {i}" , f"Grade {i}") for i in range(11 , 13)]

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

class CreateSingle(FlaskForm) :
    subject = SelectField(label="Subject" , choices=subjects , validators=[DataRequired()])
    title = StringField("Title" , validators=[DataRequired()])
    date = DateField("Date of the exam" , validators=[DataRequired()] , format="%Y-%m-%d")
    grade = SelectField(label="Grade" , choices=classes , validators=[DataRequired()])
    submit = SubmitField("Create")

class UpdateDelete(FlaskForm) :
    subject = SelectField(label="Subject" , choices=subjects , validators=[DataRequired()])
    title = StringField("Title" , validators=[DataRequired()])
    date = DateField("Date of the exam" , validators=[DataRequired()] , format="%Y-%m-%d")
    grade = SelectField(label="Grade" , choices=classes , validators=[DataRequired()])
    submit = SubmitField("Update")
    delete = SubmitField("Delete")