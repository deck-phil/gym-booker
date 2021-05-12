from pymongo import MongoClient
from bson import ObjectId
from data.model.user import User


class LocalDB:
    client = None
    db = None

    users = None

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.gym_manager
        self.users = self.db.users

    def get_user(self, **kwargs):
        user = self.users.find_one(kwargs)
        return user and User(user)

    def get_user_by_id(self, user_id):
        user = self.users.find_one(ObjectId(user_id))
        return user and User(user)

    def create_user(self, user):
        new_user = self.users.insert_one(user.to_dict())
        return new_user

    def list_users(self):
        users = self.users.find()
        return users and [User(i) for i in users] or []
