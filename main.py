from flask import Flask, render_template, url_for, redirect, request
import os
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(".flaskenv")
url = os.environ.get('DATABASE_URL')
connection = psycopg2.connect(url)
add_user = "INSERT INTO users (username, password) VALUES (%s, %s)"
get_user = "SELECT * FROM users WHERE username = %s"
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = connection.cursor()
    if request.method == 'POST':
        if request.form["username"] == "" or request.form["password"] == "" or request.form["confirm-password"] == "":
            return render_template('register.html', error="Please fill out all fields")
        if request.form["password"] != request.form["confirm-password"]:
            return render_template('register.html', error="Passwords do not match")
        cursor.execute(add_user, (request.form["username"], request.form["password"]))
        connection.commit()
        return redirect(url_for("home", username=request.form["username"]))
    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute(get_user, (username,))
        user = cursor.fetchone()
        if user == None:
            return render_template('login.html', error="Invalid username or password")
        if user[2] == password:
            return redirect(url_for('home', username=username))
        else:
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')
@app.route('/')
def start():
    return redirect(url_for('register'))
@app.route('/home/<username>')
def home(username):
    return render_template('index.html', username=username)
app.run()