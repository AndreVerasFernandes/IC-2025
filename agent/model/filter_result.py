from dataclasses import dataclass


@dataclass
class FilterResult:
    valid: bool
    error_code: str = None
    whitelisted: bool = False
