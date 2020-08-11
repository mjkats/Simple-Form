from flask import Flask, render_template, request, redirect, flash, url_for
from cs50 import SQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KBCQ6H9OQ4Ck3LrLtnYDRg'

db = SQL("sqlite:///customer_research.db")

@app.route("/", methods=["GET", "POST"])
def client_research():

    username = "michel"
    user_id = db.execute("SELECT user_id FROM users WHERE username = :name", name = username)[0]['user_id']

    if request.method == "GET":

        query = db.execute("SELECT questions.question, options.option, options.option_number, questions.question_id "
                            + "FROM questions "
                            + "JOIN question_options ON question_options.question_id = questions.question_id "
                            + "JOIN options ON options.option_id = question_options.option_id "
                            + "ORDER BY questions.question_id, options.option_number")

        questions = [{} for question in range(4)]

        for i in range(4):
            questions[i]["question_id"] = query[i*4]["question_id"]
            questions[i]["question"] = query[i*4]["question"]
            questions[i]["option_one"] = query[i*4]["option"]
            questions[i]["option_two"] = query[i*4+1]["option"]
            questions[i]["option_three"] = query[i*4+2]["option"]
            questions[i]["option_four"] = query[i*4+3]["option"]

        return render_template("client_research.html", questions = questions)

    else:

        answers = [{} for answer in range(4)]

        for i in range(4):
            index = str(i+1)

            data = request.form.get('radio_' + index)

            if data == None:
                flash("Erro: Por favor responda todas as perguntas.")
                return redirect(url_for('client_research'))

            data = data.split()
            answers[i]['answer_number'] = data[0]
            answers[i]['question_id'] = data[1]

        db.execute(f"INSERT INTO answers (question_id, answer_number, user_id) VALUES "
                    + "(?, ?, ?), (?, ?, ?), (?, ?, ?), (?, ?, ?)",
                    answers[0]['question_id'], answers[0]['answer_number'], user_id,
                    answers[1]['question_id'], answers[1]['answer_number'], user_id,
                    answers[2]['question_id'], answers[2]['answer_number'], user_id,
                    answers[3]['question_id'], answers[3]['answer_number'], user_id)

        flash(f"Obrigado por responder o questionário, {username}!")
        return render_template("empty.html")