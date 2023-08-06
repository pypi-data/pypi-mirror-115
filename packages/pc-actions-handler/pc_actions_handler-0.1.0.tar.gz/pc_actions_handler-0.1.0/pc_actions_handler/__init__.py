from flask import request, Flask
from flask_restful import Resource, Api
import json
import os

from .middleware import Middleware
from .server import Audio, Player, Display, Sys

config = {
    'port': 5000,
    'api_key': '',
}

config_path = os.path.join(os.environ['HOME'], '.config', 'pc_actions_handler')
with open(os.path.join(config_path, 'config.json')) as f:
    config = json.load(f)

app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app, config['api_key'])
api = Api(app)

api.add_resource(Audio, '/audio')
api.add_resource(Player, '/player')
api.add_resource(Display, '/display/<id>')
api.add_resource(Sys, '/')

def run_server():
    app.run('0.0.0.0', port=config['port'])
