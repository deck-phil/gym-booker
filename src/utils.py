from datetime import datetime, timedelta

WEEKDAYS = {
    'MO': 0,
    'TU': 1,
    'WE': 2,
    'TH': 3,
    'FR': 4,
    'SA': 5,
    'SU': 6
}

BOOKING_DATE_FORMAT = '%Y-%m-%d'
BOOKING_TIME_FORMAT = '%I:%M %p'


# Checks if time string is within the hour.
# time_str must be in format HH:MM
def is_time_for_now(current_datetime, time_str):
    current_time = current_datetime
    end_booking_time = current_datetime + timedelta(hours=1)
    booking_time = datetime.combine(current_datetime.date(), datetime.strptime(time_str, '%H:%M').time())
    return current_time < booking_time < end_booking_time


# Returns the Date and Time for booking if it's for today else False
def is_booking_for_today(schedule):
    current_datetime = datetime.today()
    for date in schedule:
        if WEEKDAYS.get(date, '') == current_datetime.weekday():
            time_for_booking = schedule.get(date, None)
            if is_time_for_now(current_datetime, time_for_booking):
                booking_date = current_datetime.strftime(BOOKING_DATE_FORMAT)
                booking_time = datetime.strptime(time_for_booking, '%H:%M').strftime(BOOKING_TIME_FORMAT)
                return booking_date, booking_time

    return False, False
