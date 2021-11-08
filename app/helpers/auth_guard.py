import azure_ad_verify_token
from flask_restful import abort
from functools import wraps
from flask import g, request
from azure_ad_verify_token import verify_jwt
from app.config import config


def get_token_auth_header():
    # read the token value from authorization header
    auth = request.headers.get("Authorization", None)

    # check if token is present.
    if not auth:
        raise Exception(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            }
        )
    parts = auth.split()

    # validate the token

    if parts[0].lower() != "bearer":
        raise Exception(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with Bearer",
            }
        )
    elif len(parts) == 1:
        raise Exception(
            {"code": "invalid_header", "description": "Token not found Bearer"}
        )

    elif len(parts) > 2:
        raise Exception(
            {
                "code": "invalid_header",
                "description": "Authorization header must be Bearer token",
            }
        )

    token = parts[1]
    return token


def restricted(access_level=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_jwt(
                    token=token,
                    valid_audiences=[config.B2C_APP_ID],
                    issuer=config.B2C_ISSUER,
                    jwks_uri=config.B2C_JWKS_URI,
                )

                # read user from the mongo db where sub = payload["sub"]
                # set g.user = result, below is the sample
                g.user = {
                    "username": payload["given_name"],
                    "role": payload["jobTitle"],
                }
                if access_level != None:
                    if access_level.lower() in g.user["role"].lower():
                        raise Exception(
                            {
                                "code": "invalid_role",
                                "description": "You do not have {access_level} permission to requested resource",
                            }
                        )

                return func(*args, **kwargs)
            except azure_ad_verify_token.InvalidAuthorizationToken:
                abort(
                    401,
                    messages=[
                        {
                            "code": "invalid_token",
                            "description": "Invalid authorization " " token.",
                        }
                    ],
                )
            except azure_ad_verify_token.AzureVerifyTokenError:
                abort(
                    401,
                    messages=[
                        {
                            "code": "invalid_token",
                            "description": "Invalid authorization " " token.",
                        }
                    ],
                )

            except Exception as e:
                abort(401, messages=e.args)

        return wrapper

    return decorator
