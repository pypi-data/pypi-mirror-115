import os
import json
from flask import Request, Response

class Middleware():
    def __init__(self, app, api_key):
        self.app = app
        self.api_key = api_key

    def __call__(self, env, start_response):
        request = Request(env)
        headers = request.headers
        if 'api_key' not in headers or headers['api_key'] != self.api_key:
            res = Response(
                json.dumps({
                    'message': 'Not Authorized',
                }),
                mimetype='application/json',
                status=401
            )
            return res(env, start_response)
        return self.app(env, start_response)
