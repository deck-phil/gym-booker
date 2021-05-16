from flask_login import current_user
from api.handler.base_handler import BaseHandler


class TestCredentialsHandler(BaseHandler):

    def get(self):
        from engine.main import GymBooker

        result = GymBooker().run_script('test_script', user_id=current_user.user_id)

        return self.json_response({
            'status': result
        })
