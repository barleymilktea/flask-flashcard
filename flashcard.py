from flask import (Flask, render_template,abort, jsonify, request, redirect, url_for)
from model import db, save_db
from datetime import datetime

app = Flask(__name__)

@app.route("/") #this changes the function below to a view function. We can assign an URL in the (), now it is "/", which is the main page
def welcome():
    return render_template('welcome.html',
        cards=db)

@app.route("/card/<int:index>") #we expect an integer after the card/
def card_view(index):
    try:
        card_load = db[index]
        return render_template("card.html", card=card_load, index=index, max_index=len(db)-1) #first 'card' comes from the jinja in card.html
    except IndexError:
        abort(404) #this will show the Page Not Found webpage error

@app.route("/add_card/", methods = ["GET","POST"])
def add_card():
    if request.method == "POST":
    #form has been submitted, process user data
        card ={"question": request.form['question'], "answer": request.form['answer']}
        db.append(card)
        save_db()
        return redirect(url_for('card_view', index=len(db)-1))
    else:
        return render_template("add_card.html")

@app.route("/remove_card/<int:index>", methods=['GET','POST'])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('card_view', index=len(db)-1))
        else:
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)
#use REST API
@app.route("/api/card/")
def api_card_list():
    return jsonify(db) #cannot return db because we cannot return a list in flask and REST API

@app.route("/api/card/<int:index>")
def api_card_details(index):
    try:
        return db[index]
    except IndexError:
        abort(404)

#add a page called 'date'
#@app.route("/date") #the URL/date page appears below
#def date():
#    return "This page was served at " + str(datetime.now())

#add a page that shows how many times it has been viewed
#counter = 0
#@app.route("/count")
#def count_views():
#    global counter
#    counter += 1
#    return "Page views: " + str(counter)
