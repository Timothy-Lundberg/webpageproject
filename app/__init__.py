from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


# Vi skapar ett Flask-objekt med "denna filen" som input
app = Flask(__name__)
# Vi skickar med Config-klassen som input för att sätta inställningar.
app.config.from_object(Config)
# Skapar en databas och döper den till db.
db = SQLAlchemy(app)
# Länkar databasen till vårat Flask-objekt. För att lättare kunna uppdatera databasen.
migrate = Migrate(app, db)
# Vi använder biblioteket LoginManager för att hantera inloggningar.
login = LoginManager(app)
# Sätter en standard sida där användaren behöver logga in. Aktiveras med @login_required i routes.
login.login_view = 'login'
# vi använder bootstrap för att snygga till våran hemsida
bootstrap = Bootstrap(app)

from app import routes, models


