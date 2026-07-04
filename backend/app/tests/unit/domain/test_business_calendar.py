import pytest
from datetime import date
from app.domain.calendar.business_calendar import BusinessCalendar


class TestBusinessCalendar:
    def setup_method(self):
        self.cal = BusinessCalendar()

    def test_is_business_day_weekday(self):
        monday = date(2026, 6, 29)
        assert self.cal.is_business_day(monday)

    def test_is_business_day_saturday(self):
        saturday = date(2026, 6, 27)
        assert not self.cal.is_business_day(saturday)

    def test_is_business_day_sunday(self):
        sunday = date(2026, 6, 28)
        assert not self.cal.is_business_day(sunday)

    def test_next_business_day_from_friday(self):
        friday = date(2026, 6, 26)
        assert self.cal.next_business_day(friday) == date(2026, 6, 29)

    def test_next_business_day_from_saturday(self):
        saturday = date(2026, 6, 27)
        assert self.cal.next_business_day(saturday) == date(2026, 6, 29)

    def test_previous_business_day_from_monday(self):
        monday = date(2026, 6, 29)
        assert self.cal.previous_business_day(monday) == date(2026, 6, 26)

    def test_previous_business_day_from_sunday(self):
        sunday = date(2026, 6, 28)
        assert self.cal.previous_business_day(sunday) == date(2026, 6, 26)

    def test_first_business_day_june_2026(self):
        assert self.cal.first_business_day(2026, 6) == date(2026, 6, 1)

    def test_first_business_day_march_2026(self):
        assert self.cal.first_business_day(2026, 3) == date(2026, 3, 2)

    def test_last_business_day_june_2026(self):
        assert self.cal.last_business_day(2026, 6) == date(2026, 6, 30)

    def test_last_business_day_december_2026(self):
        assert self.cal.last_business_day(2026, 12) == date(2026, 12, 31)

    def test_current_business_day_on_weekday(self):
        tuesday = date(2026, 6, 30)
        assert self.cal.current_business_day(tuesday) == tuesday

    def test_current_business_day_on_weekend(self):
        saturday = date(2026, 6, 27)
        assert self.cal.current_business_day(saturday) == date(2026, 6, 29)
