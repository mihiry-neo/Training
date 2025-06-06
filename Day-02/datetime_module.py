from datetime import date, time, timedelta, timezone, datetime as dt
import datetime
from datetime import time
from datetime import timezone

print(datetime.MINYEAR)  # Minimum Year allowed is 1
print(datetime.MAXYEAR)  # Maximum year allowed is 9999

print(timezone.utc) #UTC Time Zone Singleton

# timedelta Objects
"""
A timedelta object represents a duration, the difference between two datetime or date instances.

All arguments are optional and default to 0. Arguments may be integers or floats, and may be positive or negative.

Only days, seconds and microseconds are stored internally. Arguments are converted to those units:

    A millisecond is converted to 1000 microseconds.

    A minute is converted to 60 seconds.

    An hour is converted to 3600 seconds.

    A week is converted to 7 days.

delta = datetime.timedelta(
    days=0, seconds=0,
    microseconds=0, milliseconds=0,
    minutes=0, hours=0, weeks=0
)
"""

delta = timedelta(
    days=40,
    seconds=49,
    microseconds=29,
    milliseconds=2000,
    minutes=40,
    hours=5,
    weeks=1
)  # Total time duration here is 47 days, 5:40:5.000029

print(delta)

print(timedelta.min) # Most negative timedelta object
print(timedelta.max) #Most Positive timedelta object

print(timedelta.resolution)  # Smallest Possible difference between two timedelta objects

print(delta.days) #47 days

print(delta.seconds) # 20451 seconds

print(delta.microseconds) #29

print(delta.total_seconds()) # This will give the total time difference in seconds

# date Objects
"""
A date object represents a date (year, month and day) in an idealized calendar, 
the current Gregorian calendar indefinitely extended in both directions.

class datetime.date(year, month, day)

All arguments are required. Arguments must be integers, in the following ranges:
    MINYEAR <= year <= MAXYEAR
    1 <= month <= 12
    1 <= day <= number of days in the given month and year

"""

print(date.today())  # This will give today's date
print(time.time())  # returns the current time in seconds since the Unix epoch (January 1, 1970)
print(date.fromtimestamp(time.time()))  # This will convert the unix epoch seconds into date

print(date.fromordinal(979322)) # Return the date corresponding to the proleptic Gregorian ordinal, where January 1 of year 1 has ordinal 1

date_str = '1972-12-12'
print(date.fromisoformat(date_str))  # This converts date string in ISO 8601 format to date object

year, week, day = 2025, 22, 5
print(date.fromisocalendar(year, week, day))  # This converts the date specified by year, week, day in ISO Calender format.

print(date.min) # Lowest date possible
print(date.max) # Highest date possible
print(date.resolution) # Smallest difference between two non-equal date objects


today = dt.today()
print(today)  # This will gives datetime down to milliseconds

today = dt.today().date() # This will only give the date
print(today)

print(today.year)
print(today.month)
print(today.weekday())  # Day in the current week where week starts from 0 (Monday)
print(today.day)  # Day in the month
print(today.timetuple()) # Here only the date related contents are visible as today var has only date
print(dt.today().timetuple()) # Everything is visible

newtoday = today.replace(year=today.year+2, month=today.month+3, day=today.day+4)
print(newtoday)

print(today.isocalendar())
print(today.isoformat())
print(today.isoweekday())  # iso weekdays starts from 1 (Monday)

print(today.toordinal())  # Converts todays's date to preleptic georgian ordinal

today2 = dt.today()
print(today2.ctime())  # Date in String Format

string_format = '%d/%m/%y, %H:%M:%S'
print(today2.strftime(string_format))

print(today2.tzinfo)

print(today2.fold)

print("------------------------------------")

# datetime Objects
"""
A datetime object is a single object containing all the information from a date object and a time object.
datetime.datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
The year, month and day arguments are required.

The remaining arguments must be integers in the following ranges:
    MINYEAR <= year <= MAXYEAR,
    1 <= month <= 12,
    1 <= day <= number of days in the given month and year,
    0 <= hour < 24,
    0 <= minute < 60,
    0 <= second < 60,
    0 <= microsecond < 1000000,
    fold in [0, 1].
"""

print(dt.today())

print(dt.now())

current_time_aware = dt.now(timezone(timedelta(hours=1, minutes=30)))  # IST
print(current_time_aware)

timestamp = time.time()  # Return the current time in seconds since the Epoch.
print(dt.fromtimestamp(timestamp))

print(dt.fromordinal(942373))   

random_date = dt(2020,2,21)
random_time = datetime.time(9,00)
combdate = dt.combine(random_date,random_time)
print(combdate)

print(dt.strptime(date_str, '%Y-%m-%d'))

print(dt.min)

print("-------------------------------------")

# time Objects:
"""
A time object represents a (local) time of day, independent of any particular day, 
and subject to adjustment via a tzinfo object.

datetime.time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)

All arguments are optional.
"""

print(time.min)  # Min time
print(time.max) # Max time
print(time.resolution)  # Smallest possible time difference between two non equal time objects

cur_time = datetime.time(21,49,28,33)
print(cur_time)

print(cur_time.hour)
print(cur_time.minute)
print(cur_time.second)
print(cur_time.microsecond)

ist = timezone(timedelta(hours=5, minutes=30))
t2 = time(21, 49, 28, 33, tzinfo=ist)
print(t2.tzinfo)

# Fold is used wherever the concept of Daylight Saving time is Introduced in order to distinguish the repeated time
t1 = dt(2023, 11, 5, 1, 30, fold=0)  # First 1:30 (before rollback)
t2 = dt(2023, 11, 5, 1, 30, fold=1)  # Second 1:30 (after rollback)

print(t1.fold)  # Output: 0
print(t2.fold)  # Output: 1

print(time.fromisoformat('04:23:01'))

print(cur_time.replace(hour=cur_time.hour+2, minute=cur_time.minute+9, second=cur_time.second+22,
    microsecond=cur_time.microsecond+56, tzinfo=cur_time.tzinfo, fold=0))

time_format = "%H:%M %p"
print(cur_time.strftime(time_format) ) # Outputs: '21:49 AM'


