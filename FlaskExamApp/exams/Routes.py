from flask import Blueprint , flash , render_template , redirect , url_for , request
from FlaskExamApp.exams.Forms import CreateSingle , UpdateDelete
from FlaskExamApp.Models import Exam
from FlaskExamApp import db
from flask_login import login_required
from datetime import datetime

exams = Blueprint("exams" , __name__)

@exams.route("/1011011100/create" , methods=["GET" , "POST"])
@login_required
def createsingle() :
    form_createsingle = CreateSingle()
    if form_createsingle.validate_on_submit() :
        exam = Exam(subject=form_createsingle.subject.data , title=form_createsingle.title.data , date_of_exam=form_createsingle.date.data , start_time=str(form_createsingle.start_time.data) , end_time=str(form_createsingle.end_time.data) , portions="Portions : \n\n" + form_createsingle.title.data)
        if str(exam.date_of_exam) < str(datetime.now())[:10] or (str(exam.date_of_exam) < str(datetime.now())[:10] and str(exam.end_time) < str(datetime.now())[11:-7]) :
            flash("The exam was not created since you need to select a proper date and time" , category="warning")
        else :
            db.session.add(exam)
            db.session.commit()
            method_of_upload = "Create"
            flash("The exam has been created!!" , category="success")
            return redirect(url_for("main.home"))
    return render_template("CreateSingle.html" , Title="Create" , form=form_createsingle , legend="New Exam")

@exams.route("/1011011100/calendar")
@login_required
def calendar() :
    return "Calendar"

@exams.route("/1011011100/createseries")
@login_required
def createseries() :
    return "Series"

@exams.route("/1011011100/exams/<int:exam_id>/update" , methods=["GET" , "POST"])
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
        return redirect(url_for("main.home"))
    elif request.method == "GET" :
        form_update.title.data = exam.title
        form_update.subject.data = exam.subject
        method_of_upload = "Update"
        form_update.date.data = exam.date_of_exam
        # form_update.portions.data = exam.portions

    return render_template("UpdateDelete.html" , Title="Update Exam" , form=form_update , legend="Update Exam" , exam=exam)

@exams.route("/1011011100/exams/<int:exam_id>/delete" , methods=["POST"])
@login_required
def delete_exam(exam_id) :
    exam = Exam.query.get_or_404(exam_id)
    # db.drop_all()
    # db.create_all()
    db.session.delete(exam)
    db.session.commit()
    flash("The exam has been deleted!!" , category="success")
    return redirect(url_for("main.home"))
