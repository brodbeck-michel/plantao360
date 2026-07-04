from __future__ import annotations

from datetime import date, timedelta


class BusinessCalendar:
    def current_business_day(self, reference: date | None = None) -> date:
        d = reference or date.today()
        while not self.is_business_day(d):
            d += timedelta(days=1)
        return d

    def is_business_day(self, d: date) -> bool:
        return d.weekday() < 5

    def next_business_day(self, d: date) -> date:
        nxt = d + timedelta(days=1)
        while not self.is_business_day(nxt):
            nxt += timedelta(days=1)
        return nxt

    def previous_business_day(self, d: date) -> date:
        prev = d - timedelta(days=1)
        while not self.is_business_day(prev):
            prev -= timedelta(days=1)
        return prev

    def first_business_day(self, year: int, month: int) -> date:
        d = date(year, month, 1)
        while not self.is_business_day(d):
            d += timedelta(days=1)
        return d

    def last_business_day(self, year: int, month: int) -> date:
        if month == 12:
            d = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            d = date(year, month + 1, 1) - timedelta(days=1)
        while not self.is_business_day(d):
            d -= timedelta(days=1)
        return d
