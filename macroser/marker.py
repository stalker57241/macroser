__all__ = ["set_marker", "get_marker"]
__marker = "@"

def set_marker(value: str):
    global __marker
    if value == "":
        raise ValueError("Cannot set empty marker")
    __marker = value

def get_marker() -> str:
    return __marker
