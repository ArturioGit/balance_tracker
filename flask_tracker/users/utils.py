from flask import url_for
from flask_tracker import mail
from flask import current_app as app
from flask_mail import Message
import secrets
import os


def save_avatar(avatar_data):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(avatar_data.filename)
    avatar_filename = random_hex + f_ext
    avatar_path = os.path.join(app.root_path, 'static/img/avatars', avatar_filename)
    avatar_data.save(avatar_path)
    return avatar_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset request",
                  sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
<a href="{url_for('users.reset_password', token=token, _external=True)}">Here</a>
---------------------------------------------------
---------------------------------------------------
If you did not make this request, ignore this email    
    """
    mail.send(msg)
