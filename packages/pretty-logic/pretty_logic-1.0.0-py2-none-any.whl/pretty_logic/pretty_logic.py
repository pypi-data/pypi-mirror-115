def _or(*args) -> bool:
    for arg in args:
        if bool(arg):
            return True
    return False


def _and(*args) -> bool:
    for arg in args:
        if not bool(arg):
            return False
    return True
