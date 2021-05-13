from flask_login import current_user
from api.handler.base_handler import BaseHandler


class ProfileHandler(BaseHandler):

    def get(self):
        user = self.data_service.get_user_by_id(current_user.user_id)
        return self.json_response(user.to_dict())
