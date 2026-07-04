from dataclasses import dataclass, field


@dataclass
class BaseQuery:
    filters: dict[str, any] = field(default_factory=dict)
