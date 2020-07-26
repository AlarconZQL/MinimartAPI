import calendar
from datetime import date, timedelta
from app.tests import BaseTestClass
from app.utils import DateUtils, Days
from app.models import VoucherDay


class DateUtilsTestCase(BaseTestClass):

    def test_today_is_between_dates(self):
        date_one = date.today() - timedelta(days=2)
        date_two = date.today() + timedelta(days=2)
        res = DateUtils.today_is_between_dates(date_one, date_two)
        self.assertTrue(res)
        date_two = date.today() - timedelta(days=4)
        res = DateUtils.today_is_between_dates(date_one, date_two)
        self.assertFalse(res)

    def test_today_is_included_on_voucherdays(self):
        today_weekday = calendar.day_name[date.today().weekday()]
        weekdays = [VoucherDay(day=Days[today_weekday])]
        res = DateUtils.today_is_included_on_voucherdays(weekdays)
        self.assertTrue(res)
