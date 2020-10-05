from flask import render_template , url_for , flash , redirect
from FlaskExamApp.Forms import RegistrationForm , LoginForm , CreateSingle
from FlaskExamApp.Models import User , Exam
from FlaskExamApp import app

portions = [
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
        "date_of_exam" : "October 7, 2020"
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
        "date_of_exam" : "October 9, 2020"
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
        "date_of_exam" : "October 12, 2020"
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
        "date_of_exam" : "October 17, 2020"
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
        "date_of_exam" : "October 20, 2020"
    }
]

@app.route("/")
def home() :
    return render_template("Home.html" , posts=portions , Title="Exam Overview")

@app.route("/about")
def about() :
    return render_template("About.html" , Title="About Us")

@app.route("/register" , methods=['GET' , 'POST'])
def register() :
    form_reg = RegistrationForm()
    if form_reg.validate_on_submit() :
        print("Hiiiii")
        flash(f"Account created for {form_reg.name.data}!" , category="success")
        return redirect(url_for("login"))
    return render_template("Register.html" , Title="Register" , form = form_reg)

@app.route("/login" , methods=['GET' , 'POST'])
def login() :
    form_log = LoginForm()
    if form_log.validate_on_submit() :
        # Dummy success condition
        if form_log.email.data == "admin@blog.com" and form_log.password.data == "password" :
            flash("You have been logged in!" , "success")
            return redirect(url_for("home"))
        else :
            flash("Login failed" , "danger")
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