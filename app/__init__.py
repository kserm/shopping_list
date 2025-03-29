from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import calendar
from flask_wtf.csrf import CSRFProtect

load_dotenv()
csrf = CSRFProtect()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure database path
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database')
    os.makedirs(db_path, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(db_path, "shopping_lists.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    csrf.init_app(app)
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_timeout': 30,
    'pool_size': 5,
    'max_overflow': 10
    }

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