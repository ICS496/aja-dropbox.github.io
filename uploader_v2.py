import os
import time
import datetime
import dropbox
import unicodedata
import re
from contextlib import contextmanager

# A context manager for timing how long an operation takes
# Used mainly to measure how long file uploads and folder listings take
def stopwatch(message, logger=None):
    @contextmanager
    def inner():
        t0 = time.time()  # record start time
        try:
            yield  # allow the code inside the context to run
        finally:
            t1 = time.time()  # record end time
            msg = f"Total elapsed time for {message}: {t1 - t0:.3f} seconds"
            if logger:
                logger(msg)
            else:
                print(msg)
    return inner()

# Walks through a local directory and syncs files to Dropbox
# Avoids re-uploading files if nothing changed
def run_sync(dbx, dropbox_folder, local_path, logger=None):
    def log(msg, status="INFO"):
        if logger:
            logger(msg, status)

    # Walk through all subdirectories and files inside local_path
    for dn, dirs, files in os.walk(local_path):
        # Determine relative subfolder inside the main local_path
        subfolder = dn[len(local_path):].strip(os.path.sep)

        # List current files in corresponding Dropbox folder
        listing = list_folder(dbx, dropbox_folder, subfolder)

        for name in files:
            fullname = os.path.join(dn, name)  # Full path to the local file
            nname = unicodedata.normalize('NFC', name)  # Normalize filename (important for Unicode)

            # Skip temporary, hidden, or compiled files
            if name.startswith('.') or name.startswith('@') or name.endswith('~') or name.endswith('.pyc') or name.endswith('.pyo'):
                log(f"{name} skipped (system/temp file)", "SKIPPED")
                continue

            # If the normalized name is found in Dropbox folder listing
            if nname in listing:
                md = listing[nname]  # metadata for existing Dropbox file
                mtime = os.path.getmtime(fullname)  # local file last modified time
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])  # convert to datetime
                size = os.path.getsize(fullname)  # get local file size

                # Check if both client_modified time and size match
                if isinstance(md, dropbox.files.FileMetadata) and mtime_dt == md.client_modified and size == md.size:
                    # If matches, no need to upload
                    log(f"{name} already uploaded", "SKIPPED")
                    continue
                else:
                    # If not matching, re-upload and overwrite
                    upload(dbx, fullname, dropbox_folder, subfolder, name, overwrite=True, logger=logger)

            else:
                # If file not found in Dropbox, check filename format first
                if match_format(fullname):
                    # If file is in correct folder (matches owner name)
                    if check_folder_name(fullname):
                        upload(dbx, fullname, dropbox_folder, subfolder, name, logger=logger)
                    else:
                        # If wrong folder, determine correct Dropbox subfolder
                        new_subfolder = determine_dbx_subfolder(fullname)
                        listing = list_folder(dbx, dropbox_folder, new_subfolder)
                        upload(dbx, fullname, dropbox_folder, new_subfolder, name, logger=logger)
                else:
                    # If filename doesn't match expected pattern, skip
                    log(f"{name} has invalid name format", "SKIPPED")

# Uploads a local file to a Dropbox subfolder
# Overwrites if necessary, depending on the flag
def upload(dbx, fullname, folder, subfolder, name, overwrite=False, logger=None):
    def log(msg, status="INFO"):
        if logger:
            logger(msg, status)

    # Build target Dropbox path
    path = f"/{folder}/{subfolder}/{name}".replace("//", "/").rstrip("/")

    # Open the file and read its binary content
    with open(fullname, 'rb') as f:
        data = f.read()

    # Get file's modified timestamp
    mtime = os.path.getmtime(fullname)
    try:
        # Upload the file with correct metadata
        dbx.files_upload(
            data,
            path,
            mode=dropbox.files.WriteMode.overwrite if overwrite else dropbox.files.WriteMode.add,
            client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
            mute=True
        )
        log(f"{name}", "SUCCESS")  # log successful upload
    except dropbox.exceptions.ApiError as err:
        log(f"{name}: {err}", "FAILED")  # log failed upload with error

# Checks if the file matches the required naming format (Last_First-type.ext)
# numbers optional, it’s just if there's a duplicate
def match_format(filepath):
    filename = os.path.basename(filepath)  # Extract only filename
    if filename.count('.') > 1:
        return False  # More than one dot, likely invalid
    filename = filename.split('.')[0]  # Remove file extension
    r = re.compile(".*_.*-.*")  # regex: some text _ some text - some text
    return bool(r.match(filename))  # return True if matches, else False

# Checks if file's local folder matches file owner name (Last_First)
def check_folder_name(fullname):
    temp = fullname.replace("/", "\\").split("\\")  # Windows-style splitting
    filename = temp[-1]  # last part is the filename
    folder = temp[-2]  # second last part is the folder name
    fileowner = filename.split("-")[0]  # take the "Last_First" part
    return fileowner.lower() == folder.lower()  # compare lowercase versions

# Determines correct Dropbox subfolder from the file name
# Called if user saved file in the wrong folder locally
def determine_dbx_subfolder(fullname, logger=None):
    def log(msg):
        if logger:
            logger(msg)
        else:
            print(msg)

    log("[INFO] Folder and file names don't match, determining correct subfolder...")

    temp = fullname.replace("/", "\\").split("\\")  # Windows path splitting
    filename = temp[-1]
    folder = filename.split("-")[0]  # take the "Last_First" part before "-"
    # Capitalize each part (Last, First)
    formatted_folder = '_'.join(part.capitalize() for part in folder.split("_"))

    log(f"[INFO] Moving {filename} to Dropbox subfolder {formatted_folder}...")
    return formatted_folder

# Lists all files in a Dropbox folder and returns a dict {filename: metadata}
# If the folder does not exist (not found error), returns an empty dictionary
def list_folder(dbx, folder, subfolder, logger=None):
    path = f"/{folder}/{subfolder}".replace("//", "/").rstrip("/")  # clean path

    try:
        # Try listing the Dropbox folder
        with stopwatch(f"list_folder {path}", logger):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        # Folder not found or other API error
        msg = f"[INFO] Folder listing failed for {path} -- assumed empty: {err}"
        if logger:
            logger(msg)
        else:
            print(msg)
        return {}  # return empty dict if failed

    # Build dict of {filename: metadata} for quick lookup
    return {entry.name: entry for entry in res.entries}
