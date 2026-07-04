"""Demo profile — realistic dataset for demonstration."""


def generate_data() -> dict:
    """Generate demo dataset: 35 doctors, 6 months, ~60 shifts."""
    from app.seed.seed_data import generate_demo_data

    return generate_demo_data()
