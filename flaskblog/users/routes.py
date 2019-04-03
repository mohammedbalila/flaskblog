from flask import (
    flash, redirect, render_template, request,
    url_for, abort, jsonify, Blueprint)
import json
from flask_login import current_user, login_user, logout_user, login_required
from flaskblog import app, bcrypt, db, forms
from flaskblog.models.Post import Post
from flaskblog.models.User import User
from flaskblog.users.utils import save_image, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = forms.SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    password=hashed_password, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfuly.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = forms.SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(
                f'The user with an email of {form.email.data} doesn\'t exsist.', 'danger')
            return redirect(url_for('users.login'))
        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash(
                f'Wrong password', 'danger')
            return redirect(url_for('users.login'))
        login_user(user, form.remember_me.data)
        flash(f'Login success welcome back {user.username}.', 'success')
        return redirect(url_for('main.home'))
    return render_template('login.html', title='Login', form=form)


@users.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('users.login'))
# User.query.filter(User.username.like("%u%")).all()


@users.route('/search_user', methods=['GET'])
def search_user():
    username = request.args.get('username')
    users = User.query.filter(User.username.like(f'%{username}%')).all()
    return json.dumps([u.toJSON() for u in users])


@users.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    image_path = url_for(
        'static', filename=f'profile_images/{user.profile_image}')
    return render_template('profile.html', title=user.username,
                           user=user, image_path=image_path, posts=posts)


@users.route('/settings/<int:user_id>', methods=['GET', 'POST'])
def settings(user_id):
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))
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
            return redirect(url_for('users.profile', user_id=current_user.id))

    return render_template('settings.html', title='Settings', form=form)


@users.route('/password_reset', methods=['GET', 'POST'])
def password_reset():
    form = forms.RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        flash('Unavailabe now please try later.', 'info')
        return redirect('password_reset')
        # send_reset_email(user)
        # flash(
        #     f'An email with a reset token was sent to {form.email.data}', 'info')
    return render_template('password_reset.html', title='Reset password', form=form)


@users.route('/password_reset/token', methods=['GET', 'POST'])
def new_password(token):
    user = User.verfiy_reset_token(token)
    if user is None:
        flash('Token expired or invalid', 'warning')
        return redirect(url_for('users.password_reset'))
    form = forms.PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password updated successfuly', 'success')
        return redirect('login')
    return render_template('password_reset.html', title='Reset password', form=form)
