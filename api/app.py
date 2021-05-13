from flask import Flask, request, Response
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from data.local_db import DataService


login_manager = LoginManager()
data_service = DataService()

app = Flask(__name__)
app.config['SECRET_KEY'] = '[xGH34v@2jk6dA1we5e*3TUY$f0efV)^b6/;'

login_manager.init_app(app)
bcrypt = Bcrypt(app)


@login_manager.user_loader
def load_user(user_id):
    return data_service.get_user_by_id(user_id)


@app.before_request
def check_valid_login():
    if request.endpoint and 'static' not in request.endpoint:
        view_function = app.view_functions[request.endpoint]
        is_public_endpoint = getattr(view_function.view_class, 'is_public', False)
        is_admin_endpoint = getattr(view_function.view_class, 'is_admin', False)

        if (not current_user.is_authenticated and not is_public_endpoint) \
                or (is_admin_endpoint and not current_user.is_admin):
            return Response({'Unauthorized'}, status=401, mimetype='application/json')


from api.handler.login_handler import LoginHandler
from api.handler.logout_handler import LogoutHandler
from api.handler.create_user_handler import CreateUserHandler
from api.handler.profile_handler import ProfileHandler

rules = [
    ['/login', 'login_handler', LoginHandler, ['POST']],
    ['/logout', 'logout_handler', LogoutHandler, ['GET', 'POST']],
    ['/create-user', 'create_user_handler', CreateUserHandler, ['POST']],
    ['/profile', 'profile_handler', ProfileHandler, ['GET']]
]

for rule in rules:
    app.add_url_rule(rule[0], rule[1], rule[2].as_view(rule[1]), methods=rule[3])
