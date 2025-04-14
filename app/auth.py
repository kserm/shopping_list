from functools import wraps
from flask import request, Response
import os

def check_auth(username, password):
    return (username == os.getenv('AUTH_USERNAME') and 
            password == os.getenv('AUTH_PASSWORD'))

def authenticate():
    return Response(
        'Please login with proper credentials', 401,
        {
            'WWW-Authenticate': 'Basic realm="Login Required"',
            'Cache-Control': 'private, max-age=604800'  # 1 week cache
        })

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check cookie first
        if request.cookies.get('auth_token') == 'verified':
            return f(*args, **kwargs)
        
        # Fallback to basic auth
        auth = request.authorization
        if auth and check_auth(auth.username, auth.password):
            resp = f(*args, **kwargs)
            resp.set_cookie('auth_token', 'verified', max_age=604800, secure=True, httponly=True)
            return resp
            
        return Response(
            'Please login', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated
