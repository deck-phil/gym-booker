

def public_endpoint(function):
    function.is_public = True
    return function


def admin_endpoint(function):
    function.is_admin = True
    return function
