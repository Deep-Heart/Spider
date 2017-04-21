import time
from datetime import datetime, timedelta

from nanotime import nanotime


class TimeUtils(object):
    DAY_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def get_today():
        return time.strftime(TimeUtils.DAY_FORMAT, time.localtime())

    @staticmethod
    def get_cur_time():
        return time.strftime(TimeUtils.TIME_FORMAT, time.localtime())

    @staticmethod
    def get_time():
        return datetime.now()

    @staticmethod
    def get_microsecond():
        return datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')

    @staticmethod
    def get_timestamp():
        return int(datetime.now().timestamp() * 1000000)

    @staticmethod
    def get_nanoseconds():
        return nanotime.now().nanoseconds()

    @staticmethod
    def get_yesterday():
        return TimeUtils.get_yesterday_format(TimeUtils.DAY_FORMAT)

    @staticmethod
    def get_yesterday_format(time_format):
        return datetime.strftime(datetime.now() - timedelta(days=1), time_format)

    @staticmethod
    def get_timedelta(start, end):
        return TimeUtils.get_datetime(end) - TimeUtils.get_datetime(start)

    @staticmethod
    def get_datetime(start):
        if isinstance(start, int):
            start_time = datetime(start)
        elif isinstance(start, str):
            start_time = datetime.strptime(start, TimeUtils.TIME_FORMAT)
        else:
            start_time = datetime.strftime(start, TimeUtils.TIME_FORMAT)

        return start_time


class ObjectUtils(object):
    @staticmethod
    def create_instance(class_name, *args, **kwargs):
        (module_name, class_name) = class_name.rsplit('.', 1)
        module_meta = __import__(module_name, globals(), locals(), [class_name])
        class_meta = getattr(module_meta, class_name)
        return class_meta(*args, **kwargs)
