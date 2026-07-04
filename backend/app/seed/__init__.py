"""Seed module for Plantão 360 — unified CLI.

Usage:
    python -m app.seed run demo
    python -m app.seed run demo --clear
    python -m app.seed run development --clear
    python -m app.seed run edge --clear
    python -m app.seed run empty

Backward compatibility:
    python -m app.seed --dataset demo --clear
    python -m app.seed --dataset edge_cases --clear
    python -m app.seed --dataset showcase --clear
"""

import argparse
import sys

from app.seed.profiles import get_profile, AVAILABLE_PROFILES
from app.seed.seed_data import populate_database


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        _run_profile(sys.argv[2:])
    else:
        _run_legacy()


def _run_profile(args: list):
    """New CLI: python -m app.seed run <profile> [--clear]"""
    parser = argparse.ArgumentParser(
        description="Plantão 360 Seed Data",
        prog="python -m app.seed run",
    )
    parser.add_argument(
        "profile",
        choices=AVAILABLE_PROFILES,
        help="Profile to load",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear database before loading",
    )
    parsed = parser.parse_args(args)

    profile = get_profile(parsed.profile)
    data = profile.generate_data()
    populate_database(data, clear=parsed.clear)


def _run_legacy():
    """Backward compatibility: python -m app.seed --dataset <dataset> [--clear]"""
    parser = argparse.ArgumentParser(
        description="Plantão 360 Seed Data",
        prog="python -m app.seed",
    )
    parser.add_argument(
        "--dataset",
        choices=["demo", "edge_cases", "showcase"],
        help="Dataset to load (backward compatibility)",
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear database before loading",
    )
    args = parser.parse_args()

    if not args.dataset:
        parser.print_help()
        return

    profile_map = {
        "demo": "demo",
        "edge_cases": "edge",
        "showcase": "demo",
    }
    profile_name = profile_map.get(args.dataset, args.dataset)

    profile = get_profile(profile_name)
    data = profile.generate_data()
    populate_database(data, clear=args.clear)


if __name__ == "__main__":
    main()
