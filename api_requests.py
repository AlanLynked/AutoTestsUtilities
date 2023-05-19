import requests
import json
from config import Config


def register_user(nickname, email):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "nickname": nickname,
        "email": email,
        "first_name": "API",
        "last_name": "User",
        "gender": "male",
        "birthday": "2023-05-17T12:56:23.749Z",
        "education": "string",
        "country": "Russia",
        "city": "Moscow",
        "timezone": 0,
        "languages": "ru",
        "dating_purpose": "love",
    }

    response = requests.post(Config.api_auth_register, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        return True
    else:
        print(f'Error occurred: {response.status_code}')
        return None


def request_otp(email):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
    }

    response = requests.post(Config.api_auth_otp, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return True
    else:
        return False


def get_token(email, otp):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "otp": otp,
    }
    response = requests.post(Config.api_auth_token, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        return None
