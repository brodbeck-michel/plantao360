from app.common.pagination import Page


def test_page_defaults():
    page = Page[int]()
    assert page.page == 1
    assert page.size == 20
    assert page.total == 0
    assert page.pages == 0


def test_page_calculation():
    page = Page[int](items=[1, 2, 3], page=1, size=10, total=25)
    assert page.pages == 3
    assert page.has_next is True
    assert page.has_previous is False


def test_page_last():
    page = Page[int](items=[1], page=3, size=10, total=25)
    assert page.has_next is False
    assert page.has_previous is True


def test_page_to_dict():
    page = Page[int](items=[1, 2], page=1, size=10, total=2)
    d = page.to_dict()
    assert "items" in d
    assert "page" in d
    assert "size" in d
    assert "total" in d
    assert "pages" in d
