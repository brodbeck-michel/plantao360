def test_app_import():
    from app.api.app import create_app

    app = create_app()
    assert app.title == "Plantao360"


def test_main_import():
    from app.main import app

    assert app.title == "Plantao360"
