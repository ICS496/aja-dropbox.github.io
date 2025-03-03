import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.oauth import NotApprovedException
import os
from dotenv import load_dotenv
import sys

load_dotenv()

# so i can't use env for some reason lol :')
#print("app key: " + str(os.getenv("APP_KEY")))

APP_KEY="ydmdhfykvloacju"
APP_SECRET="2b15duy2govppcs"

#APP_KEY = os.getenv("APP_KEY")
#APP_SECRET = os.getenv("APP_SECRET")

def oauth():
    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, 
                                            consumer_secret=APP_SECRET, 
                                            token_access_type='offline', 
                                            scope=['files.metadata.write', 'files.metadata.read', 
                                                   'files.content.write', 'files.content.read',
                                                   'account_info.read'])

    authorize_url = auth_flow.start()

    print("\nGo to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.\n")

    auth_code = input("Input authorization code: ").strip()

    if not auth_code:
        print("Access denied or no authorization code entered. Exiting...")
        sys.exit(1)

    try:
        oauth_result = auth_flow.finish(auth_code)
    except NotApprovedException:
        print("Access was denied. Exiting...")
        sys.exit(1)

    dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)

    dbx.users_get_current_account()
    print("Authorization successful. Scopes granted:", oauth_result.scope)

    return dbx

