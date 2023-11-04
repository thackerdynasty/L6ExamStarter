from flask import Flask, render_template, url_for, redirect
import os
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(".flaskenv")
url = os.environ.get['DATABASE_URL']
connection = psycopg2.connect(url)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # add more variables as needed
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/')
def start():
    return redirect(url_for('register'))
@app.route('/home')
def home():
    return render_template('index.html')
app.run()