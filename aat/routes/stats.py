from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from .. import app, db
from ..models import Assignment, Question, QuestionType1, QuestionType2

@app.route('/staff/question/<int:id>/stats')
@login_required
def question_stats(id):
    if current_user.user_type != "staff":
        abort(403, description="This page can only be accessed by staff.")

    question = Question.query.filter_by(id=id).first_or_404()

    match question.question_type:
        case "question_type1":
            return render_template('stats/question_type1.html', title=question.title, question=question)

        case "question_type2":
            return render_template('stats/question_type2.html', title=question.title, question=question)

    abort(500)

@app.route('/staff/assessment/<int:id>/stats')
@login_required
def assessment_stats(id):
    if current_user.user_type != "staff":
        abort(403, description="This page can only be accessed by staff.")

    assignment = Assignment.query.filter_by(id=id).first_or_404()

    match assignment.assignment_type:
        case "formative_assignment":
            return render_template('stats/formative_assignment_stats.html', title=assignment.title, assignment=assignment)

        case "summative_assignment":
            abort(501)

    abort(500)

@app.route('/staff/assessment/<int:id>/stats/<int:question_num>')
@login_required
def assessment_question_stats(id, question_num):
    if current_user.user_type != "staff":
        abort(403, description="This page can only be accessed by staff.")

    assignment = Assignment.query.filter_by(id=id).first_or_404()

    question = assignment.get_questions()[question_num]

    match question.question_type:
        case "question_type1":
            return render_template('stats/assignment_question_type1.html', title=assignment.title, assignment=assignment, question=question, question_number=question_num)

        case "question_type2":
            return render_template('stats/assignment_question_type2.html', title=assignment.title, assignment=assignment, question=question, question_number=question_num)

    abort(500)
