#!/usr/bin/env python3
"""
Manifest Loader — Resolves capabilities to file paths.

Core component that loads manifests and provides a uniform API
for all governance tools. Resolves architectural capabilities
to actual file paths in the codebase.

Usage:
    from tools.manifest_loader import ManifestLoader

    loader = ManifestLoader()
    manifest = loader.get("assignment")
    files = manifest.resolve_files(APP_DIR)
"""

import re
import sys
from pathlib import Path
from dataclasses import dataclass, field
from functools import lru_cache

import yaml

ARCHITECTURE_DIR = Path(__file__).parent.parent / "backend" / "architecture"
MANIFESTS_DIR = ARCHITECTURE_DIR / "manifests"
BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"


@dataclass
class ResolvedPath:
    capability: str
    path: Path
    exists: bool


@dataclass
class ModuleManifest:
    """Represents a loaded and validated module manifest."""
    data: dict
    manifest_path: Path

    @property
    def module_id(self) -> str:
        return self.data.get("module_id", "")

    @property
    def canonical_name(self) -> str:
        return self.data.get("module", {}).get("canonical_name", "")

    @property
    def storage_name(self) -> str:
        return self.data.get("module", {}).get("storage_name", "")

    @property
    def storage_table(self) -> str:
        return self.data.get("module", {}).get("storage_table", "")

    @property
    def aggregate(self) -> str:
        return self.data.get("ownership", {}).get("aggregate", "")

    @property
    def bounded_context(self) -> str:
        return self.data.get("ownership", {}).get("bounded_context", "")

    @property
    def stability_level(self) -> str:
        return self.data.get("stability", {}).get("level", "")

    @property
    def adr_references(self) -> list[dict]:
        return self.data.get("adr_references", [])

    @property
    def validation_profile(self) -> str:
        return self.data.get("validation_profile", "enterprise")

    @property
    def lifecycle_states(self) -> list[str]:
        return self.data.get("lifecycle", {}).get("states", [])

    @property
    def aliases(self) -> list[dict]:
        return self.data.get("aliases", [])

    def has_capability(self, capability: str) -> bool:
        caps = self.data.get("capabilities", {})
        if "." in capability:
            parts = capability.split(".")
            return caps.get(parts[0], {}).get(parts[1], False)
        return caps.get(capability, False)

    def _resolve_storage_name(self) -> str:
        """Resolve the actual storage name for file path resolution."""
        storage_name = self.data.get("module", {}).get("storage_name", "")
        canonical = self.data.get("module", {}).get("canonical_name", "")

        if canonical and canonical != storage_name:
            # Check if files exist with canonical name first
            test_path = APP_DIR / "models" / f"{canonical.lower()}.py"
            if test_path.exists():
                return canonical.lower()
            # Fall back to storage_name
            return storage_name
        return storage_name

    def _resolve_file_path(self, subdir: str, filename: str, app_dir: Path) -> Path:
        """Try to find file with canonical name first, then storage name, then plural."""
        canonical = self.data.get("module", {}).get("canonical_name", "").lower()
        storage = self.data.get("module", {}).get("storage_name", "")

        # Try with the filename as-is first
        path = app_dir / subdir / filename
        if path.exists():
            return path

        # Try plural form for router
        if subdir == "api/routes" and not filename.endswith("s.py"):
            plural_path = app_dir / subdir / f"{filename[:-3]}s.py"
            if plural_path.exists():
                return plural_path

        # Try replacing storage name with canonical name in filename
        if storage and canonical != storage:
            alt_filename = filename.replace(storage, canonical)
            alt_path = app_dir / subdir / alt_filename
            if alt_path.exists():
                return alt_path
            # Try plural of canonical
            if subdir == "api/routes":
                plural_alt = app_dir / subdir / f"{alt_filename[:-3]}s.py"
                if plural_alt.exists():
                    return plural_alt

        # Try replacing canonical name with storage name in filename
        if storage and canonical != storage:
            alt_filename = filename.replace(canonical, storage)
            alt_path = app_dir / subdir / alt_filename
            if alt_path.exists():
                return alt_path
            # Try plural of storage
            if subdir == "api/routes":
                plural_alt = app_dir / subdir / f"{alt_filename[:-3]}s.py"
                if plural_alt.exists():
                    return plural_alt

        return path  # Return original path (won't exist)

    def resolve_files(self, app_dir: Path | None = None) -> dict[str, ResolvedPath]:
        """Resolve all capabilities to actual file paths."""
        if app_dir is None:
            app_dir = APP_DIR

        resolved = {}
        snake = self._resolve_storage_name()
        canonical = self.data.get("module", {}).get("canonical_name", "").lower()

        # Core layer files
        file_map = {
            "model": ("models", f"{snake}.py"),
            "repository": ("repositories", f"{snake}_repository.py"),
            "repository_interface": ("repositories/interfaces", f"{snake}_repository.py"),
            "service": ("services", f"{snake}_service.py"),
            "mapper": ("mappers", f"{snake}_mapper.py"),
            "validator": ("validators", f"{snake}_validator.py"),
            "router": ("api/routes", f"{snake}.py"),
        }

        for cap, (subdir, filename) in file_map.items():
            if self.has_capability(cap):
                path = self._resolve_file_path(subdir, filename, app_dir)
                resolved[cap] = ResolvedPath(capability=cap, path=path, exists=path.exists())

        # Domain layer files
        domain_map = {
            "state_machine": ("domain/state_machines", f"{snake}_state_machine.py"),
            "policy": ("domain/policies", f"{snake}_policy.py"),
            "events": ("domain/events", "event_names.py"),
            "contracts": ("domain/contracts", f"{snake}_contracts.py"),
            "value_objects": ("domain/value_objects", None),  # Directory check
        }

        for cap, (subdir, filename) in domain_map.items():
            if self.has_capability(cap):
                if filename:
                    path = self._resolve_file_path(subdir, filename, app_dir)
                else:
                    path = app_dir / subdir
                resolved[cap] = ResolvedPath(capability=cap, path=path, exists=path.exists())

        # Error codes
        if self.has_capability("model"):
            errors_path = self._resolve_file_path("domain/errors", f"{snake}_errors.py", app_dir)
            resolved["error_codes"] = ResolvedPath(
                capability="error_codes", path=errors_path, exists=errors_path.exists()
            )

        # DTOs
        dtos = self.data.get("capabilities", {}).get("dtos", {})
        schemas_dir = app_dir / "schemas" / snake
        # Also check with canonical name
        if not schemas_dir.exists() and canonical != snake:
            schemas_dir = app_dir / "schemas" / canonical
        for dto_type, enabled in dtos.items():
            if enabled:
                dto_path = schemas_dir / f"{snake}_{dto_type}.py"
                if not dto_path.exists() and canonical != snake:
                    dto_path = app_dir / "schemas" / canonical / f"{canonical}_{dto_type}.py"
                resolved[f"dto_{dto_type}"] = ResolvedPath(
                    capability=f"dto_{dto_type}", path=dto_path, exists=dto_path.exists()
                )

        # Tests
        tests = self.data.get("capabilities", {}).get("tests", {})
        for test_type, enabled in tests.items():
            if enabled:
                test_dir = app_dir / "tests" / test_type
                if test_dir.exists():
                    # Try both storage name and canonical name
                    test_files = list(test_dir.glob(f"test_{snake}_*.py"))
                    if not test_files and canonical != snake:
                        test_files = list(test_dir.glob(f"test_{canonical}_*.py"))
                    resolved[f"test_{test_type}"] = ResolvedPath(
                        capability=f"test_{test_type}",
                        path=test_dir,
                        exists=len(test_files) > 0
                    )
                else:
                    resolved[f"test_{test_type}"] = ResolvedPath(
                        capability=f"test_{test_type}",
                        path=test_dir,
                        exists=False
                    )

        return resolved

    def check_capability_exists(self, capability: str, app_dir: Path | None = None) -> bool:
        """Check if a capability's files actually exist."""
        resolved = self.resolve_files(app_dir)
        if capability in resolved:
            return resolved[capability].exists
        return False


