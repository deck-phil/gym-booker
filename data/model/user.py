from flask_login import UserMixin


class User(UserMixin):
    user_id = ''
    email = ''
    password = ''
    schedule = []

    def __init__(self, data):
        self.email = data.get('email', '')
        self.password = data.get('password', '')
        self.user_id = str(data.get('_id', ''))
        self.schedule = data.get('schedule', [])

    def get_id(self):
        return self.user_id

    def set_password(self, value):
        from api.app import bcrypt
        self.password = bcrypt.generate_password_hash(value).decode('utf - 8')

    def check_password(self, value):
        from api.app import bcrypt
        result = bcrypt.check_password_hash(self.password, value)
        return result

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password,
            'schedule': self.schedule,
        }
