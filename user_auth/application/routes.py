from application import app, db
from flask import render_template, redirect, url_for, flash, request
from application.forms import RegisterForm, LoginForm, NewPostForm, UpdateAccountForm,UpdatePostForm
from application.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
import secrets, os, time


# posts = [
#     {
#         'author': 'KIPTOO CALEB',
#         'title' : 'Missing Directory for Profile Pictures',
#         'content': 'Ensure the directory static/profile_pics exists in your project. If it doesn’t exist, the form_picture.save(picture_path) call will fail.Fix: Create the directory if it doesn’t exist',
#         'date_posted': 'December 20, 2024.'
#     },
#     {
#         'author': 'JANE DOE',
#         'title' : '2nd POST',
#         'content': '2nd post content ',
#         'date_posted': 'December 20, 2024.'
#     },
#     {
#         'author': 'JOHN DOE',
#         'title' : 'john\'s Post',
#         'content': 'john says: ........ ',
#         'date_posted': 'December 20, 2024.'
#     },
# ]

@app.route('/')
@app.route('/home')
def home():
    page  = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return  render_template('home.html', title='home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() 
        if user.password != form.password.data:
            flash('Invalid email or passowrd')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        return redirect(url_for('home'))
    return render_template('logIn.html', title='Log in' ,form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(fullname=form.fullname.data, username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Log in', form=form)


# # save pcture
# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, '/static/profile_pics', picture_fn)
#     form_picture.save(picture_path)
#     return picture_fn

# @app.route('/account', methods=['GET', 'POST'])
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.profile.data:
#             picture_file = save_picture(form.profile.data)
#             current_user.image_file = picture_file
#         current_user.fullname = form.fullname.data
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         return redirect(url_for('account'))
#     elif request.method == 'GET': 
#         form.fullname.data = current_user.fullname
#         form.username.data = current_user.username
#         form.email.data = current_user.email
 
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('account.html', title='Account page', form=form, image_file=image_file )

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    os.makedirs(os.path.join(app.root_path, 'static/profile_pics'), exist_ok=True)  # Ensure directory exists
    if not form_picture.filename:
        raise ValueError("Uploaded file has no filename.")
    form_picture.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    posts = Post.query.filter_by(user_id=current_user.id)
    if form.validate_on_submit():
        if form.profile.data:
            picture_file = save_picture(form.profile.data)
            current_user.image_file = picture_file
            db.session.add(current_user)  # Explicitly add current_user to the session
        current_user.fullname = form.fullname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        try:
            db.session.commit()  # Save changes
            db.session.refresh(current_user)  # Ensure current_user reflects latest data
            print(f"Updated image file: {current_user.image_file}")  # Debug
        except Exception as e:
            print(f"Database commit failed: {e}")
        return redirect(url_for('account'))
    elif request.method == 'GET': 
        form.fullname.data = current_user.fullname
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}') + '?t=' + str(int(time.time()))
    return render_template('account.html', title='Account page', form=form, image_file=image_file, posts=posts)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/require_loggedin', methods=['GET', 'POST'])
@login_required
def require_loggedin():
    users = User.query.all()
    return render_template('require_loggedin.html', title='Landing page', users=users)

@app.route('/post/new ', methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    print('unsuccessful')
    return render_template('create_post.html', title='New Post' , form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title  = form.title.data
        post.content = form.content.data
        db.session.commit()
        db.session.refresh(post)
        print('successfully updated')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data =post.content

    return render_template('update_post.html', title=form.title,form=form) 

@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))