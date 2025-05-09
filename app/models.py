from app import db
from flask_login import UserMixin
from datetime import date

# Table 'utenti'

class Utente (UserMixin, db.Model):
    
    __tablename__ = 'utenti'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    ruolo = db.Column(db.Enum('admin', 'responsabile', 'user'), nullable=False, default='user')
    q_domanda  = db.Column(db.String(250), nullable=True)
    q_risposta = db.Column(db.String(300), nullable=True)

    richieste = db.relationship('Richiesta', backref='utente', lazy=True)

    def __repr__(self):
        return f'<Utente {self.email}>'
    

# Table 'strumenti'

class Strumento (db.Model):

    __tablename__ = 'strumenti'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    modello = db.Column(db.String(50), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    caratteristiche = db.Column(db.Text, nullable=True)
    data_calibrazione = db.Column(db.Date, nullable=True)
    status = db.Column(db.Enum('disponibile', 'in uso'), nullable=False, default='disponibile')
    posizione = db.Column(db.String(100), nullable=True)
    prelevato_da = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=True)
    note = db.Column(db.Text, nullable=True)

    prelevato_da_utente = db.relationship(
        'Utente',
        foreign_keys=[prelevato_da],
        backref=db.backref('strumenti_prelevati', lazy='dynamic')
    )

    def __repr__(self):
        return f'<Strumento {self.tipo} {self.serial_number}>'


# Table 'richieste'

class Richiesta (db.Model):

    __tablename__ = 'richieste'

    id = db.Column(db.Integer, primary_key=True)
    id_utente = db.Column(db.Integer, db.ForeignKey('utenti.id'), nullable=False)
    id_strumento = db.Column(db.Integer, db.ForeignKey('strumenti.id'), nullable=False)
    data_richiesta = db.Column(db.Date, nullable=False, default=date.today)
    status = db.Column(db.Enum('in attesa', 'approvata', 'rifiutata'), nullable=False, default='in attesa')
    destinazione = db.Column(db.String(100), nullable=True)
    note = db.Column(db.Text, nullable=True)

    strumento = db.relationship('Strumento', backref='richieste', lazy=True)

    def __repr__(self):
        return f'<Richiesto strumento:{self.id_strumento} da utente:{self.id_utente}>'
