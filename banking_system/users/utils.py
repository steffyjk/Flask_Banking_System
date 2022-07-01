import os
import secrets
# from PIL import Image
import random

from flask import url_for, current_app
from flask_mail import Message
from banking_system import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password REset Request', sender='steffykhristi.18.ce@iite.indusuni.ac.in', recipients=[user.user_email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token',token=token, _external=True)}

If you did not make this request then just ignore this msg and no change will be there.   
'''
    mail.send(msg)


def send_otp_email(user):
    otp = random.randint(1111, 9999)
    msg = Message('Your OTP is here: ', sender='steffykhristi.18.ce@iite.indusuni.ac.in',
                  recipients=[user.user_email])
    msg.body = f'''This is the OTP as requested: :{otp}
    If you did not make this request then just ignore this msg and no change will be there.   
    '''
    mail.send(msg)

    return otp

