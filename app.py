import os
import config
from flask import Flask, render_template, request, jsonify, flash, Markup, redirect, url_for
from multiprocessing import Value
from sqlalchemy.event import listen
from sqlalchemy import event, DDL
from flask_sqlalchemy import SQLAlchemy

counter = Value('i', 1)
counter_questionlevel2 = Value('i', 1)
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *

@app.route("/")
def root():
    counter.value = 1
    counter_questionlevel2.value = 1
    return render_template('index.html')

@app.route("/introduction")
def introduction():
    return render_template('introduction.html')


@app.route("/tutorial/<language>")
def tutorial_ruby(language):
    if language == 'ruby':
        return render_template('tutorialruby.html')
    elif language == 'python':
        return render_template('tutorialpython.html')
    elif language == 'javascript':
        return render_template('tutorialjavascript.html')
    else:
        return 'Error'

@app.route("/question/<language>/<id_>", methods=['GET', 'POST'])
def get_question_by_id(language, id_):
    question = Question.query.filter_by(id=id_).first()
    if int(id_) > 10 and language == 'ruby':
        button = Markup(f'<form method="GET" action="/questionlevel2/ruby/1"><button class="submitbutton" type="submit">Go on level 2! ✌️</button></form>')
        flash("Well done! You completed the Ruby Level 1 🎉!")
        flash(button)
        return redirect(url_for('congratulationlevel1'))
    elif int(id_) > 20 and language == 'python':
        button = Markup(f'<form method="GET" action="/questionlevel2/ruby/1"><button class="submitbutton" type="submit">Go on level 2! ✌️</button></form>')
        flash("Well done! You completed the Python Level 1! 🎉")
        flash(button)
        return redirect(url_for('congratulationlevel1'))
    elif int(id_) > 30 and language == 'javascript':
        button = Markup(f'<form method="GET" action="/questionlevel2/ruby/1"><button class="submitbutton" type="submit">Go on level 2! ✌️</button></form>')
        flash("Well done! You completed the JavaScript Level 1 🎉!")
        flash(button)
        return redirect(url_for('congratulationlevel1'))

    if request.method =='POST':
        # print(request.form['question'])
        if request.form['question'] == question.answer:
            with counter.get_lock():
                counter.value += 1
                id = counter.value
            button = Markup(f'<form method="GET" action="/question/{language}/{id}"><button class="submitbutton" type="submit">next 🙌</button></form>')
            flash("Well done! 💪 ")
            flash(button)
            return render_template('question.html',question=question)
        else:
            flash('That is wrong 🚫 Try again!')
            return render_template('question.html',question=question)

    return render_template('question.html',question=question)

@app.route("/questionlevel2/<language>/<id_>", methods=['GET', 'POST'])
def get_questionlevel2_by_id(language, id_):
    question2 = QuestionLevel2.query.filter_by(id=id_).first()
    if int(id_) > 10 and language == 'ruby':
        flash("Well done! You completed the Ruby Level 2! 🏅")
        return redirect(url_for('congratulationlevel2'))
    elif int(id_) > 20 and language == 'python':
        flash("Well done! You completed the Python Level 2! 🏅")
        return redirect(url_for('congratulationlevel2'))
    elif int(id_) > 30 and language == 'javascript':
        flash("Well done! You completed the JavaScript Level 2! 🏅")
        return redirect(url_for('congratulationlevel2'))

    if request.method =='POST':
        if request.form['user_answer'] == question2.answer:
            with counter_questionlevel2.get_lock():
                counter_questionlevel2.value += 1
                id = counter_questionlevel2.value
            button = Markup(f'<form method="GET" action="/questionlevel2/{language}/{id}"><button class="submitbutton" type="submit">next 🙌</button></form>')
            flash("Well done! 💪 ")
            flash(button)
            return render_template('question2.html',question2=question2)
        else:
            flash('That is wrong 🚫  Try again!')
            return render_template('question2.html',question2=question2)

    return render_template('question2.html',question2=question2)

@app.route("/congratulationlevel1")
def congratulationlevel1():
    return render_template('congratulationlevel1.html')

