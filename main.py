from flask import Flask, render_template, request, redirect, g
from sen import contra, secret
import pymysql
import pymysql.cursors
import flask_login 

app = Flask(__name__)
app.secret_key = f'{secret}'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

def connect_db():
    return pymysql.connect(
        host="127.0.0.1",
        user="cvasquez",
        password=f"{contra}",
        database="cvasquez_rd",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 

class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, id,username):
        self.id = id
        self.username = username
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `id` = '{user_id}'")
    results = cursor.fetchone()
    get_db().commit()
    cursor.close()
    if results is None:
        return None
    return User((results['id']), results['username'])

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/')


@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
    return render_template('landing.html.jinja')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_email = request.form['new_email']
        new_password = request.form['new_password']
        cursor = get_db().cursor()
        cursor.execute(f'INSERT INTO `users` (`username`, `email`, `password`) VALUES ("{new_username}", "{new_email}", "{new_password}");')
        cursor.close()
        get_db().commit()
    return render_template('sign_up.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if flask_login.current_user.is_authenticated:
        return redirect('/feed')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `users` WHERE `username` = "{username}"')
        result = cursor.fetchone()
        if password == result['password']:
            user = load_user(result['id'])
            flask_login.login_user(user)
            return redirect('/feed')
    return render_template('sign_in.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')

@app.route('/feed', methods=['GET','POST'])
@flask_login.login_required
def feed():
    if flask_login.current_user.is_authenticated == False:
        return redirect('/')
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `posts` ORDER BY `timestamp`")
    get_db().commit()
    cursor.close()
    posts_db = cursor.fetchall()
    user_login = flask_login.current_user.username
    if request.method == 'POST':
        description = request.form['new_post']
        user_id = flask_login.current_user.get_id()
        cursor = get_db().cursor()
        cursor.execute(f"INSERT INTO `posts` (`user_id`, `description`) VALUES ('{user_id}', '{description}')")
        cursor.close()
        get_db().commit()
        return redirect('/feed')

    return render_template('feed.html.jinja', posts_db = posts_db, user_login = user_login)

# @app.route('/feed', methods=['POST'])
# def create_post():
#     if  request.method == 'POST':
#         description = request.form['new_post']
#         user_id = flask_login.current_user.id

#         cursor = get_db().cursor()
#         cursor.execute(f"INSERT INTO `posts` (`user_id`, `description`) VALUES ('{user_id}', '{description}')")
#         cursor.close()
#         get_db().commit()



@app.route('/new')
def new_landing():
    return render_template('prototypeSM.html.jinja')

@app.route('/new_sign_in')
def new_sign_in():
    return render_template('prototype_signin.html')