from flask import flash, redirect, render_template, url_for
from flaskblog import forms
from flaskblog import app

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
    form = forms.SignupForm()
    if form.validate_on_submit():
        flash(f'Account created for user {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = forms.SigninForm()
    return render_template('login.html', title='Login', form=form)
