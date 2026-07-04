"""Edge cases profile — boundary condition scenarios."""


def generate_data() -> dict:
    """Generate edge cases dataset."""
    from app.seed.seed_data import generate_edge_cases_data

    return generate_edge_cases_data()
