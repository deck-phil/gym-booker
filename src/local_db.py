from pymongo import MongoClient


class User:
    email = ''
    password = ''

    def __init__(self, data):
        self.email = data.get('email', '')
        self.password = data.get('password', '')

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password
        }


class LocalDB:
    client = None
    db = None

    users = None

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.gym_manager
        self.users = self.db.users

    def create_user(self, user):
        self.users.insert_one(user.to_dict())

    def list_users(self):
        users = self.users.find()
        return users and [User(i) for i in users] or []
