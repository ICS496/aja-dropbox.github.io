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

#TOKEN = 'asdkjg'

# run_sync is the main function our GUI will call to start syncing
def run_sync(dropbox_folder, local_path):
    folder = dropbox_folder
    rootdir = os.path.expanduser(local_path)  # expands ~ to full path if needed

    # checks for path validity
    if not os.path.exists(rootdir):
        raise Exception(f"{rootdir} does not exist on your filesystem.")
    elif not os.path.isdir(rootdir):
        raise Exception(f"{rootdir} is not a folder on your filesystem.")

    dbx = oauth()  # triggers OAuth flow and returns authorized Dropbox instance

    for dn, dirs, files in os.walk(rootdir):  # recursively walk the local folder
        subfolder = dn[len(rootdir):].strip(os.path.sep)  # determine relative path
        listing = list_folder(dbx, folder, subfolder)  # list existing files in current Dropbox subfolder
        print('Descending into', subfolder, '...')

        for name in files:
            fullname = os.path.join(dn, name)
            nname = unicodedata.normalize('NFC', name)  # normalize for cross-platform compatibility

            # skip unwanted files
            if name.startswith('.') or name.startswith('@') or name.endswith('~'):
                print('Skipping dot or temp file:', name)
                continue
            if name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping compiled Python file:', name)
                continue

            # if file already exists on Dropbox, compare stats
            if nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)

                # check if file has changed
                if isinstance(md, dropbox.files.FileMetadata) and mtime_dt == md.client_modified and size == md.size:
                    print(name, 'is already synced [stats match]')
                    continue
                else:
                    print(name, 'has changed, re-uploading...')
                    upload(dbx, fullname, folder, subfolder, name, overwrite=True)

            # otherwise, we need to figure out where it goes
            else:
                if match_format(fullname):  # makes sure it follows expected naming
                    if check_folder_name(fullname):
                        # correct folder already — upload directly
                        upload(dbx, fullname, folder, subfolder, name)
                    else:
                        # wrong folder — determine where it should go
                        new_subfolder = determine_dbx_subfolder(fullname)
                        listing = list_folder(dbx, folder, new_subfolder)

                        # check again if the file already exists there
                        if name in listing:
                            md = listing[name]
                            mtime = os.path.getmtime(fullname)
                            mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                            size = os.path.getsize(fullname)

                            if isinstance(md, dropbox.files.FileMetadata) and mtime_dt == md.client_modified and size == md.size:
                                print(name, 'is already synced [stats match]')
                            else:
                                print(name, 'has changed in correct folder, re-uploading...')
                                upload(dbx, fullname, folder, new_subfolder, name, overwrite=True)
                        else:
                            # file doesn't exist yet — just upload
                            upload(dbx, fullname, folder, new_subfolder, name)
                else:
                    # invalid file name format — skip
                    print(name, ' does not match naming format and was skipped.')

        # filter out hidden or generated directories
        keep = []
        for dirname in dirs:
            if dirname.startswith('.') or dirname.startswith('@') or dirname.endswith('~') or dirname == '__pycache__':
                print('Skipping non-user directory:', dirname)
                continue
            print('Keeping directory:', dirname)
            keep.append(dirname)
        dirs[:] = keep  # in-place modification for os.walk

    dbx.close()  # clean exit — releases resources



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