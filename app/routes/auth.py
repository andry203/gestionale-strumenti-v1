from flask import Blueprint, render_template, request, redirect, url_for, flash
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

        # Check if user email exists
        if Utente.query.filter_by(email=email).first():
            flash ('Email già registrata.', 'warning')
            return redirect(url_for('auth.register'))

        # Create and save user
        new_user = Utente(email=email, password=generate_password_hash(pwd))
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


# Delete account route

@bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():

    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    flash ('Il tuo account è stato eliminato.', 'info')
    return redirect(url_for('auth.homepage'))