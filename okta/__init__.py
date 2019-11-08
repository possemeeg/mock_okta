from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os

flask_app = Flask(__name__)

config = os.environ.get('CR_CONFIG', 'config.DevelopmentConfig')
print('Using config:', config)
flask_app.config.from_object(config)

CORS(flask_app)

flask_api = Api(flask_app)

logged_in_users = {}

from okta.oauth2.views import oauth2
from okta.api.views import api

flask_app.register_blueprint(oauth2, url_prefix='/oauth2/default')
flask_app.register_blueprint(api, url_prefix='/api')
