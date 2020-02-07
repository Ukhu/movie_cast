import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'ukhu-movie-cast-api.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'movie-cast'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    '''
      Gets JWT token from the request header
    '''

    auth_token = request.headers.get('Authorization', None)

    if not auth_token:
        raise AuthError({
            'error': 'header_missing',
            'description': 'No Authorization header supplied'
        }, 401)

    split_auth_token_parts = auth_token.split()

    if len(split_auth_token_parts) < 2:
        raise AuthError({
            'error': 'invalid_auth_header',
            'description': 'Invalid token supplied. Bearer token expected'
        }, 401)

    elif len(split_auth_token_parts) > 2:
        raise AuthError({
            'error': 'invalid_auth_header',
            'description': 'Invalid token supplied. Bearer token expected'
        }, 401)

    elif split_auth_token_parts[0].lower() != 'bearer':
        raise AuthError({
            'error': 'invalid_auth_header',
            'description': 'Invalid token supplied. Token must start with \'bearer\''
        }, 401)

    token = split_auth_token_parts[1]

    return token

def check_permissions(permission, payload):
    '''
      Checks that the user has the appropiate permission to access the endpoint

      Required Parameters:

      - permission: a string containing the necessary permission for this route e.g 'view:movies'
      - payload: the JWT payload returned from the verify_decode_jwt(token) function
    '''

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not found in payload'
        }, 400)
        
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Access denied. Permission not found'
        }, 403)
  
    return True
        
def verify_decode_jwt(token):
    '''
      Verifies the claims of the JWT token to ensure it is from the Auth0 source

      Required Parameters:

      - token: JWT token gotten from the 'Authorization' header
    '''

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 401)

def requires_auth(permission=''):
    '''
      Decorator function to handle authentication for specific routes
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
