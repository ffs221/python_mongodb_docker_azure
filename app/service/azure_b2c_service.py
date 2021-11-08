import requests
from app.helpers.exception import ApiException
from app.config import config
from app.helpers.exception import ApiException

service_principal = {
    "client_id": config.AZURE_B2C_CLIENT_ID,
    "client_secret": config.AZURE_B2C_SECRET,
    "scope": config.AZURE_B2C_SCOPE,
    "grant_type": "client_credentials",
}

def create_and_set_password(display_name, user_email, password) -> bool:
    token = get_token()
    payload = {
        "displayName": display_name,
        "givenName": display_name,
        "surname": display_name,
        "mail": user_email,
        "identities": [
            {
                "signInType": "emailAddress",
                "issuer": "exampleIssue.onmicrosoft.com",
                "issuerAssignedId": user_email,
            }
        ],
        "passwordProfile": {
            "password": password,
            "forceChangePasswordNextSignIn": False,
        },
    }
    user_url = "https://graph.microsoft.com/v1.0/users"
    response = requests.post(user_url, json = payload, headers={"Authorization": token})
    if response.status_code == 201 or response.status_code == 200:
        return True
    else:
        raise ApiException(
            response.status_code,
            data={
                "message": "Actiation failed : Unable to set the password, please try again"
            },
        )


def get_token() -> str:
    token_url = "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(
        config.AZURE_B2C_TENENT
    )
    response = requests.post(token_url, data = service_principal)
    if response.status_code == 200:
        res = response.json()
        return "{} {}".format(res["token_type"], res["access_token"])
    else:
        raise ApiException(
            response.status_code,
            data={
                "message": "Actiation failed : Unable to set the password, please try again"
            },
        )
