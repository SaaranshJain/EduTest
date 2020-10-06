from flask import render_template , url_for , flash , redirect , request
from FlaskExamApp.Forms import RegistrationForm , LoginForm , CreateSingle , UpdateAccForm
from FlaskExamApp.Models import User , Exam
from FlaskExamApp import app , db , bcrypt
from flask_login import login_user , current_user , logout_user , login_required
from datetime import datetime

exams = [
    {
        "subject" : "English",
        "title" : "Midterm Exam",
        "portions" : '''Portions :

        01. The Portrait of a Lady
        02. A Photograph, We're not Afraid to Die....
        03. Discovering Tut: The Saga Continues
        04. The Laburnum Top
        05. Landscape of the soul
        06. The Voice of the Rain
        07. The Summer of the Beautiful White Horse
        08. The Address
        09. Ranga's Mariage
        10. Albert Einstein at School
        11. Integrated grammar
        12. Formal letters
        13. Article Writing
        14. Note making''',
        "date_of_exam" : "2020-10-07"
    },
    {
        "subject" : "Computer",
        "title" : "Midterm Exam",
        "portions" : '''Portions : 

        01. Getting started with python.
        02. Python fundamentals.
        03. Data Handling.
        04. Conditional and iterative statements.
        05. String Manipulation.
        06. List Manipulation.
        07. Tuples.
        08. Computer system overview
        09. Data Representation.''',
        "date_of_exam" : "2020-10-09"
    },
    {
        "subject" : "Math",
        "title" : "Midterm Exam",
        "portions" : '''Portions :

        01. Sets
        02. Relations & Functions
        03. Trigonometric Functions  
        04. Complex Numbers & Quadratic Equations
        05. Linear Inequalities
        06. Sequences & Series
        07. Permutations & Combinations''',
        "date_of_exam" : "2020-10-12"
    },
    {
        "subject" : "Physics",
        "title" : "Midterm Exam",
        "portions" : '''Portions :

        02. Units and Measurements 
        03. Motion in a straight line
        04. Motion in a plane
        05. Laws of motion
        06. Work,Energy and Power
        07. Motion of system of particles''',
        "date_of_exam" : "2020-10-17"
    },
    {
        "subject" : "Chemistry",
        "title" : "Midterm Exam",
        "portions" : '''Portions :

        01. Some basic concepts in Chemistry
        02. Structure of atom
        03. Classification of elements and periodicity in properties
        04. Chemical bonding
        05. Thermodynamics
        06. Chemical Equilibrium
        07. Hydrogen''',
        "date_of_exam" : "2020-10-20"
    }
]

@app.route("/")
def home() :
    return render_template("Home.html" , posts=exams , Title="Exam Overview" , datetime=datetime , str=str)

@app.route("/about")
def about() :
    return render_template("About.html" , Title="About Us")

@app.route("/register" , methods=['GET' , 'POST'])
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

@app.route("/create")
def createsingle() :
    form_createsingle = CreateSingle()
    return render_template("CreateSingle.html" , Title="Create" , form = form_createsingle)

@app.route("/calendar")
def calendar() :
    return "Calendar"

@app.route("/createseries")
def createseries() :
    return "Series"

@app.route("/logout")
def logout() :
    logout_user()
    flash("Succesfully logged out!!" , category="success")
    return redirect(url_for("home"))

@app.route("/account" , methods=['GET' , 'POST'])
@login_required
def account() :
    form_acc = UpdateAccForm()
    if form_acc.validate_on_submit() :
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