from FlaskExamApp.Variables import subjects , classes
from wtforms import StringField , SubmitField , SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms_components import TimeField

class CreateSingle(FlaskForm) :
    subject = SelectField(label="Subject" , choices=subjects , validators=[DataRequired()])
    title = StringField("Title" , validators=[DataRequired()])
    date = DateField("Date of the exam" , validators=[DataRequired()] , format="%Y-%m-%d")
    start_time = TimeField("Start Time" , validators=[DataRequired()])
    end_time = TimeField("End Time" , validators=[DataRequired()])
    grade = SelectField(label="Grade" , choices=classes , validators=[DataRequired()])
    submit = SubmitField("Create")

class UpdateDelete(FlaskForm) :
    subject = SelectField(label="Subject" , choices=subjects , validators=[DataRequired()])
    title = StringField("Title" , validators=[DataRequired()])
    date = DateField("Date of the exam" , validators=[DataRequired()] , format="%Y-%m-%d")
    grade = SelectField(label="Grade" , choices=classes , validators=[DataRequired()])
    submit = SubmitField("Update")
    delete = SubmitField("Delete")