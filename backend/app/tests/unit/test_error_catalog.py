from app.domain.errors.error_catalog import ERROR_MESSAGES
from app.domain.constants.business_rule_code import BusinessRuleCode


def test_error_catalog_has_all_rules():
    for rule in BusinessRuleCode:
        assert rule in ERROR_MESSAGES, f"Missing error message for {rule}"


def test_error_catalog_messages_are_strings():
    for rule, message in ERROR_MESSAGES.items():
        assert isinstance(message, str), f"Message for {rule} is not a string"
        assert len(message) > 0, f"Message for {rule} is empty"


def test_error_catalog_count():
    assert len(ERROR_MESSAGES) == 6


def test_specific_messages():
    assert "médico" in ERROR_MESSAGES[BusinessRuleCode.RN_01_SHIFT_REQUIRES_DOCTOR]
    assert "sobreposição" in ERROR_MESSAGES[BusinessRuleCode.RN_03_NO_OVERLAPPING]
    assert "justificativa" in ERROR_MESSAGES[BusinessRuleCode.RN_04_EXTRA_REQUIRES_JUSTIFICATION]
