from flask import Flask, render_template, request, redirect
from sen import contra, secret
import pymysql
import pymysql.cursors
import flask_login

app = Flask(__name__)
# app.secret_key = f'{secret}'
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

# connection = pymysql.connect(
#     database = 'cvasquez_rd',
#     user = 'cvasquez',
#     password = f'{contra}',
#     host = '10.100.33.60',
#     cursorclass = pymysql.cursors.DictCursor
# )

# class User:
#     is_authenticated = True
#     is_anonymous = False
#     is_active = True

#     def __init__(self, id,username):
#         self.id = id
#         self.username = username
    
#     def get_id(self):
#         return str(self.id)

# @login_manager.user_loader
# def load_user(user_id):
#     cursor = connection.cursor()
#     cursor.execute(f"SELECT * FROM `users` WHERE `id` = '{user_id}'")
#     results = cursor.fetchone()
#     connection.commit()
#     cursor.close()
#     if results is None:
#         return None
#     return User((results['id']), results['username'])


@app.route('/')
def index():
    return render_template('landing.html.jinja')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO `users` (`username`, `email`, `password`) VALUES ("{new_username}", "{new_email}", "{new_password}");')
        cursor.close()
        connection.commit()
    return render_template('sign_up.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM `users` WHERE `username` = "{username}"')
        result = cursor.fetchone()
        if password == result['password']:
            user = load_user(result['id'])
            flask_login.login_user(user)
            return redirect('/feed')
    return render_template('sign_in.html')

@app.route('/feed')
@flask_login.login_required
def feed():
    return render_template('feed.html.jinja')

@app.route('/new')
def new_landing():
    return render_template('prototypeSM.html.jinja')