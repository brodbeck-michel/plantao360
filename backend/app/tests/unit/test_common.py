from app.common.pagination import Page


def test_page_defaults():
    p = Page()
    assert p.page == 1
    assert p.size == 20
    assert p.total == 0
    assert p.items == []


def test_page_pages_calculation():
    p = Page(items=[1, 2, 3], page=1, size=10, total=25)
    assert p.pages == 3


def test_page_has_next():
    p = Page(page=1, size=10, total=25)
    assert p.has_next is True


def test_page_has_previous():
    p = Page(page=2, size=10, total=25)
    assert p.has_previous is True


def test_page_to_dict():
    p = Page(items=["a"], page=1, size=10, total=1)
    d = p.to_dict()
    assert "items" in d
    assert "page" in d
    assert "size" in d
    assert "total" in d
    assert "pages" in d
