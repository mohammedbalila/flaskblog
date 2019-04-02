from flask import flash, redirect, render_template, url_for, request
from flask_login import login_user, current_user, logout_user
from flaskblog import app, bcrypt, db, forms
from flaskblog.models.User import User
from flaskblog.models.Post import Post
import os
import secrets
from PIL import Image
posts = [
    {
        'title': 'post one',
        'content': '''Documentation and examples for Bootstrap’s powerful,
        responsive navigation header, the navbar. Includes support for branding,
        navigation, and more, including support for our collapse plugin'''
    },
    {
        'title': 'post two',
        'content': '''A card is a flexible and extensible content container.
        It includes options for headers and footers, a wide variety of content,
        contextual background colors, and powerful display options.
        If you’re familiar with Bootstrap 3, cards replace our old panels, wells,
        and thumbnails. Similar functionality to those components is available as
        modifier classes for cards.'''
    },
    {'title': 'post three', 'content': 'I\'m a great post'},
]
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfuly.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(
                f'The user with an email of {form.email.data} doesn\'t exsist.', 'danger')
            return redirect(url_for('login'))
        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash(
                f'Wrong password', 'danger')
            return redirect(url_for('login'))
        login_user(user, form.remember_me.data)
        flash(f'Login success welcome back {user.username}.', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    user = User.query.get(user_id)
    image_path = url_for('static', filename=f'profile_images/{user.profile_image}')
    return render_template('profile.html', title=user.username, user=user, image_path=image_path)

def save_image(image):
    random_name = secrets.token_hex(16)
    _, f_ext = os.path.splitext(image.filename)
    image_fn = random_name + f_ext
    path = os.path.join(app.root_path, 'static/profile_images', image_fn)
    i = Image.open(image)
    i.thumbnail((300, 300))
    i.save(path)
    return image_fn

@app.route('/settings/<int:user_id>', methods=['GET', 'POST'])
def settings(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    form = forms.UpdateUserForm()
    form.username.data = user.username
    form.email.data = user.email
    form.bio.data = user.bio
    if request.method == 'POST':
        form = forms.UpdateUserForm()
        if form.validate_on_submit():
            user.username = form.username.data
            user.email = form.email.data
            user.bio = form.bio.data
            if form.profile_image.data:
                image = save_image(form.profile_image.data)
                user.profile_image = image
            db.session.commit()
            flash('Updated successfuly', 'success')
            return redirect(url_for('profile', user_id=current_user.id))

    return render_template('settings.html', title='Settings', form=form)


@app.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    form = forms.PasswordResetForm()
    if form.validate_on_submit():
        pass
    return render_template('password_reset.html', title='Reset password', form=form)