# Gestionale per strumentazione laboratorio R&D Vertiv

Un'applicazione web per la gestione degli strumenti in uso/in stock e delle calibrazioni.

# Descrizione

L'applicazione permette di:


# Tecnologie

- Backend: Python (Flask)
- Frontend: HTML, CSS, JavaScript
- Database: MySQL

# Installazione

Dipendenze scritte in "requirements.txt"

Database MySQL attivo le cui credenziali di accesso sono configurabili in "config.py"

# Struttura del progetto

/gestionale-strumenti-v1
|--/app
|----/routes
|------auth.py
|------dashboard.py
|------richieste.py
|------strumenti.py  
|----/static
|------/css
|------/js
|--------dashboard.js
|--------strumenti.js
|----/templates
|------base.html
|------homepage.html
|------register.html
|------/dashboard
|--------admin.html
|--------responsabile.html
|------/richieste
|--------index.html
|------/strumenti
|--------index.html
|----__init__.py
|----admin.py
|----email.py
|----models.py
|--config.py
|--run.py
|--requirements.py
|--README.md