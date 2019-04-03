from flask import (
    flash, redirect, render_template, request,
    url_for, abort, Blueprint)
from flask_login import (
    current_user, login_user, logout_user, login_required)

from flaskblog import db, forms
from flaskblog.models.Post import Post
from flaskblog.models.User import User

posts = Blueprint('posts', __name__)

@posts.route('/posts/<int:post_id>', methods=['GET', 'POST'])
def get_posts(post_id):
    post = Post.query.get(post_id)
    form = forms.PostForm()
    form.title.data = post.title
    form.content.data = post.content

    posts = Post.query.all()
    return render_template('post.html', title=post.title, post=post, form=form)


@posts.route('/post_update/<int:post_id>', methods=['POST'])
@login_required
def post_update(post_id):
    post = Post.query.get(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form = forms.PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated successfuly', 'success')
        return redirect(url_for('posts.get_posts', post_id=post_id))


@posts.route('/post_delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfuly', 'success')
    return redirect(url_for('main.home'))
