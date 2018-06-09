# third-party imports
from flask import Flask, jsonify

# local imports
from config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v2/')

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify("You do not have sufficient permissions \
         to access this resources."), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify("The resource you are looking For Doesnt exist"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify("The server encountered an internal error."), 500

    return app
