from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Пожалуйста авторизуйтесь'

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='', static_folder='static', 
                template_folder='templates')
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.tech import bp as tech_bp
    app.register_blueprint(tech_bp, url_prefix='/tech')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.errors import register_error_handlers
    register_error_handlers(app)

    return app 

from app import models