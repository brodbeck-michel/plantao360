from app.common.query.pagination import PaginationQuery
from app.common.query.sorting import SortingQuery


def test_pagination_query_defaults():
    q = PaginationQuery()
    assert q.page == 1
    assert q.size == 20
    assert q.offset == 0


def test_pagination_query_clamp():
    q = PaginationQuery(page=0, size=0)
    assert q.page == 1
    assert q.size == 1


def test_pagination_query_max():
    q = PaginationQuery(size=200)
    assert q.size == 100


def test_pagination_query_offset():
    q = PaginationQuery(page=3, size=10)
    assert q.offset == 20


def test_sorting_query_defaults():
    q = SortingQuery()
    assert q.field == "id"
    assert q.direction == "asc"


def test_sorting_query_invalid():
    q = SortingQuery(direction="invalid")
    assert q.direction == "asc"