class ManifestLoader:
    """Loads and caches module manifests. Provides discovery and lookup."""

    def __init__(self, manifests_dir: Path | None = None):
        self.manifests_dir = manifests_dir or MANIFESTS_DIR
        self._cache: dict[str, ModuleManifest] = {}

    def _load_manifest(self, path: Path) -> ModuleManifest | None:
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data is None:
                return None
            return ModuleManifest(data=data, manifest_path=path)
        except Exception:
            return None

    def discover(self) -> list[str]:
        """Discover all manifest names from the manifests directory."""
        if not self.manifests_dir.exists():
            return []
        names = []
        for f in sorted(self.manifests_dir.glob("*.yaml")):
            if f.name.startswith("_"):
                continue
            names.append(f.stem)
        return names

    def load_all(self) -> dict[str, ModuleManifest]:
        """Load all discovered manifests."""
        if self._cache:
            return self._cache

        for name in self.discover():
            path = self.manifests_dir / f"{name}.yaml"
            manifest = self._load_manifest(path)
            if manifest:
                self._cache[name] = manifest

        return self._cache

    def get(self, name: str) -> ModuleManifest | None:
        """Get a manifest by name (filename stem)."""
        if name in self._cache:
            return self._cache[name]

        path = self.manifests_dir / f"{name}.yaml"
        if path.exists():
            manifest = self._load_manifest(path)
            if manifest:
                self._cache[name] = manifest
                return manifest

        return None

    def get_by_canonical_name(self, canonical_name: str) -> ModuleManifest | None:
        """Find manifest by canonical_name (e.g., 'Assignment')."""
        for name, manifest in self.load_all().items():
            if manifest.canonical_name == canonical_name:
                return manifest
        return None

    def get_by_storage_name(self, storage_name: str) -> ModuleManifest | None:
        """Find manifest by storage_name (e.g., 'shift_part')."""
        for name, manifest in self.load_all().items():
            if manifest.storage_name == storage_name:
                return manifest
        return None

    def get_by_module_id(self, module_id: str) -> ModuleManifest | None:
        """Find manifest by module_id (e.g., 'scheduling.assignment')."""
        for name, manifest in self.load_all().items():
            if manifest.module_id == module_id:
                return manifest
        return None

    def clear_cache(self):
        """Clear the manifest cache."""
        self._cache.clear()
