from accelo_mlops.utils.constants import TZ
import datetime as dt
import pytz
import functools
import time
import logging
_logger = logging.getLogger(__name__)


__all__ = ['get_timestamp', 'get_now', 'get_now_hour', 'get_total_time', 'get_formatted_time', 'get_delta',
           'get_start_end_time', 'convert_local_timezone', 'timestamp_to_datetime', 'get_dateformat']


def get_timestamp(date=None, unit='ns'):
    now = dt.datetime.now() if not date else date
    ts = dt.datetime.timestamp(now)
    unit_map = dict(ns=int(ts*1e9),
                    us=int(ts*1e6),
                    ms=int(ts*1e3),
                    s=int(ts))
    return unit_map[unit]


def get_now(date=None, datetype='ds', unit='ns'):
    now = dt.datetime.now() if not date else date
    utc = pytz.timezone(TZ)
    now = now.astimezone(utc)
    if datetype == 'epoch':
        return get_timestamp(date=now, unit=unit)
    else:
        return now


def get_now_hour(date=None):
    now = get_now() if not date else date
    return now.hour


def get_delta(date=None, **params):
    now = get_now() if not date else get_now(date)
    return now - dt.timedelta(**params)


def get_formatted_time(date, fmt):
    return date.strftime(fmt)


def get_total_time(recent, old, unit='s'):
    try:
        recent = recent.replace(tzinfo=None)
    except Exception as e:
        _logger.debug(str(e))

    try:
        old = old.replace(tzinfo=None)
    except Exception as e:
        _logger.debug(str(e))

    delta = recent - old
    return delta.total_seconds() / 60 if unit == 'm' else delta.total_seconds()


def convert_local_timezone(series, time_index=False):
    return series.tz_convert('UTC') if not time_index else series.tz_convert(None)


def timestamp_to_datetime(t, unit='ns'):
    """
    The unit param specifies what the unit of the input 't' is not the output unit. The return is
    going to be
    """
    if unit == 'ms':
        t /= 1e3
    elif unit == 'us':
        t /= 1e6
    elif unit == 'ns':
        t /= 1e9
    return dt.datetime.fromtimestamp(t) #utcfromtimestamp(t)


def get_start_end_time(now, period, param='d'):
    if param == 'h':
        start_delta = get_delta(date=now, hours=period)
    elif param == 'm':
        start_delta = get_delta(date=now, minutes=period)
    elif param == 's':
        start_delta = get_delta(date=now, seconds=period)
    else:
        start_delta = get_delta(date=now, days=period)
    end_delta = get_delta(date=now, minutes=1)
    start_time = get_timestamp(start_delta, unit='ms')
    end_time = get_timestamp(end_delta, unit='ms')
    return start_time, end_time


def get_dateformat(fmt='%Y.%m.%d'):
    """Returns a string in the requested format"""
    return dt.datetime.now().strftime(fmt)


def timeit(func):
    """Decorator function to time the function it decorates"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        _logger.debug(f'{func.__name__}() took: {round(t2-t1,2)} seconds.')
        return result
    return wrapper
