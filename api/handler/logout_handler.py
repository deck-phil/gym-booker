from flask_login import logout_user
from api.handler.base_handler import BaseHandler
from api.access_decorators import public_endpoint


@public_endpoint
class LogoutHandler(BaseHandler):

    def get(self):
        logout_user()
        return self.json_response({
            'status': 'logged_out'
        })

    def post(self):
        logout_user()
        return self.json_response({
            'status': 'logged_out'
        })
