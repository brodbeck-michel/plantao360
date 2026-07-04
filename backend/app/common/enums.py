from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
