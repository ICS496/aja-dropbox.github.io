# import dropbox
# from dropbox import DropboxOAuth2FlowNoRedirect
# from dropbox.oauth import NotApprovedException
# import os
# from dotenv import load_dotenv
# import sys

# load_dotenv()

# APP_KEY = os.getenv("APP_KEY")
# APP_SECRET = os.getenv("APP_SECRET")

# def oauth():
#     auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, 
#                                             consumer_secret=APP_SECRET, 
#                                             token_access_type='offline', 
#                                             scope=['files.metadata.write', 'files.metadata.read', 
#                                                    'files.content.write', 'files.content.read',
#                                                    'account_info.read'])

#     authorize_url = auth_flow.start()

#     print("\nGo to: " + authorize_url)
#     print("2. Click \"Allow\" (you might have to log in first).")
#     print("3. Copy the authorization code.\n")

#     auth_code = input("Input authorization code: ").strip()

#     if not auth_code:
#         print("Access denied or no authorization code entered. Exiting...")
#         sys.exit(1)

#     try:
#         oauth_result = auth_flow.finish(auth_code)
#     except NotApprovedException:
#         print("Access was denied. Exiting...")
#         sys.exit(1)

#     dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)

#     dbx.users_get_current_account()
#     print("Authorization successful. Scopes granted:", oauth_result.scope)

#     return dbx

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
import json
import webbrowser
from PySide6.QtWidgets import QMessageBox, QInputDialog
from dotenv import load_dotenv

load_dotenv()

APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")

TOKEN_PATH = os.path.join(os.path.expanduser("~"), ".token_store.json")

def show_error_message(message):
    QMessageBox.critical(None, "Error", message)

def save_tokens(access_token, refresh_token):
    with open(TOKEN_PATH, "w") as f:
        json.dump({
            "access_token": access_token,
            "refresh_token": refresh_token
        }, f)

def load_tokens():
    try:
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None

def connect_to_dropbox():
    tokens = load_tokens()
    if tokens and "refresh_token" in tokens:
        try:
            dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=tokens["refresh_token"])
            dbx.users_get_current_account()
            return dbx
        except Exception:
            pass

    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')
    authorize_url = auth_flow.start()
    webbrowser.open(authorize_url)

    code, ok = QInputDialog.getText(None, "Dropbox Authorization",
                                    "1. Authorize the app in your browser.\n2. Paste the authorization code here:")
    if not ok or not code.strip():
        show_error_message("Authorization code was not provided.")
        return None

    try:
        oauth_result = auth_flow.finish(code.strip())
        save_tokens(oauth_result.access_token, oauth_result.refresh_token)
        dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=oauth_result.refresh_token)
        dbx.users_get_current_account()
        return dbx
    except Exception as e:
        show_error_message(f"Authorization failed: {e}")
        return None