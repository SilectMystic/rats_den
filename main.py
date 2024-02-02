from flask import Flask, render_template, request, redirect
from sen import contra
import pymysql
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(
    database = 'cvasquez_rd',
    user = 'cvasquez',
    password = contra,
    host = '10.100.33.60',
    cursorclass = pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('landing.html.jinja')

@app.route('/sign_up', methods=['POSTS'])
def sign_up():
    if request.method == 'POST':
        cursor = connection.cursor()
        new_username = request.form[new_username]
        new_email = request.form[new_email]
        new_password = request.form[new_password]
        cursor.execute(f'INSERT INTO `users` (`username`, `email`, `password`) VALUES ("{new_username}", "{new_email}", "{new_password}");')
    return render_template('sign_up.html')