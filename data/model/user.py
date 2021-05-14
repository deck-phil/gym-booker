from flask_login import UserMixin


class User(UserMixin):
    user_id = ''
    is_admin = False
    email = ''
    password = ''
    fit4less_password = ''
    home_gym = ''
    schedule = []

    def __init__(self, data):
        self.user_id = str(data.get('_id', ''))
        self.is_admin = data.get('is_admin', False)
        self.email = data.get('email', '')
        self.password = data.get('password', '')
        self.fit4less_password = data.get('fit4less_password', '')
        self.home_gym = data.get('home_gym', '')
        self.schedule = data.get('schedule', [])

    def get_id(self):
        return self.user_id

    def set_password(self, value, field_name='password'):
        from api.app import bcrypt
        if field_name == 'password':
            self.password = bcrypt.generate_password_hash(value).decode('utf - 8')
        elif field_name == 'fit4less_password':
            self.fit4less_password = bcrypt.generate_password_hash(value).decode('utf - 8')

    def check_password(self, value):
        from api.app import bcrypt
        result = bcrypt.check_password_hash(self.password, value)
        return result

    def to_dict(self):
        return {
            **self.to_api_dict(),
            **{
                'password': self.password,
                'fit4less_password': self.fit4less_password
            }
        }

    def to_api_dict(self):
        return {
            'email': self.email,
            'is_admin': self.is_admin,
            'home_gym': self.home_gym,
            'schedule': self.schedule,
        }
