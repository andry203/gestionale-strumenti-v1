from flask import Blueprint

bp = Blueprint('auth', __name__)

# Rotta di test (homepage temporanea)
@bp.route('/')
def index():
    return 'App Flask attiva, dio porcoooooooo. ciao'
