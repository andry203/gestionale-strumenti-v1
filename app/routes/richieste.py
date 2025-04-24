from flask import Blueprint


bp = Blueprint('richieste', __name__, url_prefix='/richieste')

@bp.route('/')
def index():
    return "Richieste index page"