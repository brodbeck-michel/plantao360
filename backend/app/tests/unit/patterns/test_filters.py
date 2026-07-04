from app.common.filters import FilterOperator


def test_filter_operators():
    assert FilterOperator.CONTAINS == "contains"
    assert FilterOperator.EQUALS == "equals"
    assert FilterOperator.STARTS_WITH == "starts_with"
    assert FilterOperator.ENDS_WITH == "ends_with"
    assert FilterOperator.BETWEEN == "between"
    assert FilterOperator.IN == "in"
    assert FilterOperator.NOT_IN == "not_in"
    assert FilterOperator.IS_NULL == "is_null"
