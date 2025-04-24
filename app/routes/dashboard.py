from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required


bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
def index():
    return "Dashboard Blueprint"