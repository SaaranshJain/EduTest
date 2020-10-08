from FlaskExamApp.Variables import subjects , classes
from wtforms import StringField , SubmitField , SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

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