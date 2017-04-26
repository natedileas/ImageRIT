from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders

import base64

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'WinServer'

def create_message(sender, to, subject, html_text, image_file):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    msgRoot = MIMEMultipart('alternative')
    msgRoot['Subject'] = 'Subject'
    msgRoot['From'] = sender
    msgRoot['To'] = to
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('related')
    msgText = MIMEText('Here\'s your selfie, and thanks for coming! To learn more, visit www.cis.rit.edu or https://github.com/natedileas/ImageRIT. \n\n - Nate and Ryan')
    msgRoot.attach(msgText)

    html = MIMEText(html_text, 'html')
    msgAlternative.attach(html)
    
    with open(image_file, 'rb') as f:
        img = MIMEImage(f.read(), _subtype='png')
        encoders.encode_base64(img)
        img.add_header('Content-ID', '<IMAGE>')
    
    msgAlternative.attach(img)
    msgRoot.add_header('Content-Disposition', 'attachment', filename=image_file)
    msgRoot.attach(msgAlternative)

    return {'raw': base64.urlsafe_b64encode(msgRoot.as_bytes()).decode()}

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
    #try:
    message = (service.users().messages().send(userId=user_id, body=message)
           .execute())
    print('Message Id: %s' % message['id'])
    return message
    #except Exception as error:
    #    print('An error occurred: %s' % error)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def send_async(email, imagefile):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    with open('sample_email.html', 'r') as f:
        html = f.read()

    #html = html.replace('IMAGE', imagefile)

    message = create_message('ImageRIT2017@gmail.com', email, 'subject', html, imagefile)

    send_message(service, "me", message)

if __name__ == '__main__':
    # in order to use this properly, you have to go to the google api developers console,
    # download the client secret, and put it in this directory.
    # on the first run it will require ui interaction in-browser

    send_async('ndileas@gmail.com', '..\\logo_720x720.png')
