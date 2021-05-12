from flask import request
from flask_login import login_user
from api.handler.base_handler import BaseHandler
from api.access_decorators import public_endpoint


@public_endpoint
class LoginHandler(BaseHandler):

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password', '').encode('utf-8')

        user = self.local_db.get_user(user_name=username)

        if not user or not user.check_password(password):
            return self.error_response('Wrong username or password.')

        login_user(user)

        return self.json_response({
            'status': 'logged_in'
        })
