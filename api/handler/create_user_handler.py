from flask import request
from api.handler.base_handler import BaseHandler
from data.local_db import User
from pymongo.errors import DuplicateKeyError
from api.access_decorators import admin_endpoint


@admin_endpoint
class CreateUserHandler(BaseHandler):

    def post(self):
        new_user = User({
            'email': request.form.get('email')
        })
        new_user.set_password(request.form.get('password'))

        try:
            result = self.data_service.create_user(new_user)
        except DuplicateKeyError as e:
            return self.error_response('Email already taken')

        return self.json_response({
            'success': True,
            'message': 'User created successfully!'
        })
