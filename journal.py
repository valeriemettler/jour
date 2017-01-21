#!/usr/bin/env python
from flask import Flask, redirect, request
import json
import random
import string

app = Flask(__name__)

@app.route("/mydebug")
def state():
    count = read_data()
    return json.dumps(count)

@app.route("/login")
def login():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Jour</title>
    <link rel="stylesheet" type="text/css" href="./journal.css">
    </head>
    <body>
    <p>Enter Username and Password</p>
    <form method="get" action="/login_action">
    <input type="text" name="username" />
    <input type="password" name="password" />
    <input type="submit">
    </form>
    </body>
    </html>
    """.format()

@app.route("/login_action")
def login_action():
    username = request.args.get('username')
    password = request.args.get('password')
    x = read_data()
    if username in x.keys():
        stored_password = x.get(username)
        if stored_password == password:
            return redirect("/journal/{0}".format(username))
        else:
            return """
        <p>incorrect password</p>
        <a href="/login">Return to Login</a>
        """
    else:
        return """
        <p>username does not exist</p>
        <a href="/login">Return to Login</a>
        """



@app.route("/journal/<username>")
def render_journal(username):
    text_file = open("journaldata.txt", "r")
    curr_data = json.loads(text_file.read())
    text_file.close()
    print "username is ", username
    print curr_data
    show_data = curr_data[username]
    x = ""
    for i in show_data:
        x = x + '<p class='"todo"'>{}</p>'.format(i)
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Jour</title>
    <link rel="stylesheet" type="text/css" href="./journal.css">
    </head>
    <body>
    <p>Welcome to your Journal!</p>
    <form method="get" action="/update_action">
    <input type="text" name="journal_input" />
    <input type="text" name="username" value="{0}" hidden="true" />
    <input type="submit">
    </form>
    <div>{1}</div>
    </form>
    </body>
    </html>
    """.format(username,x)

@app.route("/journal/journal.css")
def render_css():
    #put css in a file, read the file and then send it (instead of having it inline in the program)
    text_file = open("journal.css", "r")
    curr_css = text_file.read()
    text_file.close()
    return curr_css, 200, {'Content-Type' : 'text/css' }

@app.route("/update_action")
def update_journal():
    # get the input from the user
    username = request.args.get('username')
    journal_input = request.args.get('journal_input')
    #read the current data from the file
    text_file = open("journaldata.txt", "r")
    curr_data = json.loads(text_file.read())
    text_file.close()
    curr_array = curr_data[username]
    print curr_array
    # insert journal_input into curr_data to make new data
    curr_array.append(journal_input)
    new_data = curr_data
    text_file = open("journaldata.txt", "w")
    output = json.dumps(new_data)
    text_file.write(output)
    text_file.close()
    return redirect("/journal/{0}".format(username))


def read_data():
    try:
        text_file = open("user.txt", "r")
        data = json.loads(text_file.read())
        text_file.close()
    except:
        data = {}
    return data

if __name__ == "__main__":
    app.run(debug=True)