import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from pitch import app, mail

def send_welcome_email(user):
    msg = Message('Welcome to pitch-in-60', sender="lastcam00@gmail.com", recipients=[user.email])
    msg.body = f"""We have just seen you have signed up for our application and want to welcome you. Please enjoy the list of all your  favourite pitches. Please login at: {url_for('login', _external=True)}
    """
    mail.send(msg)



#
def save_picture(form_picture):
    random_hex =  secrets.token_hex(7)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    pic_file_name = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/profile-pics', pic_file_name)

    output_size = (127, 127)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_file_name