@app.route("/congratulationlevel2")
def congratulationlevel2():
    return render_template('congratulationlevel2.html')

@app.before_first_request
def setup():
    db.session.query(Question).delete()
    db.session.execute("ALTER SEQUENCE questions_id_seq RESTART WITH 1;")
    db.session.commit()
# ------------ RUBY QUESTIONS PART 1 ------------
    db.session.add(Question(question=u'1️⃣ How many data types are available in Ruby?', choice1=u'3', choice2=u'1', choice3=u'4', choice4=u'6', answer=u'6'))
    db.session.add(Question(question=u'2️⃣ Which of the following is the correct way to define a string?', choice1=u'"Hello"', choice2=u'Hello', choice3=u'-Hello-', choice4=u'(Hello)', answer=u'"Hello"'))
    db.session.add(Question(question=u'3️⃣ Which of the following is known as a boolean value?', choice1=u'Yes', choice2=u'Truth', choice3=u'Real', choice4=u'True', answer=u'True'))
    db.session.add(Question(question=u'4️⃣ How do you display "Hi there!" on the screen?', choice1=u'put "Hi there!"', choice2=u'puts "Hi there!"', choice3=u'"puts Hi there!"', choice4=u'puts Hi there!', answer=u'puts "Hi there!"'))
    db.session.add(Question(question=u'5️⃣ How do you display the integer 23 on the screen?', choice1=u'23', choice2=u'puts 23', choice3=u'23 puts', choice4=u'puts "23"', answer=u'puts 23'))
    db.session.add(Question(question=u'6️⃣ Which of the following is the correct way to assign the integer 30 to the variable a?', choice1=u'a = 30', choice2=u'a(30)', choice3=u'30 = a', choice4=u'a == 30', answer=u'a = 30'))
    db.session.add(Question(question=u'7️⃣ Given a variable a = 25, how do you display the value of the variable a?', choice1=u'puts "a"', choice2=u'puts variable(a)', choice3=u'puts a', choice4=u'a', answer=u'puts a'))
    db.session.add(Question(question=u'8️⃣ Which of the following is not a valid datatype in Ruby?', choice1=u'Integer', choice2=u'String', choice3=u'Timedate', choice4=u'Boolean', answer=u'Timedate'))
    db.session.add(Question(question=u'9️⃣ What is the extension used for saving a ruby file?', choice1=u'.ruby', choice2=u'.r', choice3=u'.rb', choice4=u'.ry', answer=u'.rb'))
    db.session.add(Question(question=u'10) How do you comment out a single line of code in Ruby?', choice1=u'#', choice2=u'begin and end', choice3=u'//', choice4=u'<!- ->', answer=u'#'))
# ------------ PYTHON QUESTIONS PART 1 ------------
    db.session.add(Question(question=u'1️⃣ How many data types are available in Python?', choice1=u'3', choice2=u'4', choice3=u'5', choice4=u'6', answer=u'5'))
    db.session.add(Question(question=u'2️⃣ Which of the following is the correct way to define a string?', choice1=u'"Hello"', choice2=u'Hello', choice3=u'-Hello-', choice4=u'(Hello)', answer=u'"Hello"'))
    db.session.add(Question(question=u'3️⃣ Which of the following is known as a boolean value?', choice1=u'Yes', choice2=u'Truth', choice3=u'Real', choice4=u'True', answer=u'True'))
    db.session.add(Question(question=u'4️⃣ How do you display "Hi there!" on the screen?', choice1=u'print "Hi there!"', choice2=u'print("Hi there!")', choice3=u'"print Hi there!"', choice4=u'prints Hi there!', answer=u'print("Hi there!")'))
    db.session.add(Question(question=u'5️⃣ How do you display the number 23 on the screen?', choice1=u'23', choice2=u'print(23)', choice3=u'23 print', choice4=u'print "23"', answer=u'print(23)'))
    db.session.add(Question(question=u'6️⃣ Which of the following is the correct way to assign the number 30 to the variable a?', choice1=u'a = 30', choice2=u'a(30)', choice3=u'30 = a', choice4=u'a == 30', answer=u'a = 30'))
    db.session.add(Question(question=u'7️⃣ Given a variable a = 25, how do you display the value of the variable a?', choice1=u'print "a"', choice2=u'print variable(a)', choice3=u'print(a)', choice4=u'a', answer=u'print(a)'))
    db.session.add(Question(question=u'8️⃣ Which of the following is not a valid datatype in Python?', choice1=u'Integer', choice2=u'String', choice3=u'Timedate', choice4=u'Boolean', answer=u'Timedate'))
    db.session.add(Question(question=u'9️⃣ What is the extension used for saving a python file?', choice1=u'.python', choice2=u'.p', choice3=u'.py', choice4=u'.pt', answer=u'.py'))
    db.session.add(Question(question=u'🔟 What do you use to comment out a single line of code in Python?', choice1=u'#', choice2=u'begin and end', choice3=u'//', choice4=u'<!- ->', answer=u'#'))

