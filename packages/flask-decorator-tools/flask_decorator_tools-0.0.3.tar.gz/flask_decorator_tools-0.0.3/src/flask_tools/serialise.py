import functools
from flask import make_response, request
import json


def serialize(obj):
    '''Used to convert a class to json'''
    return obj.__dict__

def toJSONResponse(object):
    '''Convert an object to json response'''
    data = object.__dict__
    response = make_response(json.dumps(data, default = serialize))
    response.headers['Content-Type'] = 'application/json'
    ##print(json.dumps(data, default = serialize))
    return response

def deserialise(klass):
    def decorator(funct):
        @functools.wraps(funct)
        def wrapper(*args, **kwargs):
            body = request.json
            deserialise_body = klass(body)
            return funct(deserialise_body, *args, **kwargs)
        return wrapper
    return decorator

def serialise():
    def decorator(funct):
        @functools.wraps(funct)
        def wrapper(*args, **kwargs):
            return toJSONResponse(funct(*args, **kwargs))
        return wrapper
    return decorator