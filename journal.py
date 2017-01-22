#!/usr/bin/env python
from flask import Flask, redirect, request
import json
import random
import string
import cgi

app = Flask(__name__)

@app.route("/mydebug")
def state():
    count = read_userdata()
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
    <p><a href="/signup">Sign up</a> for an account.</p>
    </body>
    </html>
    """.format()

@app.route("/login_action")
def login_action():
    username = request.args.get('username')
    password = request.args.get('password')
    x = read_userdata()
    if username in x.keys():
        stored_password = x.get(username)
        if stored_password == password:
            #generate random secret for cookie
            cookie = ''.join(random.choice(string.ascii_lowercase) for _ in range(20))
            #print cookie
            #set cookie in user's browser
            return redirect("/journal/{0}".format(username)), {'Set-Cookie' : 'name=bowwow'}
            ##todo next: get the cookie back and verify it
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

@app.route("/signup")
def signup():
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Jour</title>
    <link rel="stylesheet" type="text/css" href="./journal.css">
    </head>
    <body>
    <p>Sign up for an account here.</p>
    <p>Choose a Username and Password</p>
    <form method="get" action="/signup_action">
    <input type="text" name="username" />
    <input type="password" name="password" />
    <input type="submit">
    </form>
    <p>Already have an account? <a href="/login_action">Log in.</a></p>
    </body>
    </html>
    """

@app.route("/signup_action")
def signup_action():
    username = request.args.get('username')
    password = request.args.get('password')
    x = read_userdata()
    if username in x.keys():
        return """
        <p>There is already an account with that username</p>
        <p><a href="/signup">Sign up</a> with a different username or <a href="/login">return to Login</a></p>
        """
    else:
        #new_user = x[username]
        x[username] = password
        #return json.dumps(x)

        text_file = open("user.txt", "w")
        output = json.dumps(x)
        text_file.write(output)
        text_file.close()
        return redirect("/login")


@app.route("/journal/<username>")
def render_journal(username):
    curr_data = read_journaldata()
    #print "username is ", username
    #print curr_data
    if not username in curr_data.keys():
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
            <p><a href="/login">Log Out</a></p>
            <form method="get" action="/update_action">
            <input type="text" name="journal_input" />
            <input type="text" name="username" value="{0}" hidden="true" />
            <input type="submit">
            </form>
            </body>
            </html>
            """.format(username)
    else:
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
        <p><a href="/login">Log Out</a></p>
        <form method="get" action="/update_action">
        <input type="text" name="journal_input" />
        <input type="text" name="username" value="{0}" hidden="true" />
        <input type="submit">
        </form>
        <div>{1}</div>
        </body>
        </html>
        """.format(username,x)

@app.route("/journal/journal.css")
def render_css():
    #put css in a file, read the file and then send it
    text_file = open("journal.css", "r")
    curr_css = text_file.read()
    text_file.close()
    return curr_css, 200, {'Content-Type' : 'text/css' }

@app.route("/update_action")
def update_journal():
    # get the input from the user
    username = request.args.get('username')
    journal_input = request.args.get('journal_input')
    sanitized_input = cgi.escape(journal_input)
    #read the current data from the file
    curr_data = read_journaldata()
    if not username in curr_data.keys():
        curr_data[username] = []
        curr_array = curr_data[username]
        #print curr_array
        # insert journal_input into curr_data to make new data
        curr_array.append(sanitized_input)
        new_data = curr_data
        text_file = open("journaldata.txt", "w")
        output = json.dumps(new_data)
        text_file.write(output)
        text_file.close()
        return redirect("/journal/{0}".format(username))
    else:
        curr_array = curr_data[username]
        #print curr_array
        # insert sanitized_input into curr_data to make new data
        curr_array.append(sanitized_input)
        new_data = curr_data
        write_journaldata(new_data)
        return redirect("/journal/{0}".format(username))


def read_userdata():
    try:
        text_file = open("user.txt", "r")
        data = json.loads(text_file.read())
        text_file.close()
    except:
        data = {}
    return data


def read_journaldata():
    try:
        text_file = open("journaldata.txt", "r")
        data = json.loads(text_file.read())
        text_file.close()
    except:
        data = {}
    return data

def write_journaldata(new_data):
    try:
        text_file = open("journaldata.txt", "w")
        output = json.dumps(new_data)
        text_file.write(output)
        text_file.close()
    except:
        output = {}
    return output

if __name__ == "__main__":
    app.run(debug=True)