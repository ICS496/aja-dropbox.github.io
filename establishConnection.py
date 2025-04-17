import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
import os
import json
import webbrowser
from PySide6.QtWidgets import QMessageBox, QInputDialog
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Dropbox API credentials from .env
APP_KEY = os.getenv("APP_KEY")
APP_SECRET = os.getenv("APP_SECRET")

# Path to store user's refresh/access token persistently
TOKEN_PATH = os.path.join(os.path.expanduser("~"), ".token_store.json")

# Displays a critical error message using PySide6 message box
def show_error_message(message):
    QMessageBox.critical(None, "Error", message)

# Saves Dropbox access and refresh tokens into a local JSON file
def save_tokens(access_token, refresh_token):
    with open(TOKEN_PATH, "w") as f:
        json.dump({
            "access_token": access_token,
            "refresh_token": refresh_token
        }, f)

# Loads saved tokens (if available) from the JSON token file
def load_tokens():
    try:
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None

# Handles connecting to Dropbox via stored refresh token or OAuth GUI flow
def connect_to_dropbox():
    tokens = load_tokens()
    
    # Try using existing refresh token for silent login
    if tokens and "refresh_token" in tokens:
        try:
            dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=tokens["refresh_token"])
            dbx.users_get_current_account()  # test connection
            return dbx
        except Exception:
            pass  # If refresh token fails, fallback to OAuth

    # First-time login — initiate OAuth2 web flow
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET, token_access_type='offline')
    authorize_url = auth_flow.start()
    webbrowser.open(authorize_url)  # open Dropbox auth page in browser

    # Prompt user for authorization code through a GUI dialog
    code, ok = QInputDialog.getText(None, "Dropbox Authorization",
                                    "1. Authorize the app in your browser.\n2. Paste the authorization code here:")
    if not ok or not code.strip():
        show_error_message("Authorization code was not provided.")
        return None

    # Try finishing the OAuth flow and saving tokens
    try:
        oauth_result = auth_flow.finish(code.strip())
        save_tokens(oauth_result.access_token, oauth_result.refresh_token)
        dbx = dropbox.Dropbox(app_key=APP_KEY, app_secret=APP_SECRET, oauth2_refresh_token=oauth_result.refresh_token)
        dbx.users_get_current_account()
        return dbx
    except Exception as e:
        show_error_message(f"Authorization failed: {e}")
        return None
