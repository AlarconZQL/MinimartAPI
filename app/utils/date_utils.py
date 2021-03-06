import calendar
from datetime import date
from app.utils.days import Days


class DateUtils:
    @staticmethod
    def today_is_between_dates(date_one, date_two):
        """Checks if today's date is included between the two dates received
        as parameters"""
        if date_one <= date_two:
            start_date = date_one
            end_date = date_two
        else:
            start_date = date_two
            end_date = date_one
        return start_date <= date.today() <= end_date

    @staticmethod
    def today_is_included_on_voucherdays(weekdays):
        """Checks if today's week day applies for valid week days of a
        discount voucher"""
        current_weekday = calendar.day_name[date.today().weekday()]
        weekday_names = list(
            map(lambda weekday: weekday.day.name, weekdays))
        return current_weekday in weekday_names
