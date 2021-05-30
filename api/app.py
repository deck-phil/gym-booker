from flask import Flask, request, Response
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from data.local_db import DataService
from api.encryption import SECRET_KEY
from api.job.job_scheduler import JobScheduler


job_scheduler = JobScheduler()
login_manager = LoginManager()
data_service = DataService()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

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


def initialize_jobs():
    from engine.config import START_JOB

    if not START_JOB:
        print('CONFIG: START_JOB is False')
        return False
    print('Starting Job Scheduler')
    from api.job.job_create_booking_events import job, JOB_INTERVAL

    job_scheduler.add_job(job, JOB_INTERVAL)# in seconds)
    job_scheduler.start()


from api.handler.login_handler import LoginHandler
from api.handler.logout_handler import LogoutHandler
from api.handler.create_user_handler import CreateUserHandler
from api.handler.profile_handler import ProfileHandler
from api.handler.list_home_gym_handler import ListHomeGymHandler
from api.handler.test_credentials_handler import TestCredentialsHandler

rules = [
    ['/login', 'login_handler', LoginHandler, ['POST']],
    ['/logout', 'logout_handler', LogoutHandler, ['GET', 'POST']],
    ['/create-user', 'create_user_handler', CreateUserHandler, ['POST']],
    ['/profile', 'profile_handler', ProfileHandler, ['GET', 'POST']],
    ['/list-home-gyms', 'list_home_gym_handler', ListHomeGymHandler, ['GET']],
    ['/test-credentials', 'test_credentials_handler', TestCredentialsHandler, ['GET']]
]

for rule in rules:
    app.add_url_rule(rule[0], rule[1], rule[2].as_view(rule[1]), methods=rule[3])

initialize_jobs()
