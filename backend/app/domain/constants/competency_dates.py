from datetime import date


def get_competency_dates(year: int, month: int) -> tuple[date, date]:
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1

    start_date = date(year, month, 26)
    end_date = date(next_year, next_month, 25)
    return start_date, end_date