# ------------ JAVASCRIPT QUESTIONS PART 1 ------------


# ------------ RUBY QUESTIONS PART 2 ------------
    db.session.commit()

    db.session.query(QuestionLevel2).delete()
    db.session.execute("ALTER SEQUENCE questions_level2_id_seq RESTART WITH 1;")
    db.session.commit()
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=1, question=u' 1️⃣ What do you use to call a method on an object?', answer=u'.'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=2, question=u'2️⃣ What is the result of 8 % 5?', answer=u'3'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=3, question=u'3️⃣ How do you assign the string "Programming is fun" to the variable a?', answer=u'a = "Programming is fun"'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=4, question=u'4️⃣ What is the syntax to close a class ?', answer=u'end'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=5, question=u'5️⃣ How would you display the integer 42 as a string?', answer=u'puts "42"'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=6, question=u'6️⃣ Given an array a = [25, "Yikes!", false]. What would be the output of a[2] output?', answer=u'false'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=7, question=u'7️⃣ Given an array a = [25, "Yikes!", false]. If you do a.push("WOW"), what would be the output of a[3] ?', answer=u'WOW'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=8, question=u'8️⃣ Given a hash h = {"one" => "un", "two" => "deux", "three" => "trois"}. What would be the output of h["three"]', answer=u'trois'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=9, question=u'9️⃣ Given a string s = "Test123". What would s.reverse.upcase output?', answer=u'321TSET'))
    db.session.add(QuestionLevel2(language=u'Ruby', question_display_id=10, question=u'🔟 Given a string s = "Test123". What would s.include? "est1" output?', answer=u'true'))
# ------------ PYTHON QUESTIONS PART 2 ------------
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=11, question=u' 1️⃣ What is a Python?', answer=u'Programming language'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=12, question=u'2️⃣ What is the output of print (10 * 2)?', answer=u'20'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=13, question=u'3️⃣ Given a variable python = "Snake", How do you output "Snake"?', answer=u'print(python)'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=14, question=u'4️⃣ What is the syntax to create a class named person ?', answer=u'class Person:'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=15, question=u'5️⃣ How would you display the integer 42 as a string?', answer=u'print("42")'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=16, question=u'6️⃣ Given an list l = [15, "Bike", True]. What would be the output of print(l[0]) output?', answer=u'15'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=17, question=u'7️⃣ Given an list l = ["Cat", 2, "dog"]. If you do l.append(4), what would be the output of print(l[3]) ?', answer=u'4'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=18, question=u'8️⃣ Given a dictionnary d = {"marvel":  "Iron Man", "Dc Comics": "Batman"}. What would be the output of print(d.get("marvel"))', answer=u'Iron Man'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=19, question=u'9️⃣ Given a string s = "Hello everyone!". How would you output the lenght of it?', answer=u'print(len(s))'))
    db.session.add(QuestionLevel2(language=u'Python', question_display_id=20, question=u'🔟 Given a string s = "amazing". What would be the output of print(s.upper())?', answer=u'AMAZING'))
# ------------ JAVASCRIPT QUESTIONS PART 2 ------------


    db.session.commit()



if __name__ == '__main__':
    app.run()
