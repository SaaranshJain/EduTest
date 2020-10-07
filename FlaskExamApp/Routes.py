from flask import render_template , url_for , flash , redirect , request
from FlaskExamApp.Forms import (RegistrationForm , LoginForm , CreateSingle , UpdateAccForm ,
                                UpdateDelete , RequestResetForm , ResetPasswordForm)
from FlaskExamApp.Models import User , Exam
from FlaskExamApp import app , db , bcrypt , mail
from flask_login import login_user , current_user , logout_user , login_required
from flask_mail import Message
from datetime import datetime
import secrets
import os
from PIL import Image

@app.route("/1011011100")
def home() :
    page = request.args.get("page" , 1 , type=int)
    exams = Exam.query.order_by(Exam.date_of_exam.asc()).paginate(page=page , per_page=7)
    return render_template("Home.html" , exams=exams , Title="Exam Overview" , datetime=datetime , str=str)

@app.route("/about")
@login_required
def about() :
    return render_template("About.html" , Title="About Us")

@app.route("/1011011100/register" , methods=['GET' , 'POST'])
def register() :
    if current_user.is_authenticated :
        return redirect(url_for("home"))
    form_reg = RegistrationForm()
    if form_reg.validate_on_submit() :
        hashed_pass = bcrypt.generate_password_hash(form_reg.password.data).decode("utf-8")
        user = User(name=form_reg.name.data , email=form_reg.email.data , password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form_reg.name.data}!" , category="success")
        return redirect(url_for("login"))
    return render_template("Register.html" , Title="Register" , form = form_reg)

@app.route("/login" , methods=['GET' , 'POST'])
def login() :
    if current_user.is_authenticated :
        return redirect(url_for("home"))
    form_log = LoginForm()
    if form_log.validate_on_submit() :
        user = User.query.filter_by(email=form_log.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form_log.password.data) :
            login_user(user , remember=form_log.remember.data)
            next_page = request.args.get("next")
            flash("Login successful!!" , "success")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else :
            flash("Login failed!!" , "danger")
    return render_template("Login.html" , Title="Login" , form = form_log)

@app.route("/logout")
def logout() :
    logout_user()
    flash("Succesfully logged out!!" , category="success")
    return redirect(url_for("home"))

def savepic(pic) :
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path , "static/Profile_Pics" , pic_fn)
    i = Image.open(pic)
    i.thumbnail((125 , 125))
    i.save(pic_path)
    return pic_fn


@app.route("/account" , methods=['GET' , 'POST'])
@login_required
def account() :
    form_acc = UpdateAccForm()
    if form_acc.validate_on_submit() :
        if form_acc.pic.data :
            pic_file = savepic(form_acc.pic.data)
            current_user.image_file = pic_file
        current_user.name = form_acc.name.data
        current_user.email = form_acc.email.data
        db.session.commit()
        flash("Your account has successfully been updated!" , category="success")
        return redirect(url_for("account"))
    elif request.method == "GET" :
        form_acc.name.data = current_user.name
        form_acc.email.data = current_user.email
    image = url_for("static" , filename="Profile_Pics/" + current_user.image_file)
    return render_template("Account.html" , title="User Profile" , image=image , form=form_acc)

@app.route("/1011011100/create" , methods=["GET" , "POST"])
@login_required
def createsingle() :
    form_createsingle = CreateSingle()
    if form_createsingle.validate_on_submit() :
        exam = Exam(subject=form_createsingle.subject.data , title=form_createsingle.title.data , date_of_exam=form_createsingle.date.data , portions="Portions : \n\n" + form_createsingle.title.data)
        db.session.add(exam)
        db.session.commit()
        method_of_upload = "Create"
        flash("The exam has been created!!" , category="success")
        return redirect(url_for("home"))
    return render_template("CreateSingle.html" , Title="Create" , form=form_createsingle , legend="New Post")

@app.route("/calendar")
@login_required
def calendar() :
    return "Calendar"

@app.route("/1011011100/createseries")
@login_required
def createseries() :
    return "Series"

@app.route("/1011011100/exams/<int:exam_id>/update" , methods=["GET" , "POST"])
@login_required
def edit_exam(exam_id) :
    exam = Exam.query.get_or_404(exam_id)
    form_update = UpdateDelete()
    if form_update.validate_on_submit() :
        exam.title = form_update.title.data
        exam.subject = form_update.subject.data
        exam.date_of_exam = form_update.date.data
        method_of_upload = "Update"
        # exam.portions = form_update.portions.data
        db.session.commit()
        flash("The exam has been updated!!" , category="success")
        return redirect(url_for("home"))
    elif request.method == "GET" :
        form_update.title.data = exam.title
        form_update.subject.data = exam.subject
        method_of_upload = "Update"
        form_update.date.data = exam.date_of_exam
        # form_update.portions.data = exam.portions

    return render_template("UpdateDelete.html" , Title="Update Exam" , form=form_update , legend="Update Exam" , exam=exam)

@app.route("/1011011100/exams/<int:exam_id>/delete" , methods=["POST"])
@login_required
def delete_exam(exam_id) :
    exam = Exam.query.get_or_404(exam_id)
    db.session.delete(exam)
    db.session.commit()
    flash("The exam has been deleted!!" , category="success")
    return redirect(url_for("home"))

def send_email(user) :
    token = user.get_reset_token()
    msg = Message("Password Reset Request" , sender="edtest.noreply@gmail.com" , recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link :
    {url_for("reset_password" , token=token , _external=True)}
    If you did not make this request, then simply ignore this email and nothing will be changed!
    '''
    mail.send(msg)

@app.route("/reset_password" , methods=["GET" , "POST"])
def reset_request() :
    if current_user.is_authenticated :
        return redirect(url_for("home"))
    form_reset = RequestResetForm()
    if form_reset.validate_on_submit() :
        user = User.query.filter_by(email=form_reset.email.data).first()
        send_email(user)
        flash("An email has been sent with instructions" , category="info")
        return redirect(url_for("login"))
    return render_template("Request_Reset.html" , title="Reset Password" , form=form_reset)

@app.route("/reset_password/<token>" , methods=["GET" , "POST"])
def reset_password(token) :
    if current_user.is_authenticated :
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if not user :
        flash("Password reset timed out/invalid. Please try again!" , category="warning")
        return redirect(url_for("reset_request"))
    form_reset_new = ResetPasswordForm()
    if form_reset_new.validate_on_submit() :
        hashed_pass = bcrypt.generate_password_hash(form_reset_new.password.data).decode("utf-8")
        user.password = hashed_pass
        db.session.commit()
        flash("Your password has been updated!" , category="success")
        return redirect(url_for("login"))
    return render_template("Token_Reset.html" , title="Reset Password" , form=form_reset_new)