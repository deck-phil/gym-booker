import json
from flask.views import MethodView
from flask import Response
from data.local_db import DataService


class BaseHandler(MethodView):

    @property
    def data_service(self):
        return DataService()

    def error_response(self, message=None, status=500):
        return self.json_response({
            'success': False,
            'message': message or 'No message provided.'
        }, status=status)

    def json_response(self, data, status=200):
        json_data = json.dumps(data)
        return Response(json_data, status=status, mimetype='application/json')
