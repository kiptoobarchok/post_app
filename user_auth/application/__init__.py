from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'kiptoobarchok8032'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

## initialization of flask extensions
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

from application import routes, models