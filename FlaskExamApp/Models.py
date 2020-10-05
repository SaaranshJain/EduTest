from FlaskExamApp import db
from datetime import datetime

class User(db.Model) :
    Id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(20) , unique=True , nullable=False)
    email = db.Column(db.String(80) , unique=True , nullable=False)
    image_file = db.Column(db.String(120) , nullable=False , default="default.jpg")
    password = db.Column(db.String(60) , nullable=False)

    def __repr__(self) :
        return f"User('{self.name} , {self.email} , {self.image_file}')"

class Exam(db.Model) :
    Id = db.Column(db.Integer , primary_key=True)
    subject = db.Column(db.String , nullable=True)
    title = db.Column(db.String(100) , nullable=False)
    date_of_exam = db.Column(db.DateTime , nullable=False , default=datetime.utcnow)
    portions = db.Column(db.Text , nullable=False)

    def __repr__(self) :
        return f"Post('{self.title} , {self.date_of_exam} , {self.subject}')"