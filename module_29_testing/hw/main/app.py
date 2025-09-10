from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

first_request_done = False

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///parking_app.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .routes import bp  # импорт вашего Blueprint

    @app.before_request
    def run_once():
        global first_request_done
        if not first_request_done:
            with app.app_context():
                db.create_all()
            first_request_done = True

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    app.register_blueprint(bp)

    return app
