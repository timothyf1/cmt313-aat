from flask_sqlalchemy import SQLAlchemy
from aat.aat import app, db
import abc


# Tables for many to many relationships links
module_user = db.Table(
    'module_user',
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("module_id", db.Integer, db.ForeignKey('module.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    user_type = db.Column(db.String)

    modules = db.relationship(
        'Module',
        secondary=module_user,
        back_populates='user'
    )

    __mapper_args__ = {
        "polymorphic_on": "user_type",
        "polymorphic_identity": "user",
    }


class Student(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    course = db.Column(db.String)
    cohort = db.Column(db.Integer)

    submissions = db.relationship(
        "Submission",
        back_populates = "student"
    )

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }


class Staff(User):
    id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    position = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "staff",
    }


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    code = db.Column(db.String, unique=True)

    user = db.relationship(
        'User',
        secondary=module_user,
        back_populates='modules'
    )

    assignments = db.relationship(
        'Assignment',
        back_populates="module"
    )

    def get_students(self):
        return [user for user in self.user if user.user_type == "student"]

    def get_staff(self):
        return [user for user in self.user if user.user_type == "staff"]


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"))
    assignment_type = db.Column(db.String)
    active = db.Column(db.Boolean)

    module = db.relationship(
        "Module",
        back_populates="assignments"
    )

    question_assignment = db.relationship(
        "AssignQuestion",
        back_populates = "assignment",
        order_by = "AssignQuestion.question_number.asc()"
    )

    submissions = db.relationship(
        "Submission",
        back_populates = "assignment"
    )

    __mapper_args__ = {
        "polymorphic_on": "assignment_type",
        "polymorphic_identity": "assignment",
    }

    def get_questions(self):
        return dict([(item.question_number, item.question) for item in self.question_assignment])

    def add_question(self, question, question_no):
        print(self.id, question, question_no)
        return AssignQuestion.add_question(self.id, question.id, question_no)


class FormativeAssignment(Assignment):
    id = db.Column(db.Integer, db.ForeignKey("assignment.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "formative_assignment",
    }


class SummativeAssignment(Assignment):
    id = db.Column(db.Integer, db.ForeignKey("assignment.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "summative_assignment",
    }


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"))
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))

    attempt_number = db.Column(db.Integer)
    mark = db.Column(db.Integer)

    assignment = db.relationship(
        "Assignment",
        back_populates = "submissions"
    )

    student = db.relationship(
        "Student",
        back_populates = "submissions"
    )


class AssignQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    question_number = db.Column(db.Integer)

    assignment = db.relationship(
        "Assignment",
        back_populates = "question_assignment"
    )

    question = db.relationship(
        "Question",
        back_populates = "question_assignment"
    )

    @staticmethod
    def get_assignment_questions(assignment_id):
        assign = AssignQuestion.query.filter_by(assignment_id=assignment_id).order_by(AssignQuestion.question_number.asc()).all()
        questions = dict([(item.question_number, item.question) for item in assign])
        return questions

    @staticmethod
    def get_question_assignments(question_id):
        assign = AssignQuestion.query.filter_by(question_id=question_id).all()
        assignments = [item.assignment for item in assign]
        return assignments

    @staticmethod
    def add_question(assignment_id, question_id, question_number):
        print(assignment_id, question_id, question_number)
        assign = AssignQuestion(
            assignment_id = assignment_id,
            question_id = question_id,
            question_number = question_number
        )
        db.session.add(assign)
        db.session.commit()


# https://stackoverflow.com/a/28727066/
class QuestionMeta(type(db.Model), type(abc.ABC)):
    pass


class Question(db.Model, abc.ABC, metaclass=QuestionMeta):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    question_type = db.Column(db.String)
    active = db.Column(db.Boolean)

    question_assignment = db.relationship(
        "AssignQuestion",
        back_populates = "question"
    )

    __mapper_args__ = {
        "polymorphic_on": "question_type",
        "polymorphic_identity": "question",
    }

    @abc.abstractmethod
    def mark(self):
        pass

    def get_assignments(self):
        return [item.assignment for item in self.question_assignment]


class QuestionType1(Question):
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    question_text = db.Column(db.String)
    option1 = db.Column(db.String)
    option2 = db.Column(db.String)
    option3 = db.Column(db.String)
    option4 = db.Column(db.String)
    correctOption = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "question_type1",
    }

    def mark(self):
        return 0


class QuestionType2(Question):
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    question_text = db.Column(db.String)

    answer = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": "question_type2",
    }

    def mark(self):
        return 0
