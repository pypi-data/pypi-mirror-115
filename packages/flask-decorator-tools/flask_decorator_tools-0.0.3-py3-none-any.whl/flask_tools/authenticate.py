import functools
from flask import request

def authenticate(klass):
    def decorator(funct):
        @functools.wraps(funct)
        def wrapper(*args, **kwargs):
            token = request.headers.get('auth-token')
            # ensure that the token is valid
            # extract the user id from the token
            user_id = ""
            return funct(user_id, *args, **kwargs)
        return wrapper
    return decorator