
def vtype(obj, *types):
    for t in types:
        if isinstance(obj, t):
            return True
    return False
