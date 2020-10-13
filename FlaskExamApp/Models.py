from FlaskExamApp import db , login_manager
from datetime import datetime
from flask_login import UserMixin as UserMixinLogin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_user import UserManager
from flask_user import UserMixin as UserMixinUser

@login_manager.user_loader
def load_user(user_id) :
    return User.query.get(int(user_id))

class User(db.Model , UserMixinUser , UserMixinLogin) :
    __tablename__ = 'users'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(5) , unique=True , nullable=False)
    kind = db.Column(db.String() , unique=False , nullable=False)
    email = db.Column(db.String(30) , unique=True , nullable=False)
    image_file = db.Column(db.String(120) , nullable=False , default="default.jpg")
    password = db.Column(db.String(60) , nullable=False)
    roles = db.relationship('Role', secondary='user_roles')

    def get_reset_token(self , expires_secs=600) :
        s = Serializer(current_app.config["SECRET_KEY"] , expires_secs)
        return s.dumps({'user_id' : self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token) :
        s = Serializer(current_app.config["SECRET_KEY"])
        try :
            user_id = s.loads(token)["user_id"]
        except :
            return None
        return User.query.get(user_id)
        
    def __repr__(self) :
        return f"User('{self.name} , {self.email} , {self.image_file}')"

user_manager = UserManager(current_app , db , User)

class Exam(db.Model) :
    id = db.Column(db.Integer , primary_key=True)
    subject = db.Column(db.String , nullable=False)
    title = db.Column(db.String(100) , nullable=False)
    date_of_exam = db.Column(db.DateTime , nullable=False , default=datetime.utcnow)
    start_time = db.Column(db.String(2) , nullable=False)
    end_time = db.Column(db.String(2) , nullable=False)
    duration = db.Column(db.String(2) , nullable=False)
    portions = db.Column(db.Text , nullable=False)
    questions = db.Column(db.String(120))

    def __repr__(self) :
        return f"Exam('{self.title} , {self.date_of_exam} , {self.subject}')"

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))