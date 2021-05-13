from flask_login import UserMixin


class User(UserMixin):
    user_id = ''
    is_admin = False
    email = ''
    password = ''
    schedule = []

    def __init__(self, data):
        self.email = data.get('email', '')
        self.is_admin = data.get('is_admin', False)
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
        return self.to_dict() + {
            'password': self.password
        }

    def to_api_dict(self):
        return {
            'email': self.email,
            'is_admin': self.is_admin,
            'schedule': self.schedule,
        }
