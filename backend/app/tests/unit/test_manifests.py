"""Tests for Module Manifest system — Schema, Validator, Loader, Discovery."""

import sys
from pathlib import Path

import pytest
import yaml

# Add tools directory to path
TOOLS_DIR = Path(__file__).parent.parent.parent.parent.parent / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from manifest_loader import ManifestLoader, ModuleManifest, ResolvedPath
from manifest_validator import (
    validate_manifest_version,
    validate_required_fields,
    validate_coherence,
    validate_adr_references,
    validate_uniqueness,
)

MANIFESTS_DIR = Path(__file__).parent.parent.parent.parent.parent / "backend" / "architecture" / "manifests"
APP_DIR = Path(__file__).parent.parent


# ============================================================
# Manifest Schema Tests
# ============================================================

class TestManifestSchema:
    """Validate manifest YAML structure."""

    def test_manifests_directory_exists(self):
        assert MANIFESTS_DIR.exists()
        assert MANIFESTS_DIR.is_dir()

    def test_all_manifests_are_valid_yaml(self):
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            assert data is not None, f"Empty YAML: {mf}"

    def test_all_manifests_have_version(self):
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            assert "manifest_version" in data, f"Missing manifest_version in {mf}"

    def test_all_manifests_have_required_fields(self):
        required = ["manifest_version", "module_id", "module", "ownership",
                     "stability", "lifecycle", "capabilities", "validation_profile"]
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            for field in required:
                assert field in data, f"Missing {field} in {mf}"

    def test_module_id_format(self):
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            module_id = data.get("module_id", "")
            assert "." in module_id, f"module_id must have '.' separator in {mf}"

    def test_module_has_required_subfields(self):
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            module = data.get("module", {})
            for field in ["canonical_name", "storage_name", "storage_table"]:
                assert field in module, f"Missing module.{field} in {mf}"

    def test_ownership_has_required_subfields(self):
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            ownership = data.get("ownership", {})
            for field in ["aggregate", "bounded_context"]:
                assert field in ownership, f"Missing ownership.{field} in {mf}"

    def test_lifecycle_has_states(self):
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            lifecycle = data.get("lifecycle", {})
            assert "states" in lifecycle, f"Missing lifecycle.states in {mf}"
            assert "initial_state" in lifecycle, f"Missing lifecycle.initial_state in {mf}"
            assert "terminal_states" in lifecycle, f"Missing lifecycle.terminal_states in {mf}"

    def test_capabilities_have_required_keys(self):
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            caps = data.get("capabilities", {})
            for cap in ["model", "repository", "repository_interface", "service", "router"]:
                assert cap in caps, f"Missing capabilities.{cap} in {mf}"
            assert "dtos" in caps, f"Missing capabilities.dtos in {mf}"
            assert "tests" in caps, f"Missing capabilities.tests in {mf}"


# ============================================================
# Manifest Validator Tests
# ============================================================

class TestManifestValidator:
    """Test manifest validation logic."""

    def _load_manifest(self, name: str) -> dict:
        path = MANIFESTS_DIR / f"{name}.yaml"
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def test_valid_version(self):
        data = self._load_manifest("doctor")
        errors = validate_manifest_version(data, "doctor")
        assert len(errors) == 0

    def test_invalid_version(self):
        data = {"manifest_version": 99}
        errors = validate_manifest_version(data, "test")
        assert len(errors) > 0

    def test_missing_version(self):
        data = {}
        errors = validate_manifest_version(data, "test")
        assert len(errors) > 0

    def test_required_fields_present(self):
        data = self._load_manifest("doctor")
        errors = validate_required_fields(data, "doctor")
        assert len(errors) == 0

    def test_coherence_valid(self):
        data = self._load_manifest("doctor")
        errors = validate_coherence(data, "doctor")
        assert len(errors) == 0

    def test_coherence_invalid_initial_state(self):
        data = self._load_manifest("doctor")
        data["lifecycle"]["initial_state"] = "nonexistent"
        errors = validate_coherence(data, "doctor")
        assert any("initial_state" in e.field for e in errors)

    def test_adr_references_valid(self):
        data = self._load_manifest("doctor")
        errors = validate_adr_references(data, "doctor")
        assert len(errors) == 0

    def test_uniqueness_no_duplicates(self):
        all_data = {}
        for mf in MANIFESTS_DIR.glob("*.yaml"):
            with open(mf, encoding="utf-8") as f:
                all_data[mf.stem] = yaml.safe_load(f)
        warnings = validate_uniqueness([], all_data)
        assert len(warnings) == 0


# ============================================================
# Manifest Loader Tests
# ============================================================

