import smtplib
from email.mime.text import MIMEText
from threading import Thread
from flask import current_app

def _send_via_smtp_ssl(subject, recipients, text_body):
    """Funzione interna che apre la connessione SSL e invia la mail."""
    cfg = current_app.config

    # Recipients converted to list even when contain only 1 str
    if isinstance(recipients, str):
        recipients_list = [recipients]
    else:
        recipients_list = list(recipients)

    msg = MIMEText(text_body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From']    = cfg['MAIL_USERNAME']
    msg['To']      = ', '.join(recipients_list)

    server = smtplib.SMTP_SSL(cfg['MAIL_SERVER'], cfg['MAIL_PORT'])
    server.set_debuglevel(1)
    try:
        server.login(cfg['MAIL_USERNAME'], cfg['MAIL_PASSWORD'])
        server.sendmail(cfg['MAIL_USERNAME'], recipients_list, msg.as_string())
        current_app.logger.info(f"Email inviata a: {recipients_list}")
    finally:
        server.quit()

def send_email_async(subject, recipients, text_body):
    """
    Wrapper che cattura il context e lancia _send_via_smtp_ssl in un Thread.
    In questo modo la rotta non resta bloccata.
    """
    app = current_app._get_current_object()

    def task():
        with app.app_context():
            _send_via_smtp_ssl(subject, recipients, text_body)

    Thread(target=task, daemon=True).start()
