from bson import ObjectId

from datetime import datetime


class BookingEvent:
    booking_datetime = None
    status_id = 0
    user_id = ''
    gym_id = ''
    weekday = ''
    time_slot = ''

    def __init__(self, data):
        self.booking_datetime = data.get('booking_datetime', self.booking_datetime)
        self.status_id = data.get('status_id', self.status_id)
        self.user_id = data.get('user_id', self.user_id)
        self.gym_id = data.get('gym_id', self.gym_id)
        self.weekday = data.get('weekday', self.weekday)
        self.time_slot = data.get('time_slot', self.time_slot)

    def to_dict(self):
        return {
            'booking_datetime': self.booking_datetime,
            'user_id': ObjectId(self.user_id),
            'status_id': self.status_id,
            'gym_id': self.gym_id,
            'weekday': self.weekday,
            'time_slot': self.time_slot,
        }
