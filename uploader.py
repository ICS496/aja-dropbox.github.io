import dropbox
import os
import time
import datetime
import sys
import six
import contextlib
import unicodedata
import argparse
import re

from establishConnection import oauth

TOKEN = 'asdkjg'

# for cmd use only
parser = argparse.ArgumentParser(description='Sync ~/Documents/ICS496_test to Dropbox')
parser.add_argument('folder', nargs='?', default='Test',
                    help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~\Documents\ICS496_testfiles',
                    help='Local directory to upload')
parser.add_argument('--token', default=TOKEN,
                    help='Access token '
                    '(see https://www.dropbox.com/developers/apps)')
parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')

# main program begins here
def main():
    args = parser.parse_args() # for now, just takes cmd line arguments

    # deals with correct cmd input
    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        print('At most one of --yes, --no, --default is allowed')
        sys.exit(2)
    if not args.token:
        print('--token is mandatory')
        sys.exit(2)

    #storing variables from arg
    folder = args.folder
    rootdir = os.path.expanduser(args.rootdir)
    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a folder on your filesystem')
        sys.exit(1)

    #dbx = dropbox.Dropbox(args.token)
    dbx = oauth()

    # testing access calls
    #print(dbx.users_get_current_account())

    for entry in dbx.files_list_folder('').entries:
        print(entry.name)
    

    # walks thru all the files and uploads them
    # First do all the files.
    for dn, dirs, files in os.walk(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder, '...')

        # First do all the files. (root folder)
        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            
            # checks if file already exists on dbx
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already synced [stats match]')
                else:
                    print(name, 'exists with different stats, downloading')
                    res = download(dbx, folder, subfolder, name)
                    with open(fullname) as f:
                        data = f.read()
                    if res == data:
                        print(name, 'is already synced [content match]')
                    else:
                        print(name, 'has changed since last sync')
                        #if yesno('Refresh %s' % name, False, args):
                        # probably check for the correct subfolder here

                        upload(dbx, fullname, folder, subfolder, name,
                                overwrite=True)
            #elif yesno('Upload %s' % name, True, args):

            # check also if file name matches folder name; if not, find correct folder on dbx
            else:
                if match_format(fullname):
                    if check_folder_name(fullname):
                        # proceed as normal if file is under its designated subfolder on desktop
                        upload(dbx, fullname, folder, subfolder, name)
                    else:
                        # otherwise, find correct folder
                        new_subfolder = determine_dbx_subfolder(fullname)
                        listing = list_folder(dbx, folder, new_subfolder)

                        # Recheck for existence in the new subfolder
                        if name in listing:
                            md = listing[name]
                            mtime = os.path.getmtime(fullname)
                            mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                            size = os.path.getsize(fullname)
                            if (isinstance(md, dropbox.files.FileMetadata) and
                                    mtime_dt == md.client_modified and size == md.size):
                                print(name, 'is already synced [stats match]')
                            else:
                                print(name, 'exists in correct subfolder with different stats, re-uploading...')
                                upload(dbx, fullname, folder, new_subfolder, name, overwrite=True)
                        else:
                            upload(dbx, fullname, folder, new_subfolder, name)

                else:
                    print (name, ' is unable to be uploaded because it does not match the specified naming format.')

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            elif name == '__pycache__':
                print('Skipping generated directory:', name)
            else:
                print('Keeping directory:', name)
                keep.append(name)
            #elif yesno('Descend into %s' % name, True, args): # will maybe null this later
            #    print('Keeping directory:', name)
            #    keep.append(name)
            #else:
            #    print('OK, skipping directory:', name)
        dirs[:] = keep


    dbx.close() # exits program

# checks to see if file matches file format
# i'm thinking like this? Last_First123.ext
# numbers optional ofc it's just if there's a duplicate
def match_format(filepath):
    # do some cutting so we just get the filename without the path
    temp = filepath.split("\\")
    filename = temp[len(temp) - 1] # gets the last item
    # checks how many periods there are, if there's more than one throw an error.
    if filename.count(".") > 1:
        return False
    # if it only appears once, splits off the file extension and just deals with the filename
    filename = filename.split(".")[0]

    r = re.compile(".*_.*-.*") # any string, underscore, then any string, then a dash, then any string
    if r.match(filename):
        return True
    else:
        return False

# checks if the file name matches its folder name
def check_folder_name(fullname):
    #print("Checking folder name correctness:")

    # separate into folder and filename
    temp = fullname.split("\\")
    filename = temp[len(temp) - 1] # gets the last item
    folder = temp[len(temp) - 2] # item before the filename is the folder

    # should have already checked to see if filename matches format, so good on that front
    # two names separated by underscores, then a dash, then the filename (like taxform or whatever) 
    # so three elements of the full file name

    # so... basically get everything before the dash (the name) to see if it matches
    temp2 = filename.split("-")
    fileowner = temp2[0]

    # made lower to just make it easier... so any form of the name (as long as it's spelled right) will work
    if fileowner.lower() != folder.lower():
        return False
    return True

# gets the path to the folder the file will go in
# upload function already deals with making a new folder so it's just a matter of changing the subfolder name
# (folder arg in dbx is the root folder, Test)
def determine_dbx_subfolder(fullname):
    print("Folder and file names don't match, determining correct subfolder...")
    temp = fullname.split("\\")
    filename = temp[len(temp) - 1] # first gets the file name...
    folder = filename.split("-")[0] # then gets just the person's name from the filename
    # capitalizes the first letters of the names just in case
    folder = folder.title()
    print("Moving " + filename + " to Dropbox subfolder " + folder + "...")
    return folder

# Lists a folder
def list_folder(dbx, folder, subfolder):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

# Downloads a file
def download(dbx, folder, subfolder, name):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data

# Uploads a file
# notably, limited to files under 150 MB
def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res

def yesno(message, default, args):
    """Handy helper function to ask a yes/no question.

    Command line arguments --yes or --no force the answer;
    --default to force the default answer.

    Otherwise a blank line returns the default, and answering
    y/yes or n/no returns True or False.

    Retry on unrecognized answer.

    Special answers:
    - q or quit exits the program
    - p or pdb invokes the debugger
    """
    if args.default:
        print(message + '? [auto]', 'Y' if default else 'N')
        return default
    if args.yes:
        print(message + '? [auto] YES')
        return True
    if args.no:
        print(message + '? [auto] NO')
        return False
    if default:
        message += '? [Y/n] '
    else:
        message += '? [N/y] '
    while True:
        answer = input(message).strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        if answer in ('q', 'quit'):
            print('Exit')
            raise SystemExit(0)
        if answer in ('p', 'pdb'):
            import pdb
            pdb.set_trace()
        print('Please answer YES or NO.')

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

# runs main
#if __name__ == '__main__':
#    main()