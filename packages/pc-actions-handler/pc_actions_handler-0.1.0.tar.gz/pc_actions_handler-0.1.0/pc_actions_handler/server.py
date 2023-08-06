from flask import request
from flask_restful import Resource
import os

class Audio(Resource):
    def post(self):
        action = request.json['action']
        if action in ['phone', 'tv']:
            os.system(f'audio-{action}')
            return 200
        return 400


class Player(Resource):
    def post(self):
        action = request.json['action']
        if action in ['play', 'pause', 'next', 'previous']:
            os.system(f'playerctl {action}')
            return 200
        return 400


class Display(Resource):
    def post(self, id):
        action = request.json['action']
        if action in ['plug', 'unplug', 'toggle'] and \
            id in ['left', 'right', 'tv']:
            os.system(f'{action}-{id}')
            return 200
        return 400


class Sys(Resource):
    def post(self):
        action = request.json['action']
        if action in ['off']:
            os.system('poweroff')
            return 200
        return 400
