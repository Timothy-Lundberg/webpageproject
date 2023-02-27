from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
# Skapar en databas och döper den till db.
db = SQLAlchemy(app)
# Länkar databasen till vårat Flask-objekt. För att lättare kunna uppdatera databasen.
migrate = Migrate(app, db)
# Vi använder biblioteket LoginManager för att hantera inloggningar.
login = LoginManager(app)
# Sätter en standard sida där användaren behöver logga in. Aktiveras med @login_required i routes.
login.login_view = 'login'

from app import routes, models


