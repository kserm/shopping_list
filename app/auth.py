from functools import wraps
from flask import request, Response
import os

def check_auth(username, password):
    return (username == os.getenv('AUTH_USERNAME') and 
            password == os.getenv('AUTH_PASSWORD'))

def authenticate():
    return Response(
        'Please login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
