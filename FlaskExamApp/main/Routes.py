from FlaskExamApp.users.utils import locked
from flask import Blueprint , redirect , url_for , render_template , request
from FlaskExamApp.Models import Exam
from datetime import datetime
from flask_login import login_required
from FlaskExamApp import db
from flask_login import current_user

main = Blueprint("main" , __name__)

@main.route("/")
@login_required
def red() :
    db.session.commit()
    if current_user.kind == "Student" :
        return redirect(url_for("main.student_home"))
    return redirect(url_for("main.teacher_home"))

@main.route("/1011011100")
@login_required
@locked
def teacher_home() :
    # db.drop_all()
    # db.create_all()
    page = request.args.get("page" , 1 , type=int)
    exams = Exam.query.order_by(Exam.date_of_exam.asc()).paginate(page=page , per_page=7)
    for exam in exams.items :
        print(exam.questions)
        if str(exam.date_of_exam) <= str(datetime.now())[:10] or (str(exam.date_of_exam) <= str(datetime.now())[:10] and str(exam.end_time) <= str(datetime.now())[11:-7]) :
            db.session.delete(exam)
            db.session.commit()
    return render_template("teacher_home.html" , exams=exams , Title="Exam Overview" , datetime=datetime , str=str)

@main.route("/1101111010")
@login_required
def student_home() :
    page = request.args.get("page" , 1 , type=int)
    exams = Exam.query.order_by(Exam.date_of_exam.asc()).paginate(page=page , per_page=7)
    for exam in exams.items :
        print(exam.questions)
        if str(exam.date_of_exam) <= str(datetime.now())[:10] or (str(exam.date_of_exam) <= str(datetime.now())[:10] and str(exam.end_time) <= str(datetime.now())[11:-7]) :
            db.session.delete(exam)
            db.session.commit()
    return render_template("student_home.html" , exams=exams , Title="Exam Overview" , datetime=datetime , str=str)

@main.route("/about")
@login_required
def about() :
    return render_template("About.html" , Title="About Us")