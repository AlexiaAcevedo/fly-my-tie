from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login_signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/finish/account/setup')
def signup_continued():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('account_setup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# POST Methods

@app.route('/login/user', methods = ['POST'])
def login_user():
    user_in_db_email = User.get_by_email({"email": request.form['email']})
    user_in_db_username = User.get_by_username({"username": request.form['email']})
    if user_in_db_email == True:
        user_in_db = user_in_db_email
        return user_in_db
    elif user_in_db_username == True:
        user_in_db = user_in_db_username
        return user_in_db
    if not user_in_db:
        flash('Invalid Email/Username', 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/login')
    
    session['user_id'] = user_in_db.id
    return redirect('/home')

@app.route('/signup/user', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/signup')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save_user_initial(data)
    session['user_id'] = user_id
    return redirect('/finish/account/setup')