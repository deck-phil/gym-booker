from pymongo import MongoClient
from bson import ObjectId
from data.model.user import User


class LocalDB:
    client = None
    db = None

    user = None

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.gym_manager
        self.user = self.db.user


class DataService:
    local_db = LocalDB()

    def get_user(self, **kwargs):
        user = self.local_db.user.find_one(kwargs)
        return user and User(user)

    def get_user_by_id(self, user_id):
        user = self.local_db.user.find_one(ObjectId(user_id))
        return user and User(user)

    def create_user(self, user):
        new_user = self.local_db.user.insert_one(user.to_dict())
        return new_user

    def change_user(self, user):
        self.local_db.user.update_one({
            '_id': ObjectId(user.user_id)
        }, {
            '$set': user.to_dict()
        })

    def list_users(self):
        users = self.local_db.user.find()
        return users and [User(i) for i in users] or []

    def list_home_gyms(self):
        return {
            'ottawa_gloucester': 'Ottawa Gloucester',
            'kanata_bridlewood': 'Kanata Bridlewood',
        }
