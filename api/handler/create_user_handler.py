from flask import request
from api.handler.base_handler import BaseHandler
from data.local_db import User


class CreateUserHandler(BaseHandler):

    def post(self):
        new_user = User({
            'email': request.form.get('email')
        })
        new_user.set_password(request.form.get('password'))

        result = self.local_db.create_user(new_user)
        message = 'User created successfully!' if result else 'Error. Could not create user.'
        return self.json_response({
            'success': result,
            'message': message
        })
