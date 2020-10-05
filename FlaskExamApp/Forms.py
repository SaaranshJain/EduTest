from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField , SelectField , DateTimeField
from wtforms.validators import DataRequired , Length , Email , EqualTo

subjects = [
    ("Mathematics" , "Mathematics") , 
    ("Physics" , "Physics") , 
    ("Chemistry" , "Chemistry") , 
    ("English" , "English") , 
    ("Computer" , "Computer") , 
    ("Biology" , "Biology") , 
    ("PE" , "PE") , 
    ("Entrepreneurship" , "Entrepreneurship") , 
    ("Psychology" , "Psychology") , 
    ("Business Studies" , "Business Studies") , 
    ("Accountancy" , "Accountancy")
    ]

class RegistrationForm(FlaskForm) :
    name = StringField("Student Name" , validators=[DataRequired() , Length(min=2 , max=20)])
    email = StringField("School Email" , validators=[DataRequired() , Email()])
    password = PasswordField("Password" , validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password" , validators=[DataRequired() , EqualTo("password")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm) :
    email = StringField("School Email" , validators=[DataRequired() , Email()])
    password = PasswordField("Password" , validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class CreateSingle(FlaskForm) :
    subject = SelectField(label="Subject" , choices=subjects , validators=[DataRequired()])
    title = StringField("Title" , validators=[DataRequired()])
    date = DateTimeField("Date of the exam" , validators=[DataRequired()])
    submit = SubmitField("Create")