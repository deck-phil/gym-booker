from flask_login import current_user
from api.handler.base_handler import BaseHandler


class ProfileHandler(BaseHandler):

    def get(self):
        return self.json_response({
            'user_id': current_user.user_id,
            'email': current_user.email,
        })
