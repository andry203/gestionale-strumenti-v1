from flask import Blueprint, render_template, redirect, flash, request
from flask_login import current_user, login_required
from app import db
from sqlalchemy.orm import joinedload
from app.models import Richiesta


bp = Blueprint('richieste', __name__, url_prefix='/richieste')


# Requests index route

@bp.route('/')
@login_required
def index():

    user_requests = (Richiesta.query.options(joinedload(Richiesta.strumento))
                     .filter_by(id_utente=current_user.id)
                     .all())
    print(user_requests)
    return render_template('richieste/index.html', richieste=user_requests)