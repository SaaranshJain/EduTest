from flask import Blueprint , redirect , url_for , render_template , flash , request
from flask_login import current_user , login_user , logout_user , login_required
from FlaskExamApp import db , bcrypt
from FlaskExamApp.Models import User
from FlaskExamApp.users.Forms import RegistrationForm , RequestResetForm , ResetPasswordForm , LoginForm , UpdateAccForm
from FlaskExamApp.users.utils import savepic , send_email

users = Blueprint("users" , __name__)

@users.route("/1011011100/register" , methods=['GET' , 'POST'])
def register() :
    if current_user.is_authenticated :
        return redirect(url_for("main.home"))
    form_reg = RegistrationForm()
    if form_reg.validate_on_submit() :
        hashed_pass = bcrypt.generate_password_hash(form_reg.password.data).decode("utf-8")
        user = User(name=form_reg.name.data , email=form_reg.email.data , password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form_reg.name.data}!" , category="success")
        return redirect(url_for("users.login"))
    return render_template("Register.html" , Title="Register" , form = form_reg)

@users.route("/login" , methods=['GET' , 'POST'])
def login() :
    if current_user.is_authenticated :
        return redirect(url_for("main.home"))
    form_log = LoginForm()
    if form_log.validate_on_submit() :
        user = User.query.filter_by(email=form_log.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form_log.password.data) :
            login_user(user , remember=form_log.remember.data)
            next_page = request.args.get("next")
            flash("Login successful!!" , "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else :
            flash("Login failed!!" , "danger")
    return render_template("Login.html" , Title="Login" , form = form_log)

@users.route("/logout")
def logout() :
    logout_user()
    flash("Succesfully logged out!!" , category="success")
    return redirect(url_for("main.home"))

@users.route("/account" , methods=['GET' , 'POST'])
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
        return redirect(url_for("users.account"))
    elif request.method == "GET" :
        form_acc.name.data = current_user.name
        form_acc.email.data = current_user.email
    image = url_for("static" , filename="Profile_Pics/" + current_user.image_file)
    return render_template("Account.html" , title="User Profile" , image=image , form=form_acc)

@users.route("/reset_password" , methods=["GET" , "POST"])
def reset_request() :
    if current_user.is_authenticated :
        return redirect(url_for("main.home"))
    form_reset = RequestResetForm()
    if form_reset.validate_on_submit() :
        user = User.query.filter_by(email=form_reset.email.data).first()
        send_email(user)
        flash("An email has been sent with instructions" , category="info")
        return redirect(url_for("users.login"))
    return render_template("Request_Reset.html" , title="Reset Password" , form=form_reset)

@users.route("/reset_password/<token>" , methods=["GET" , "POST"])
def reset_password(token) :
    if current_user.is_authenticated :
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user :
        flash("Password reset timed out/invalid. Please try again!" , category="warning")
        return redirect(url_for("users.reset_request"))
    form_reset_new = ResetPasswordForm()
    if form_reset_new.validate_on_submit() :
        hashed_pass = bcrypt.generate_password_hash(form_reset_new.password.data).decode("utf-8")
        user.password = hashed_pass
        db.session.commit()
        flash("Your password has been updated!" , category="success")
        return redirect(url_for("users.login"))
    return render_template("Token_Reset.html" , title="Reset Password" , form=form_reset_new)