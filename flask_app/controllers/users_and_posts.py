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

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('home.html', user = User.get_by_id(data), all_posts = Post.get_all_posts_with_users())

@app.route('/edit/user-profile')
def edit_user_settings():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template('edit_user.html', user = User.get_by_id(data))

@app.route('/profile/<int:id>')
def view_user_profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    this_user_data = {
        "id": id
    }
    logged_in_user_data = {
        "id": session['user_id']
    }
    return render_template('profile.html', this_user = User.get_all_posts_of_one_user(this_user_data), user = User.get_by_id(logged_in_user_data))

@app.route('/create/post')
def new_post():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    return render_template('create.html', user = user)

@app.route('/edit/post/<int:id>')
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    post_data = {
        "id":id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template('edit.html', post = Post.get_one_post_with_user(post_data), user = User.get_by_id(user_data))

@app.route('/post/<int:id>')
def read_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    post_data = {
        "id": id
    }
    user_data = {
        "id": session['user_id']
    }
    return render_template('read.html', post = Post.get_one_post_with_user(post_data), user = User.get_by_id(user_data))

@app.route('/delete/<int:id>')
def delete_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Post.delete_post(data)
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# POST Methods

@app.route('/login/user', methods = ['POST'])
def login_user():
    user_in_db = User.get_by_email({"email": request.form['email']})
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
        'profile_photo_url': 'https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png',
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save_user_initial(data)
    session['user_id'] = user_id
    return redirect('/home')

@app.route('/edit/profile', methods=['POST'])
def edit_user_info():
    if not User.validate_edit_user(request.form):
        return redirect('/edit/user-profile')
    data = {
        'bio': request.form['bio'],
        'profile_photo_url': request.form['profile_photo_url'],
        'id': session['user_id']
    }
    User.update_user(data)
    return redirect('/home')

@app.route('/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/create/post')
    data = {
        "image_url": request.form['image_url'],
        "fly_name": request.form['fly_name'],
        "pattern_type": request.form['pattern_type'],
        "difficulty": request.form["difficulty"],
        "hook": request.form['hook'],
        "bead": request.form['bead'],
        "thread": request.form['thread'],
        "fins": request.form['fins'],
        "tail": request.form['tail'],
        "belly": request.form['belly'],
        "body": request.form['body'],
        "instructions": request.form['instructions'],
        "user_id": session['user_id']
    }
    Post.save_post(data)
    return redirect('/home')

@app.route('/edit/<int:id>', methods=['POST'])
def edit_user_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect(f'/edit/post/{id}')
    data = {
        "image_url": request.form['image_url'],
        "fly_name": request.form['fly_name'],
        "pattern_type": request.form['pattern_type'],
        "difficulty": request.form["difficulty"],
        "hook": request.form['hook'],
        "bead": request.form['bead'],
        "thread": request.form['thread'],
        "fins": request.form['fins'],
        "tail": request.form['tail'],
        "belly": request.form['belly'],
        "body": request.form['body'],
        "instructions": request.form['instructions'],
        "user_id": session['user_id']
    }
    Post.update_post(data)
    return redirect(f'/post/{id}')

@app.route('/post/<int:id>/favorite', methods = ['POST'])
def favorite_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    pass

@app.route('/post/<int:id>/unfavorite', methods = ['POST'])
def unfavorite_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    pass