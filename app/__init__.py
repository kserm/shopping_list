from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import calendar
from flask_wtf.csrf import CSRFProtect
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
csrf = CSRFProtect()

db = SQLAlchemy()

auth = HTTPBasicAuth()

def create_app():
    app = Flask(__name__)
    
    # Configure database path
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database')
    os.makedirs(db_path, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_path, "shopping_lists.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    app.config['AUTH_USERNAME'] = os.getenv('AUTH_USERNAME', 'admin')
    app.config['AUTH_PASSWORD'] = os.getenv('AUTH_PASSWORD', 'admin')
    csrf.init_app(app)
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_timeout': 30,
    'pool_size': 5,
    'max_overflow': 10
    }
    
    users = {
        app.config['AUTH_USERNAME']: generate_password_hash(app.config['AUTH_PASSWORD'])
    }

    @auth.verify_password
    def verify_password(username, password):
        if username in users and check_password_hash(users.get(username), password):
            return username

    # Add month format filter
    @app.template_filter('format_month')
    def format_month_filter(month_num):
        try:
            return f"{month_num} - {calendar.month_name[month_num]}"
        except (IndexError, KeyError):
            return str(month_num)  # Fallback to just the number if month is invalid

    db.init_app(app)

    with app.app_context():
        from app.models import ShoppingList
        db.create_all()

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app