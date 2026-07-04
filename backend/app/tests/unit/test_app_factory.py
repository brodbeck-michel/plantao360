from app.api.app import create_app


def test_create_app_returns_fastapi():
    app = create_app()
    assert app is not None
    assert app.title == "Plantao360"


def test_main_module_importable():
    from app.main import app

    assert app is not None
    assert app.title == "Plantao360"
