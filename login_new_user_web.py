import os
import re
import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import Config

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

driver = webdriver.Chrome()


now = datetime.now()
date_str = now.strftime("%y%m%d")
time_str = now.strftime("%H%M%S")

NICKNAME = "tui" + date_str + time_str
EMAIL = Config.email + date_str + time_str + "@gmail.com"


def register_new_user():
    # go to the signup page
    driver.get(Config.web_signup)
    driver.implicitly_wait(10)

    # fill the registration fields
    nickname_field = driver.find_element(By.CSS_SELECTOR, '.form__wrapper input[type="text"]:nth-child(1)')
    nickname_field.send_keys(NICKNAME)
    name_field = driver.find_element(By.CSS_SELECTOR, '.form__wrapper input[type="text"]:nth-child(2)')
    name_field.send_keys("Selenium")
    surname_field = driver.find_element(By.CSS_SELECTOR, '.form__wrapper input[type="text"]:nth-child(3)')
    surname_field.send_keys("User")
    signup_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    signup_button.click()

    birthday_field = driver.find_element(By.CSS_SELECTOR, '.form__wrapper .date__input')
    birthday_field.clear()
    birthday_field.send_keys("12 12 1999")
    next_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    next_button.click()

    select_gender = driver.find_element(By.CSS_SELECTOR, '.vs__search')
    select_gender.click()
    select_gender = driver.find_element(By.ID, 'vs1__option-0')
    select_gender.click()
    next_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    next_button.click()

    select_purpose = driver.find_element(By.CSS_SELECTOR, '.vs__search')
    select_purpose.click()
    select_purpose = driver.find_element(By.ID, 'vs2__option-0')
    select_purpose.click()
    next_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    next_button.click()

    select_country = driver.find_element(By.CSS_SELECTOR, '.vs__search')
    select_country.click()
    select_country = driver.find_element(By.ID, 'vs3__option-0')
    select_country.click()
    next_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    next_button.click()

    select_city = driver.find_element(By.CSS_SELECTOR, '.vs__search')
    select_city.click()
    select_city = driver.find_element(By.ID, 'vs4__option-0')
    select_city.click()
    next_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    next_button.click()

    email_field = driver.find_element(By.CSS_SELECTOR, '.form__wrapper input')
    email_field.send_keys(EMAIL)
    next_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    next_button.click()

    otp_code = get_confirmation_code()
    code_field = driver.find_element(By.CSS_SELECTOR, '.form__wrapper input')
    code_field.send_keys(f"{otp_code}")
    next_button = driver.find_element(By.CSS_SELECTOR, '.form__wrapper button[type="submit"]')
    next_button.click()

    # this is so the browser window won't close
    input()

    driver.quit()


# Helper function to het OTP from the email
def get_confirmation_code():

    # wait until the message is delivered
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


def extract_code_from_message(message):
    code_pattern = r"\d{3} \d{3} \d{3}"
    recipient_pattern = r"testuserinkast\+\d*?@gmail\.com"
    try:
        code = ''.join(re.search(code_pattern, message['snippet'])[0].split())
        # recipient_email = re.search(recipient_pattern, str(message['payload']['headers']))[0]
        # print(f'{code} {recipient_email}')
        return code
    except TypeError as error:
        print(f' {error}')


register_new_user()
