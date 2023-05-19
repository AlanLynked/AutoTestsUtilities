import os
import re
import time
from datetime import datetime
from api_requests import *
from config import Config
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


now = datetime.now()
date_str = now.strftime("%y%m%d")
time_str = now.strftime("%H%M%S")


NICKNAME = "tuiapi" + date_str + time_str
EMAIL = Config.email + date_str + time_str + "@gmail.com"


# Access mailbox and find confirmation code
def get_confirmation_code():

    # Request OneTimePassword
    if request_otp(EMAIL):
        time.sleep(5)
        scopes = ['https://mail.google.com/']
        creds = None

        if os.path.exists('token_gmail_v1.json'):
            creds = Credentials.from_authorized_user_file('token_gmail_v1.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token_gmail_v1.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)
            # call the Gmail API to fetch INBOX
            results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
            messages = results.get('messages', [])

            # get the last message in the inbox
            last_message = messages[0]

            # get the message ID and fetch the message using the ID
            message = service.users().messages().get(userId='me', id=last_message['id']).execute()
            code = extract_code_from_message(message)

            # # decode the message payload
            # payload = message['payload']
            # headers = payload['headers']
            # for header in headers:
            #     if header['name'] == 'From':
            #         sender = header['value']
            #     if header['name'] == 'Subject':
            #         subject = header['value']
            #     if header['name'] == 'Date':
            #         date = header['value']
            #
            # # decode the message body
            # if 'parts' in payload:
            #     parts = payload['parts']
            #     data = parts[0]['body']['data']
            # else:
            #     data = payload['body']['data']
            #
            # # decode the message body from base64 encoding
            # data = data.replace("-", "+").replace("_", "/")
            # decoded_data = base64.b64decode(data)
            #
            # # return the decoded message body along with other details
            # print({'sender': sender, 'subject': subject, 'date': date, 'body': decoded_data})
            # return {'sender': sender, 'subject': subject, 'date': date, 'body': decoded_data}
            return code
        except HttpError as error:
            print(f'An error occurred: {error}')


# Helper function to extract the confirmation code from the email
def extract_code_from_message(message):
    code_pattern = r"\d{3} \d{3} \d{3}"
    recipient_pattern = r"testuserinkast\+\d*?@gmail\.com"
    try:
        code = ''.join(re.search(code_pattern, message['snippet'])[0].split())
        recipient_email = re.search(recipient_pattern, str(message['payload']['headers']))[0]
        print(f'{code} {recipient_email}')
        return code
    except TypeError as error:
        print(f' {error}')


# Just to check if it's working
def post_note(access_token):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "text": "This is an automated note"
    }

    response = requests.post(Config.api_main_notes, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print("Note placed successfully")
    else:
        return None


# Main function
def get_registered_user_token():
    # Step 1: Send API request to register a new user
    if register_user(NICKNAME, EMAIL):
        # Step 2: Access mailbox and find confirmation code
        confirmation_code = get_confirmation_code()

        if confirmation_code:
            # Step 3: Send confirmation code and receive access token
            token = get_token(EMAIL, confirmation_code)

            if token:
                # Access token received successfully
                print("User registration successful. Access token:", token)
                return token
            else:
                print("Failed to obtain access token.")
                return None
        else:
            print("Confirmation code not found in the mailbox.")
            return None
    else:
        print("Failed to register user.")
        return None


# Run the automation function
access_token = get_registered_user_token()
# if access_token:
#     post_note(access_token)
