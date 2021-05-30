from data.local_db import DataService
from datetime import datetime, timedelta

JOB_INTERVAL = 5


def job():
    data_service = DataService()

    all_users = data_service.list_users()

    for user in all_users:
        existing_events = data_service.list_user_events(user.user_id)   # Get all current events
        existing_events = [(i.weekday, i.time_slot) for i in existing_events]   # Create unique list
        user_events = user.schedule.generate_events(datetime.now() + timedelta(days=7), user=user)  # Generate events to be added
        user_events = [i for i in user_events if (i.weekday, i.time_slot) not in existing_events]   # Filter out duplicate events
        if user_events:
            events = data_service.add_events(user_events)
            print('added events')
    print('job complete')
    return [] # return success log