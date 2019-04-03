import os
from PIL import Image
import secrets
from flaskblog import app, mail
from flask import url_for
from flask_mail import Message

def save_image(image):
    random_name = secrets.token_hex(16)
    _, f_ext = os.path.splitext(image.filename)
    image_fn = random_name + f_ext
    path = os.path.join(app.root_path, 'static/profile_images', image_fn)
    i = Image.open(image)
    i.thumbnail((300, 300))
    i.save(path)
    return image_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''A password reset was made by someone (hopfuly you):
To reset your password please visit 
{url_for('new_password', token=token, _external=True)}
or simply ignore this message if that wasn't you
'''
    mail.send(msg)