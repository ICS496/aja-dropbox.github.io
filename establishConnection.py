import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.oauth import NotApprovedException
import os
from dotenv import load_dotenv
import sys

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, consumer_secret=APP_SECRET, token_access_type='offline', scope=['files.metadata.write', 'files.metadata.read', 'files.content.write', 'files.content.read'])

authorize_url = auth_flow.start()

print("\nGo to: " + authorize_url)

auth_code = input("Authorization code: ").strip()

if not auth_code:
    print("Access denied or no authorization code entered. Exiting...")
    sys.exit(1)

try:
    oauth_result = auth_flow.finish(auth_code)
except NotApprovedException:
    print("Access was denied. Exiting...")
    sys.exit(1)

print("Authorization successful. Scopes granted:", oauth_result.scope)
