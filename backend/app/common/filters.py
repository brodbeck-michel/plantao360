from enum import Enum


class FilterOperator(str, Enum):
    CONTAINS = "contains"
    EQUALS = "equals"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    BETWEEN = "between"
    IN = "in"
    NOT_IN = "not_in"
    IS_NULL = "is_null"
