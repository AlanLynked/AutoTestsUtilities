import requests
import json


with open('config.json') as config_file:
    config_data = json.load(config_file)

email_base = config_data["email"]
register_url = config_data["register_url"]
otp_url = config_data["otp_url"]
token_url = config_data["token_url"]


def register_user(nickname, email):
    url = register_url
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "nickname": nickname,
        "email": email,
        "first_name": "Auto",
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

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        return True
    else:
        print(f'Error occurred: {response.status_code}')
        return None


def request_otp(email):
    url = otp_url
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return True
    else:
        return False


def get_token(email, otp):
    url = token_url
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "email": email,
        "otp": otp,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        token = response.json().get('access_token')
        return token
    else:
        return None
