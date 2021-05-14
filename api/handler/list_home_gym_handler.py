from api.handler.base_handler import BaseHandler


class ListHomeGymHandler(BaseHandler):

    def get(self):
        home_gyms = self.data_service.list_home_gyms()
        return self.json_response({
            'home_gyms': home_gyms
        })
