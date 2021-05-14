from flask import request
from flask_login import current_user
from api.handler.base_handler import BaseHandler


class ProfileHandler(BaseHandler):

    def get(self):
        user = self.data_service.get_user_by_id(current_user.user_id)
        return self.json_response(user.to_api_dict())

    def post(self):
        user = self.data_service.get_user_by_id(current_user.user_id)

        request_home_gym = request.form.get('home_gym', '')
        request_fit4less_password = request.form.get('fit4less_password', '')

        home_gyms = self.data_service.list_home_gyms()
        if request_home_gym not in home_gyms:
            return self.error_response('Invalid home gym')

        user.home_gym = request_home_gym

        if request_fit4less_password:
            user.set_password(request_fit4less_password, field_name='fit4less_password')

        self.data_service.change_user(user)

        return self.json_response({
            'status': 'profile_updated'
        })
