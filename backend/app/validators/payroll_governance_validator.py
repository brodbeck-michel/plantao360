"""Payroll governance validator."""

from app.validators.base_validator import BaseValidator, ValidationResult
from app.domain.payroll.governance import ChecklistItemStatus


class PayrollGovernanceValidator(BaseValidator):
    """Validates governance operations for payroll competencies."""

    def _validate_approval(self, data: dict, result: ValidationResult) -> None:
        """Validate approval request data."""
        if not data.get("justification"):
            result.add_error("Justificativa é obrigatória para aprovação")
        elif len(data["justification"]) < 1:
            result.add_error("Justificativa deve ter pelo menos 1 caractere")

        if not data.get("approved_by"):
            result.add_error("Responsável pela aprovação é obrigatório")

    def _validate_lock(self, data: dict, result: ValidationResult) -> None:
        """Validate lock request data."""
        if not data.get("locked_by"):
            result.add_error("Responsável pelo bloqueio é obrigatório")

    def _validate_unlock(self, data: dict, result: ValidationResult) -> None:
        """Validate unlock request data."""
        if not data.get("unlocked_by"):
            result.add_error("Responsável pelo desbloqueio é obrigatório")
        if not data.get("justification"):
            result.add_error("Justificativa é obrigatória para desbloqueio")
        elif len(data["justification"]) < 10:
            result.add_error("Justificativa deve ter pelo menos 10 caracteres")

    def _validate_checklist_item(self, data: dict, result: ValidationResult) -> None:
        """Validate checklist item update data."""
        if not data.get("item_id"):
            result.add_error("ID do item é obrigatório")

        valid_statuses = {"satisfied", "not_satisfied", "waived"}
        status = data.get("status")
        if status not in valid_statuses:
            result.add_error(f"Status inválido. Valores aceitos: {valid_statuses}")

        if status == "waived" and not data.get("justification"):
            result.add_error("Justificativa é obrigatória para dispensa de item")

        if status == "waived" and data.get("justification") and len(data["justification"]) < 10:
            result.add_error("Justificativa deve ter pelo menos 10 caracteres para dispensa")
