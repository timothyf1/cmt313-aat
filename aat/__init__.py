import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dotenv import DotEnv
from flask_wtf.csrf import CSRFProtect
from flask_assets import Environment
from flask_caching import Cache
from flask_compress import Compress
from flask_login import LoginManager


# Initialisation and configuration:
# Flask app
app = Flask(__name__)
env = DotEnv(app)
if bool(os.environ.get('SECRET_KEY')):
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
else:
    app.config['SECRET_KEY'] = 'development'
cookie_security = True
app.config['SESSION_COOKIE_SECURE'] = cookie_security
app.config['REMEMBER_COOKIE_SECURE'] = cookie_security
app.config['REMEMBER_COOKIE_HTTPONLY'] = True

# Database connection
if bool(os.environ.get('DATABASE_URI')):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
else:
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'aat.db')
db = SQLAlchemy(app)

# Form protection
csrf = CSRFProtect(app)

# Assets
from .assets import bundles
assets = Environment(app)
assets.register(bundles)

# Caching & Compression
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
Compress(app)

# Login Manager
from .models import User
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    return User.query.get(int(user_id))

# Routes
from .routes import auth, errors, routes, stats

# Create database
from . import models
with app.app_context():
    db.create_all()
    models.create_admin()
    # Comment/uncomment the below line to enable/disable test content generation for the database.
    from . import create_db_test_data
