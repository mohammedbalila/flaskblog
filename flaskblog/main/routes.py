from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user
from flaskblog import db, forms
from flaskblog.models.Post import Post

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
def home():
    form = forms.PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfuly', 'success')
        return redirect(url_for('main.home'))
    posts = Post.query.all()
    return render_template('home.html', title='Home', posts=posts, form=form)
