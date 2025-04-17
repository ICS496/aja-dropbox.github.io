import os
import time
import datetime
import dropbox
import unicodedata
import re
from contextlib import contextmanager

# A context manager for timing how long an operation takes
@contextmanager
def stopwatch(message):
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print(f"Total elapsed time for {message}: {t1 - t0:.3f} seconds")

# Main sync routine — walks through a local folder and uploads files to Dropbox
def run_sync(dbx, dropbox_folder, local_path):
    for dn, dirs, files in os.walk(local_path):
        subfolder = dn[len(local_path):].strip(os.path.sep)
        listing = list_folder(dbx, dropbox_folder, subfolder)
        print(f"Descending into {subfolder or '[root]'}...")

        for name in files:
            fullname = os.path.join(dn, name)
            nname = unicodedata.normalize('NFC', name)  # normalize Unicode encoding

            # Skip unwanted system or temp files
            if name.startswith('.') or name.startswith('@') or name.endswith('~'):
                print(f"Skipping dot or temp file: {name}")
                continue
            if name.endswith('.pyc') or name.endswith('.pyo'):
                print(f"Skipping compiled Python file: {name}")
                continue

            # File already exists in Dropbox folder — check if re-upload is needed
            if nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)

                if isinstance(md, dropbox.files.FileMetadata) and mtime_dt == md.client_modified and size == md.size:
                    print(f"{name} is already synced [stats match]")
                    continue
                else:
                    print(f"{name} has changed, re-uploading...")
                    upload(dbx, fullname, dropbox_folder, subfolder, name, overwrite=True)

            # File not yet uploaded — determine proper folder based on file naming
            else:
                if match_format(fullname):  # file matches expected Last_First-type.ext pattern
                    if check_folder_name(fullname):  # file is in correct local folder
                        upload(dbx, fullname, dropbox_folder, subfolder, name)
                    else:
                        # Wrong local folder — determine correct Dropbox subfolder
                        new_subfolder = determine_dbx_subfolder(fullname)
                        listing = list_folder(dbx, dropbox_folder, new_subfolder)

                        if name in listing:
                            md = listing[name]
                            mtime = os.path.getmtime(fullname)
                            mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                            size = os.path.getsize(fullname)

                            if isinstance(md, dropbox.files.FileMetadata) and mtime_dt == md.client_modified and size == md.size:
                                print(f"{name} is already synced [stats match]")
                            else:
                                print(f"{name} has changed in correct folder, re-uploading...")
                                upload(dbx, fullname, dropbox_folder, new_subfolder, name, overwrite=True)
                        else:
                            print(f"Uploading {name} to {new_subfolder}...")
                            upload(dbx, fullname, dropbox_folder, new_subfolder, name)
                else:
                    print(f"{name} does not match naming format and was skipped.")

        # Remove unwanted system directories
        keep = []
        for dirname in dirs:
            if dirname.startswith('.') or dirname.startswith('@') or dirname.endswith('~') or dirname == '__pycache__':
                print(f"Skipping non-user directory: {dirname}")
                continue
            keep.append(dirname)
        dirs[:] = keep  # update dirs in-place for os.walk()

# Uploads a file to the specified Dropbox subfolder
def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    path = f"/{folder}/{subfolder}/{name}".replace("//", "/").rstrip("/")
    with open(fullname, 'rb') as f:
        data = f.read()

    mtime = os.path.getmtime(fullname)
    with stopwatch(f"upload {name}"):
        try:
            dbx.files_upload(
                data,
                path,
                mode=dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True
            )
        except dropbox.exceptions.ApiError as err:
            print(f"*** API error: {err}")
            return None
    print(f"Uploaded as: {name}")
    return True

# Checks to see if file matches the required naming format (Last_First-type.ext)
# numbers optional, it’s just if there's a duplicate
def match_format(filepath):
    # do some cutting so we just get the filename without the path
    filename = os.path.basename(filepath)
    if filename.count('.') > 1:
        return False
    filename = filename.split('.')[0]
    r = re.compile(".*_.*-.*")  # any string, underscore, then any string, then a dash, then any string
    return bool(r.match(filename))

# Checks if the file's name matches its folder name (i.e., folder name == Last_First from file)
def check_folder_name(fullname):
    temp = fullname.replace("/", "\\").split("\\")
    filename = temp[-1]
    folder = temp[-2]
    fileowner = filename.split("-")[0]
    return fileowner.lower() == folder.lower()

# Gets the correct Dropbox subfolder name from the filename
# upload function already deals with making a new folder so it's just a matter of changing the subfolder name
def determine_dbx_subfolder(fullname):
    print("Folder and file names don't match, determining correct subfolder...")
    temp = fullname.replace("/", "\\").split("\\")
    filename = temp[-1]
    folder = filename.split("-")[0]
    formatted_folder = '_'.join(part.capitalize() for part in folder.split("_"))
    print(f"Moving {filename} to Dropbox subfolder {formatted_folder}...")
    return formatted_folder

# Lists a Dropbox folder and returns a dict of filename -> metadata
def list_folder(dbx, folder, subfolder):
    path = f"/{folder}/{subfolder}".replace("//", "/").rstrip("/")
    try:
        with stopwatch(f"list_folder {path}"):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print(f"Folder listing failed for {path} -- assumed empty: {err}")
        return {}
    return {entry.name: entry for entry in res.entries}
