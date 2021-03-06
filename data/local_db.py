from pymongo import MongoClient
from bson import ObjectId
from data.model.user import User
from data.model.booking_event import BookingEvent


class LocalDB:
    client = None
    db = None

    user = None
    booking_event = None

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.gym_manager
        self.user = self.db.user
        self.booking_event = self.db.booking_event


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

    def list_user_events(self, user_id):
        events = self.local_db.booking_event.find({'user_id': ObjectId(user_id)})
        return events and [BookingEvent(i) for i in events] or []

    def add_events(self, events_list):
        events_list = [event.to_dict() for event in events_list]
        result = self.local_db.booking_event.insert_many(events_list)
        return result

