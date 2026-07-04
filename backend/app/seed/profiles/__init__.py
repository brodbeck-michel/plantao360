"""Seed profiles for Plantão 360."""

from . import demo, development, edge_cases, empty

PROFILES = {
    "demo": demo,
    "development": development,
    "edge": edge_cases,
    "empty": empty,
}

AVAILABLE_PROFILES = list(PROFILES.keys())


def get_profile(name: str):
    """Get a profile module by name."""
    if name not in PROFILES:
        raise ValueError(
            f"Unknown profile: {name}. Available: {', '.join(AVAILABLE_PROFILES)}"
        )
    return PROFILES[name]
