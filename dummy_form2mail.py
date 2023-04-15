import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Authenticate the user and build the APIs
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/gmail.compose'])
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/gmail.compose'])
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

sheets_service = build('sheets', 'v4', credentials=creds)
gmail_service = build('gmail', 'v1', credentials=creds)

# Extract email addresses from the Google Form response spreadsheet
spreadsheet_id = '<your-spreadsheet-id>'
range_name = 'Form Responses 1!C2:C'
result = sheets_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
emails = [row[0] for row in result.get('values', []) if row[0]]

# Send an email to each extracted email address
for email in emails:
    message = create_message('<sender-email>', email, '<subject>', '<body>')
    send_message(gmail_service, 'me', message)

def create_message(sender, to, subject, body):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      body: The body of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    message['from'] = sender
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
               can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(F'Sent message to {message["to"]} Message Id: {message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        message = None
    return message
