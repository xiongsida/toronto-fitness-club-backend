import datetime
import pytz


def user_has_x(user, x):
    return hasattr(user, x) and getattr(user, x) != None


def get_now2utc():
    return datetime.datetime.utcnow()


def dbtime2utc(dt):
    return dt.replace(tzinfo=None)


def utc2dbtime(dt):
    return dt.replace(tzinfo=pytz.UTC)
