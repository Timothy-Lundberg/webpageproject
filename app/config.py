import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # här Sätter vi lösenordet till databasen
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Här visar vi vägen till vår databas.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Här sätter vi notiser till disabled
    SQLALCHEMY_TRACK_MODIFICATIONS = False
