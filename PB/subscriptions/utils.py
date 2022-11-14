

def user_has_x(user, x):
    return hasattr(user, x) and getattr(user, x) != None
