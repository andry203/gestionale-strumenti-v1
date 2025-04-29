from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app import db
from app.models import Strumento, Utente, Richiesta
from datetime import datetime


bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


# Dashboard route 

@bp.route('/')
@login_required
def index():

    strumenti = Strumento.query.all()
    utenti = Utente.query.all()
    richieste = Richiesta.query.all()

    if current_user.ruolo == 'admin':
        return render_template('dashboard/admin.html', strumenti=strumenti, utenti=utenti, richieste=richieste)
    elif current_user.ruolo == 'responsabile':
        return render_template('dashboard/responsabile.html', strumenti=strumenti, richieste=richieste)
    else:
        flash('Accesso non autorizzato.', 'danger')
        return redirect(url_for('auth.homepage'))


# New instrument route 

@bp.route('/aggiungi', methods=['POST'])
@login_required
def aggiungi():

    tipo = request.form.get('tipo')
    marca = request.form.get('marca')
    modello = request.form.get('modello')
    serial_number = request.form.get('serial_number')
    caratteristiche = request.form.get('caratteristiche')
    data_calib = request.form.get('data_calibrazione')

    nuovo_strumento = Strumento(
        tipo = tipo,
        marca = marca,
        modello = modello,
        serial_number = serial_number,
        caratteristiche = caratteristiche,
        data_calibrazione = data_calib
    )
    db.session.add(nuovo_strumento)
    db.session.commit()

    flash('Nuovo strumento aggiunto con successo', 'success')
    return redirect(url_for('dashboard.index'))

# Delete instrument route

@bp.route('/<int:id>/elimina', methods=['POST'])
@login_required
def elimina(id):

    strumento = Strumento.query.get_or_404(id)

    db.session.delete(strumento)
    db.session.commit()

    flash('Strumento eliminato con successo', 'success')
    return redirect(url_for('dashboard.index'))

# Save instrument modification route

@bp.route('/<int:id>/modifica', methods=['POST'])
@login_required
def modifica(id):

    strumento = Strumento.query.get_or_404(id)

    strumento.tipo = request.form.get('tipo')
    strumento.marca = request.form.get('marca')
    strumento.modello = request.form.get('modello')
    strumento.serial_number = request.form.get('serial_number')
    strumento.caratteristiche = request.form.get('caratteristiche')
    strumento.data_calibrazione = request.form.get('data_calibrazione')

    db.session.commit()

    flash('Strumento modificato con successo', 'success')
    return redirect(url_for('dashboard.index'))


# Approve request route

@bp.route('/richieste/<int:id>/status', methods=['POST'])
@login_required
def aggiorna_status_richiesta(id):

    richiesta = Richiesta.query.get_or_404(id)

    new_status = request.form.get('status')
    if new_status not in ('approvata', 'rifiutata'):
        flash('Status non valido.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    richiesta.status = new_status

    if new_status == 'approvata':
        strumento = Strumento.query.get(richiesta.id_strumento)
        strumento.status = 'in uso'
        strumento.prelevato_da = richiesta.id_utente

    db.session.commit()
    flash(f'Richiesta #{id} marcata come "{new_status}"', 'success')
    return redirect(url_for('dashboard.index'))


# Change roles route

@bp.route('/utenti/ruolo', methods=['POST'])
@login_required
def cambia_ruolo():

    email = request.form.get('email')
    nuovo_ruolo = request.form.get('ruolo')

    utente = Utente.query.filter_by(email=email).first_or_404()

    if nuovo_ruolo not in ('admin', 'responsabile', 'user'):
        flash('Ruolo non valido.', 'danger')
        return redirect(url_for('dashboard.index'))
    
    utente.ruolo = nuovo_ruolo
    db.session.commit()

    flash(f'Ruolo di {utente.email} cambiato in "{nuovo_ruolo}"', 'success')
    return redirect(url_for('dashboard.index'))