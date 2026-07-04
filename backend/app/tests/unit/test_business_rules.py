from app.domain.rules.business_rules import BusinessRuleCode


def test_business_rule_code_values():
    values = BusinessRuleCode.values()
    assert "RN_01" in values
    assert "RN_02" in values
    assert "RN_03" in values
    assert "RN_04" in values
    assert "RN_05" in values
    assert "RN_06" in values


def test_business_rule_code_members():
    assert BusinessRuleCode.RN_01_SHIFT_REQUIRES_DOCTOR == "RN_01"
    assert BusinessRuleCode.RN_02_SPLIT_MUST_CLOSE_PERIOD == "RN_02"
    assert BusinessRuleCode.RN_03_NO_OVERLAPPING == "RN_03"
    assert BusinessRuleCode.RN_04_EXTRA_REQUIRES_JUSTIFICATION == "RN_04"
    assert BusinessRuleCode.RN_05_CLOSED_PERIOD_IMMUTABLE == "RN_05"
    assert BusinessRuleCode.RN_06_DOCTOR_SOFT_DELETE == "RN_06"


def test_business_rule_code_labels():
    labels = BusinessRuleCode.labels()
    assert len(labels) == 6
    assert ("RN_01", "RN_01_SHIFT_REQUIRES_DOCTOR") in labels


def test_business_rule_code_is_str_enum():
    assert issubclass(BusinessRuleCode, str)
