from . import db
from .models import *

try:
    student1 = Student(
        username = "leia",
        password = "alpha",
        email = "c@example.com",
        first_name = "Leia",
        surname = "Beasley",
        cohort = 2013,
        course = "computing",
    )
    db.session.add(student1)

    student2 = Student(
        username = "priya",
        password = "alpha",
        email = "d@example.com",
        first_name = "Priya",
        surname = "Bishop",
        cohort = 2013,
        course = "computing"
    )
    db.session.add(student2)

    student3 = Student(
        username = "elliot",
        password = "alpha",
        email = "e@example.com",
        first_name = "Elliot",
        surname = "Hull",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student3)

    student4 = Student(
        username = "nathaniel",
        password = "alpha",
        email = "f@example.com",
        first_name = "Nathaniel",
        surname = "Moore",
        cohort = 2014,
        course = "computing"
    )
    db.session.add(student4)

    staff1 = Staff(
        username = "elena",
        password = "alpha",
        email = "a@example.com",
        first_name = "Elena",
        surname = "Thomas",
        position = "Lect"
    )
    db.session.add(staff1)

    staff2 = Staff(
        username = "oakley",
        password = "alpha",
        email = "b@example.com",
        first_name = "Oakley",
        surname = "Bender",
        position = "Lect"
    )
    db.session.add(staff2)

    module1 = Module(
        name = "Programming",
        code = "COMP1-2",
        user = [student1, student2, student3, staff1, staff2]
    )
    db.session.add(module1)

    module2 = Module(
        name = "Computer systems",
        code = "COMP2-8",
        user = [student1, student2, student4, staff1]
    )
    db.session.add(module2)

    module3 = Module(
        name = "The Internet",
        code = "COMP2-9",
        user = [student1, student2, student4, staff1]
    )
    db.session.add(module3)

    q1 = QuestionType1(
        title = "Code 1",
        active = True,
        question_template = "A {} language program is called {} code.",
        correct_answers = "['high-level', ' source']",
        incorrect_answers = "['high', 'low', 'low-level', 'machine', 'object', 'assembly']"
    )
    db.session.add(q1)

    q2 = QuestionType1(
        title = "Code 2",
        active = True,
        question_template = "A {} translates source code into {} code.",
        correct_answers = "['compiler', ' object']",
        incorrect_answers = "['interpreter', 'assemblers', 'executes', 'machine', 'source']"
    )
    db.session.add(q2)

    q3 = QuestionType1(
        title = "Code 3",
        active = True,
        question_template = "An {} analyses each {} of the {} code as it {} the statement.",
        correct_answers = "['interpreter', 'statement', 'source, 'executes']",
        incorrect_answers = "['compiler', 'assemblers', 'machine', 'object', 'assembly', 'line']"
    )
    db.session.add(q3)

    q4 = QuestionType2(
        title = "hi2"
    )
    db.session.add(q4)

    q5 = QuestionType2(
        title = "hello2"
    )
    db.session.add(q5)

    q6 = QuestionType2(
        title = "world2"
    )
    db.session.add(q6)

    assignment1 = SummativeAssignment(
        title = "Procedures and functions",
        module = module1,
        active = True
    )
    db.session.add(assignment1)

    assignment2 = SummativeAssignment(
        title = "Hardware devices",
        module = module2,
        active = True
    )
    db.session.add(assignment2)

    assignment3 = SummativeAssignment(
        title = "Web site design",
        module = module3,
        active = True
    )
    db.session.add(assignment3)

    assignment4 = FormativeAssignment(
        title = "Classification of software",
        module = module2,
        active = True
    )
    db.session.add(assignment4)

    assignment5 = FormativeAssignment(
        title = "Structure of the Internet",
        module = module3,
        active = True
    )
    db.session.add(assignment5)

    assignment6 = FormativeAssignment(
        title = "Data types",
        module = module1,
        active = True
    )
    db.session.add(assignment6)

    db.session.commit()

    assignment4.add_question(q1, 1)
    assignment4.add_question(q2, 3)
    assignment4.add_question(q3, 2)

    db.session.commit()
except:
    print('''
Tried to populate the database with test data but an error occured.
This is likely because data already exists.
To avoid this error please disable the line which includes 'create_db_test_data' in 'aat/__init__.py'.
    ''')
