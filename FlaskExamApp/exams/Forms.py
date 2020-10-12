from FlaskExamApp.Variables import subjects11_12 , classes
from wtforms import StringField , SubmitField , SelectField
from wtforms.fields.html5 import DateField , IntegerField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms_components import TimeField

class CreateSingle(FlaskForm) :
    subject = SelectField(label="Subject" , choices=subjects11_12 , validators=[DataRequired()])
    title = StringField("Title" , validators=[DataRequired()])
    date = DateField("Date of the exam" , validators=[DataRequired()] , format="%Y-%m-%d")
    start_time = TimeField("Start Time" , validators=[DataRequired()])
    end_time = TimeField("End Time" , validators=[DataRequired()])
    duration = TimeField("Duration of the exam" , validators=[DataRequired()])
    grade = SelectField(label="Grade" , choices=classes , validators=[DataRequired()])
    questions = FileField("Upload questions template" , validators=[FileAllowed(["docx" , "txt"])])
    submit = SubmitField("Create")

class UpdateDelete(FlaskForm) :
    subject = SelectField(label="Subject" , choices=subjects11_12 , validators=[DataRequired()])
    title = StringField("Title" , validators=[DataRequired()])
    date = DateField("Date of the exam" , validators=[DataRequired()] , format="%Y-%m-%d")
    grade = SelectField(label="Grade" , choices=classes , validators=[DataRequired()])
    submit = SubmitField("Update")
    delete = SubmitField("Delete")