from flask import Flask, escape, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view ="login"
bootstrap=Bootstrap(app)



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Car': Car}



from routes import Routes
from model import models
