# third-party imports
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py")

    Bootstrap(app)
    FontAwesome(app)
    JWTManager(app)

    from .home import homes as home_blueprint
    from .auth import auths as auth_blueprint

    from .web import web_client as web_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(web_blueprint)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("error.html", title="Error")

    return app
