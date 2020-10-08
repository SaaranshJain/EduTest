import secrets
import os
from PIL import Image
from flask_mail import Message
from flask import url_for , current_app
from FlaskExamApp import mail

def savepic(pic) :
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path , "static/Profile_Pics" , pic_fn)
    i = Image.open(pic)
    i.thumbnail((125 , 125))
    i.save(pic_path)
    return pic_fn

def send_email(user) :
    token = user.get_reset_token()
    msg = Message("Password Reset Request" , sender="edtest.noreply@gmail.com" , recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link :
    {url_for("users.reset_password" , token=token , _external=True)}
    If you did not make this request, then simply ignore this email and nothing will be changed!
    '''
    mail.send(msg)