from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Utente


bp = Blueprint('auth', __name__)


# Homepage route
@bp.route('/')
def homepage():
    return render_template('homepage.html')

# Register route

@bp.route('/register', methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        q_domanda = request.form['domanda']
        q_risposta = request.form['risposta']

        # Check if user email exists
        if Utente.query.filter_by(email=email).first():
            flash ('Email già registrata.', 'warning')
            return redirect(url_for('auth.register'))
        
        # Production first user registered == admin
        if Utente.query.filter_by(ruolo='admin').count() == 0:
            ruolo = 'admin'
        else:
            ruolo = 'user'

        # Create and save user
        new_user = Utente(email=email,
                          password=generate_password_hash(pwd),
                          ruolo=ruolo,
                          q_domanda=q_domanda,
                          q_risposta=generate_password_hash(q_risposta))
        db.session.add(new_user)
        db.session.commit()

        flash ('Registrazione effettuata con successo. Puoi effettuare il login.', 'success')
        return redirect(url_for('auth.homepage'))

    return render_template('register.html')


# Login route

@bp.route('/login', methods=('GET', 'POST'))
def login():

    if request.method == 'POST':
        next_page = request.form.get('next') or url_for('auth.homepage')
        email = request.form['email']
        pwd   = request.form['password']
        user  = Utente.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, pwd):
            flash('Credenziali errate', 'danger')
            return redirect(request.referrer or url_for('auth.homepage'))

        login_user(user)
        flash('Login eseguito!', 'success')
        return redirect(next_page)

    return redirect(url_for('auth.homepage'))


# Logout route 

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash ('Logout avvenuto con successo.', 'info')
    return redirect(url_for('auth.homepage'))


# Personal area route

@bp.route('/area_personale', strict_slashes=False)
@login_required
def area_personale():
    return render_template('area_personale.html', user=current_user)


# Delete account route

@bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():

    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash ('Il tuo account è stato eliminato.', 'info')
    return redirect(url_for('auth.homepage'))


# Change password route

@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():

    if request.method == 'POST':
        old_pwd = request.form['old_password']
        new_pwd = request.form['new_password']

        # Check if old password is correct
        if not check_password_hash(current_user.password, old_pwd):
            flash('Password errata', 'danger')
        else:
            # Update password
            current_user.password = generate_password_hash(new_pwd)
            db.session.commit()
            flash('Password aggiornata con successo', 'success')
        return redirect(request.referrer or url_for('auth.homepage'))
    

# Recover password route

@bp.route('/password_recovery', methods=['POST'])
def password_recovery():
    # 1) Forziamo la lettura JSON e logghiamo eventuali errori
    try:
        payload = request.get_json(force=True)
    except Exception as e:
        current_app.logger.error("JSON parse error: %s", e)
        return jsonify({'error': 'Richiesta malformata'}), 400

    email       = payload.get('email')
    answer      = payload.get('answer')
    new_password= payload.get('new_password')

    current_app.logger.info("Password recovery step: email=%s, answer=%s, new_pwd=%s",
                            email, bool(answer), bool(new_password))

    if not email:
        return jsonify({'error': 'Email non fornita'}), 400

    user = Utente.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Email non trovata'}), 404

    # 2) Primo step: invio la domanda
    if answer is None and new_password is None:
        return jsonify({'question': user.q_domanda}), 200

    # 3) Secondo step: controllo la risposta
    if answer is not None and new_password is None:
        if not check_password_hash(user.q_risposta, answer):
            return jsonify({'error': 'Risposta di sicurezza errata'}), 400
        return jsonify({'request_new_password': True}), 200

    # 4) Terzo step: aggiorno la password
    if new_password:
        if not check_password_hash(user.q_risposta, answer):
            return jsonify({'error': 'Risposta di sicurezza errata'}), 400
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'success': True}), 200

    # fallback
    return jsonify({'error': 'Parametri mancanti'}), 400