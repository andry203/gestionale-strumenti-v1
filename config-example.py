class config:

    SECRET_KEY = "EXAMPLE"
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:PASSWORD-EXAMPLE@localhost/DB-NAME-EXAMPLE'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Flask Mail settings ---
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'EXAMPLE@gmail.com'
    MAIL_PASSWORD = 'EXAMPLE'