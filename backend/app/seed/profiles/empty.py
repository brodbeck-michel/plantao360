"""Empty profile — clears all data, no insertion."""


def generate_data() -> dict:
    """Return empty dataset — used for clearing the database."""
    return {"doctors": [], "periods": [], "shifts": [], "extras": []}
