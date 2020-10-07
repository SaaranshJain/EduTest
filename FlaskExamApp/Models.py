from FlaskExamApp import db , login_manager , app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id) :
    return User.query.get(int(user_id))

class User(db.Model , UserMixin) :
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(20) , unique=True , nullable=False)
    email = db.Column(db.String(80) , unique=True , nullable=False)
    image_file = db.Column(db.String(120) , nullable=False , default="default.jpg")
    password = db.Column(db.String(60) , nullable=False)

    def get_reset_token(self , expires_secs=600) :
        s = Serializer(app.config["SECRET_KEY"] , expires_secs)
        return s.dumps({'user_id' : self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token) :
        s = Serializer(app.config["SECRET_KEY"])
        try :
            user_id = s.loads(token)["user_id"]
        except :
            return None
        return User.query.get(user_id)

    def __repr__(self) :
        return f"User('{self.name} , {self.email} , {self.image_file}')"

class Exam(db.Model) :
    id = db.Column(db.Integer , primary_key=True)
    subject = db.Column(db.String , nullable=False)
    title = db.Column(db.String(100) , nullable=False)
    date_of_exam = db.Column(db.DateTime , nullable=False , default=datetime.utcnow)
    portions = db.Column(db.Text , nullable=False)

    def __repr__(self) :
        return f"Post('{self.title} , {self.date_of_exam} , {self.subject}')"