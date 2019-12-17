from instance.config import Config as cfg
import datetime


class DatetimeFormatter:

    def get_str_from_datetime(self, date_time):
        string_datetime = date_time.strftime(cfg.DATETIME_FORMAT)
        return string_datetime

    def get_datetime_with_timezone(self):
        return datetime.datetime. \
            now(datetime.timezone(datetime.timedelta(0))).astimezone()
