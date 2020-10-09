from flask import Blueprint , redirect , url_for , render_template , request
from FlaskExamApp.Models import Exam
from datetime import datetime
from flask_login import login_required
from flask import flash
from FlaskExamApp import db

main = Blueprint("main" , __name__)

@main.route("/")
def red() :
    return redirect(url_for("main.home"))

@main.route("/1011011100")
def home() :
    # db.drop_all()
    # db.create_all()
    page = request.args.get("page" , 1 , type=int)
    exams = Exam.query.order_by(Exam.date_of_exam.asc()).paginate(page=page , per_page=7)
    for exam in exams.items :
        if str(exam.date_of_exam) <= str(datetime.now())[:10] or (str(exam.date_of_exam) <= str(datetime.now())[:10] and str(exam.end_time) <= str(datetime.now())[11:-7]) :
            db.session.delete(exam)
            db.session.commit()
    return render_template("Home.html" , exams=exams , Title="Exam Overview" , datetime=datetime , str=str)

@main.route("/about")
@login_required
def about() :
    return render_template("About.html" , Title="About Us")