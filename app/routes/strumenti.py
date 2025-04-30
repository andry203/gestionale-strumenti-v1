from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models import Strumento, Richiesta, Utente
from datetime import date
from app.email import send_email_async

bp = Blueprint('strumenti', __name__, url_prefix='/strumenti')


# Instruments index route

@bp.route('/')
def index():

    strumenti = Strumento.query.all()
    return render_template('strumenti/index.html', strumenti=strumenti)


# Instrument request route

@bp.route('/<int:id>/richiedi', methods=['POST'])
@login_required
def richiedi(id):
    inst = Strumento.query.get_or_404(id)

    if inst.status != "disponibile":
        flash('Strumento non disponibile al momento.', 'warning')
    else:
        note = request.form.get('note', None)
        req = Richiesta(
            id_utente=current_user.id,
            id_strumento=id,
            data_richiesta=date.today(),
            note=note
        )
        db.session.add(req)
        db.session.commit()
        flash('Richiesta inviata.', 'success')

        # Send email to all responsables
        subject = 'Nuova richiesta di strumento'
        recipients = Utente.query.filter_by(ruolo='responsabile').with_entities(Utente.email).all()
        recipients = [recipient[0] for recipient in recipients]
        text_body = f'Nuova richiesta di strumento da parte di {current_user.email}.\nStrumento: {inst.tipo} {inst.serial_number}\nNote: {note}'

        try:
            send_email_async(subject, recipients, text_body)
            print("Flask mail invio riuscito")
        except Exception as e:
            print("Errore invio email:", e)

    return redirect(url_for('strumenti.index'))
    