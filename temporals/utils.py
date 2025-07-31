from typing import Type, Any

def verify_type(attr_name: str, attr_type: Type, value: Any):
    if not isinstance(value, attr_type):
        raise ValueError(f"Provided value for `{attr_name}` is not of type {attr_type}: {value}")
    return value
