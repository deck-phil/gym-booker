from data.model.booking_event import BookingEvent
from datetime import datetime, timedelta
from engine.utils import WEEKDAYS

BOOKING_DAY_OFFSET = 3  # in days
TIME_SLOT_FORMAT = '%H:%M'


class UserSchedule:
    schedule = []

    def __init__(self, schedule_list=()):
        self.schedule = schedule_list

    def generate_events(self, until=datetime.now(), user=None):
        booking_events = []
        _date_idx = datetime.now().replace(hour=0, minute=0, second=0)
        while _date_idx < until:
            for weekday, time_slots in self.schedule.items():
                if WEEKDAYS.get(weekday, '') == _date_idx.weekday():
                    for time_slot in time_slots:
                        datetime_slot = datetime.combine(_date_idx.date(),
                                                         datetime.strptime(time_slot, TIME_SLOT_FORMAT).time())
                        event = BookingEvent({
                            'booking_datetime': datetime_slot - timedelta(days=BOOKING_DAY_OFFSET),
                            'user_id': user.user_id,
                            'gym_id': user.home_gym,
                            'weekday': weekday,
                            'time_slot': time_slot
                        })
                        booking_events.append(event)

            _date_idx += timedelta(days=1)
        return booking_events

    def to_dict(self):
        return self.schedule