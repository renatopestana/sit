from flask import Flask
from .extensions import db, migrate, login_manager, csrf
from .blueprints.auth import auth_bp
from .blueprints.clients import clients_bp
from .blueprints.dealers import dealers_bp
from .blueprints.projects import projects_bp
from .blueprints.statuses import statuses_bp
from .blueprints.inventory import inventory_bp
from .blueprints.main import main_bp
from .models import User

def create_app(config_object="config.DevConfig"):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Por favor, faça login para acessar a página."

    app.register_blueprint(auth_bp)
    app.register_blueprint(clients_bp, url_prefix="/clientes")
    app.register_blueprint(dealers_bp, url_prefix="/concessionarios")
    app.register_blueprint(projects_bp, url_prefix="/projetos")
    app.register_blueprint(statuses_bp, url_prefix="/status-equipamentos")
    app.register_blueprint(inventory_bp, url_prefix="/equipamentos")
    app.register_blueprint(main_bp)

    return app
