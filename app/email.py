from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail

def _send_async(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body=None):
    app = current_app._get_current_object()
    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    # invio in background
    Thread(target=_send_async, args=(app, msg)).start()
