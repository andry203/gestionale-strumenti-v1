import os, click
from flask.cli import with_appcontext
from app import db
from app.models import Utente
from werkzeug.security import generate_password_hash

@click.command('create-admin')
@with_appcontext
def create_admin():
    email = os.getenv('ADMIN_EMAIL', 'xxxxxxxxxxxxxx')
    pwd   = os.getenv('ADMIN_PASSWORD', 'xxxxxxxxxxxxxxx')
    if Utente.query.filter_by(email=email).first():
        click.echo(f"Esiste già un admin con email {email}")
        return
    admin = Utente(
        email=email,
        password=generate_password_hash(pwd),
        ruolo='admin'
    )
    db.session.add(admin)
    db.session.commit()
    click.echo(f"Super-user creato: {email}")