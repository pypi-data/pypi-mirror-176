import sys
import requests

from orijin_sdk.defaults import ENDPOINTS
from orijin_sdk.types import API

def login_full(email: str, password: str, custom_endpoint = ENDPOINTS.firebase_login):
    """
    Request a login token to the Orijin system.
    Returns a json of the response, which if successful should include a user token at ["idToken"]
    """
    # try:
    r = requests.post(url=custom_endpoint, json={"email":email, "password":password})
    # except Exception as e:
        # print(e, sys.stderr)
    return r.json()

def login(email: str, password: str, custom_endpoint = ENDPOINTS.firebase_login) -> str | None:
    """
    Request a login token to the Orijin system.
    Same as login_full(), but only the auth token is returned.
    """
    try:
        return login_full(email, password, custom_endpoint)["idToken"]
    except:
        return None

def register_consumer(
    email: str,
    phone: str,
    password: str,
    custom_api: API = ENDPOINTS,
    firstName: str = "Made By",
    lastName: str = "Orijin-SDK (Python)",
    referralCode: str = "",
    purchaseToken: str = "",
    productRegisterID: str = "",
):
    rtn = None
    try:
        fire = None
        r = None

        fire = requests.post(url=ENDPOINTS.firebase_register, json={
            "displayName": f"{firstName} {lastName}",
            "email": email,
            "phone": phone,
            "password": password
        })

        fire = fire.json()

        idToken = fire["idToken"]
        uid = fire["localId"]

        r = requests.post(url=custom_api.consumer_register, json={
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "phone": phone,
            "password": password,
            "referralCode": referralCode,
            "purchaseToken": purchaseToken,
            "productRegisterID": productRegisterID,
            "uid": uid,
            "idToken": idToken
        })

        rtn = r.json()
    except Exception as e:
        print("Registration Error:", sys.stderr)
        print(e, sys.stderr)
        print(fire, sys.stderr)
        print(r, sys.stderr)
    return rtn
