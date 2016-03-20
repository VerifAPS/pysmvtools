

def is_true(val):
    return str(val).lower() in ("true", "yes", 't')


def is_false(val):
    return str(val).lower() in ("false", "no", 'f')


def is_dont_care(val):
    return str(val).lower() in ("*", "o")