class TestManifestLoader:
    """Test manifest loading and resolution."""

    def test_discover_finds_all_manifests(self):
        loader = ManifestLoader()
        names = loader.discover()
        assert len(names) == 5
        assert "doctor" in names
        assert "period" in names
        assert "shift" in names
        assert "assignment" in names
        assert "extra" in names

    def test_load_all_returns_all_manifests(self):
        loader = ManifestLoader()
        manifests = loader.load_all()
        assert len(manifests) == 5

    def test_get_by_name(self):
        loader = ManifestLoader()
        manifest = loader.get("doctor")
        assert manifest is not None
        assert manifest.canonical_name == "Doctor"

    def test_get_by_canonical_name(self):
        loader = ManifestLoader()
        manifest = loader.get_by_canonical_name("Assignment")
        assert manifest is not None
        assert manifest.module_id == "scheduling.assignment"

    def test_get_by_storage_name(self):
        loader = ManifestLoader()
        manifest = loader.get_by_storage_name("shift_part")
        assert manifest is not None
        assert manifest.canonical_name == "Assignment"

    def test_get_by_module_id(self):
        loader = ManifestLoader()
        manifest = loader.get_by_module_id("scheduling.shift")
        assert manifest is not None
        assert manifest.canonical_name == "Shift"

    def test_module_properties(self):
        loader = ManifestLoader()
        manifest = loader.get("shift")
        assert manifest.canonical_name == "Shift"
        assert manifest.storage_name == "shift"
        assert manifest.storage_table == "shifts"
        assert manifest.aggregate == "Shift"
        assert manifest.bounded_context == "Scheduling"
        assert manifest.stability_level == "stable"
        assert manifest.validation_profile == "enterprise"

    def test_has_capability(self):
        loader = ManifestLoader()
        manifest = loader.get("doctor")
        assert manifest.has_capability("model") is True
        assert manifest.has_capability("state_machine") is False
        assert manifest.has_capability("tests.unit") is True

    def test_resolve_files_doctor(self):
        loader = ManifestLoader()
        manifest = loader.get("doctor")
        resolved = manifest.resolve_files()
        assert "model" in resolved
        assert "service" in resolved
        assert "router" in resolved
        assert resolved["model"].exists is True
        assert resolved["service"].exists is True

    def test_resolve_files_assignment(self):
        loader = ManifestLoader()
        manifest = loader.get("assignment")
        resolved = manifest.resolve_files()
        # Assignment uses shift_part for model but assignment for service
        assert resolved["model"].exists is True
        assert resolved["service"].exists is True
        assert resolved["router"].exists is True

    def test_resolve_files_shift(self):
        loader = ManifestLoader()
        manifest = loader.get("shift")
        resolved = manifest.resolve_files()
        assert resolved["model"].exists is True
        assert resolved["service"].exists is True
        assert resolved["state_machine"].exists is True

    def test_resolve_files_period(self):
        loader = ManifestLoader()
        manifest = loader.get("period")
        resolved = manifest.resolve_files()
        assert resolved["model"].exists is True
        assert resolved["service"].exists is True
        assert resolved["state_machine"].exists is True
        assert resolved["policy"].exists is True

    def test_aliases(self):
        loader = ManifestLoader()
        manifest = loader.get("assignment")
        aliases = manifest.aliases
        assert len(aliases) > 0
        storage_aliases = [a for a in aliases if a["type"] == "storage"]
        assert len(storage_aliases) > 0
        assert storage_aliases[0]["name"] == "shift_part"

    def test_adr_references(self):
        loader = ManifestLoader()
        manifest = loader.get("assignment")
        refs = manifest.adr_references
        assert len(refs) > 0
        assert refs[0]["id"] == "ADR-015"


# ============================================================
# Manifest Integration Tests
# ============================================================

class TestManifestIntegration:
    """Integration tests — manifests reflect actual codebase."""

    def test_all_model_files_exist(self):
        loader = ManifestLoader()
        for name in loader.discover():
            manifest = loader.get(name)
            resolved = manifest.resolve_files()
            if manifest.has_capability("model"):
                assert resolved["model"].exists, \
                    f"{manifest.canonical_name}: model declared but not found"

    def test_all_service_files_exist(self):
        loader = ManifestLoader()
        for name in loader.discover():
            manifest = loader.get(name)
            resolved = manifest.resolve_files()
            if manifest.has_capability("service"):
                assert resolved["service"].exists, \
                    f"{manifest.canonical_name}: service declared but not found"

    def test_all_router_files_exist(self):
        loader = ManifestLoader()
        for name in loader.discover():
            manifest = loader.get(name)
            resolved = manifest.resolve_files()
            if manifest.has_capability("router"):
                assert resolved["router"].exists, \
                    f"{manifest.canonical_name}: router declared but not found"

    def test_all_state_machine_files_exist(self):
        loader = ManifestLoader()
        for name in loader.discover():
            manifest = loader.get(name)
            resolved = manifest.resolve_files()
            if manifest.has_capability("state_machine"):
                assert resolved["state_machine"].exists, \
                    f"{manifest.canonical_name}: state_machine declared but not found"

    def test_all_policy_files_exist(self):
        loader = ManifestLoader()
        for name in loader.discover():
            manifest = loader.get(name)
            resolved = manifest.resolve_files()
            if manifest.has_capability("policy"):
                assert resolved["policy"].exists, \
                    f"{manifest.canonical_name}: policy declared but not found"

    def test_lifecycle_states_are_consistent(self):
        loader = ManifestLoader()
        for name in loader.discover():
            manifest = loader.get(name)
            states = manifest.lifecycle_states
            initial = manifest.data.get("lifecycle", {}).get("initial_state")
            terminals = manifest.data.get("lifecycle", {}).get("terminal_states", [])
            assert initial in states, \
                f"{manifest.canonical_name}: initial_state '{initial}' not in states"
            for t in terminals:
                assert t in states, \
                    f"{manifest.canonical_name}: terminal_state '{t}' not in states"
