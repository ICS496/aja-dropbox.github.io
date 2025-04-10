## Table of contents

* [Overview](#overview)
* [Deployment](#deployment)
* [Installation](#installation)
* [User Guide](#user-guide)
* [Developer Guide](#developer-guide)
* [Development History](#development-history)
* [Links](#links)
* [Project Milestones](#project-milestones)
* [Team](#team)

## Overview
This script automates synchronizing files from a local directory to numerous Dropbox folders. It authenticates with Dropbox using OAuth2 (prompting the user for an authorization code). Then it determines the local source directory and the Dropbox folder using command-line parameters. The script recursively traverses the local files, checks for changes or new files (skipping temporary or hidden files), and uploads or refreshes files on Dropbox as needed. It also provides interactive prompts and performance timing for key operations.

* [Qt for Python/PySide](https://wiki.qt.io/Qt_for_Python) for GUI capabilities

## Deployment
View our website application here: **TO ADD**

## Activity Badges
[![ci-AJA_Dropbox](https://github.com/kalo-stems/kalo-kode/actions/workflows/ci.yml/badge.svg)](https://github.com/kalo-stems/kalo-kode/actions/workflows/ci.yml)

## Installation
Before using AJA Dropbox, a few other things need to be installed beforehand. These instructions are specific to Windows machines... for now (will update with mac too maybe?)

1. Make sure Python is installed on your machine. To do this, open a new Command Prompt window and type `python`, then enter to check your Python version.
   * If already installed, the Python version number should appear. Press `Ctrl-Z` then enter to the right of the >>> to exit from putting any more input into Python.
   * Otherwise, you will have to install Python yourself.
      * **For Windows:** Navigate to **Microsoft Store** from the **Start** menu, and search for Python in the apps. Install the latest version.
      * **For mac:** (TO ADD)
      * After installation, make sure Python is properly installed by repeating step 1. 
2. There are a few packages we need to install, as well. In terminal, run these three commands separately:
   * `pip install dotenv`
   * `pip install dropbox`
   * `pip install PySide6`

Great! AJA Dropbox needs these packages to create its GUI and access the Dropbox API. Now that we've got all the necessary things installed, we can go ahead and download AJA Dropbox itself.

3. **are we just having the user download from a specified branch?** In the AJA Github page, navigate to the [latest branch.](https://github.com/ICS496/aja-dropbox.github.io/tree/main_app_0.4) Under the green code button in the top right, click `Download ZIP` to download all the files.
4. After downloading, unzip the files to wherever you'd like.

And you're done!

## User Guide
This section provides a walkthrough of how to use the AJA Dropbox user interface and its capabilities.

### How to Run the App
AJA Dropbox is able to be run via the command terminal or through an IDE (a code editor, like VSCode).

#### If using a code editor:
In this method, we can simply run the main app file from your IDE.
1. Navigate to the AJA Dropbox folder you've unzipped on your machine.
2. Double click the folder to show its contents. Open the file named `mvp_v1`. If you have an IDE installed, it should automatically open in the IDE.
3. Locate the **Run** button to run the program.
   
#### If using command line:
Here, we'll have to navigate to the app's folder with the terminal and run it from there.
**For Windows:**
1. Take note of the location of your app folder. The path is usually located at the top of the File Explorer window. For example, it may be something like `Downloads\aja-dropbox.github.io-main_app_0.4\aja-dropbox.github.io-main_app_0.4`. Keep this File Explorer window open for reference.
2. Open a new command terminal window. To the left of the cursor, it should read something like `C:\Users\(Your Username Here)`. This is the current directory/path.
3. We need to navigate to the AJA Dropbox folder we installed. To do this, we're going to be using two commands:
  * `cd`: navigates to a specified folder
  * `dir`: lists the contents of a specified folder
In the terminal, type `cd FolderName` then enter to go to that folder. For example, `cd Downloads` navigates to the Downloads folder. You should see that reflected in the current path listed on the left.
4. Keep using `cd` to navigate to the AJA Dropbox folder. If you're unsure as to what content is inside the folder, type `dir` then enter to see a list of all items. If you've messed up and went to the wrong subfolder, use `cd ../` to move back a directory.
5. Finally, now that we've reached the Aja Dropbox Folder, we're going to want to run the program. In the terminal, type `python mvp_v1.py` to run the program.

* From here, regardless of the method used to run the program, an app window will appear. Follow the instructions to link your account to the app and select your local folder to pull files from, and you should be good.

### Usage Notes
* Individual file upload limit is **150 MB**.
* Application can move misplaced files to their correct Dropbox folders (for example, misplacing Smith_Amanda-document.txt in folder Lee_Bruce) and create new folders if necessary--HOWEVER, new folders do not have sharing permissions. User needs to manually give the intended recipent access to the newly created folder on Dropbox.
* Application will also overwrite files of the same name if they're already present in the target Dropbox folder or subfolders within that folder.

## Developer Guide
This section provides information of interest to developers wishing to use this code base as a basis for their own development tasks.

This application uses the [Dropbox for Python API.](https://dropbox-sdk-python.readthedocs.io/en/latest/index.html)

### Application Design
AJA Dropbox is based upon the features our client would like to have. The main goal is to have a program that rarely needs maintenance as they possess no coding knowledge. We are developing an application that would allow the user to maintain the program script itself by creating features that will change the script when neccessary changes are needed. 

### Data Model
This is our prototype Data Model in which we hope to base our collections off of. This is a design choice that we are currently working in progress.

## Development History 
The development process for AJA Dropbox conformed to [Issue Driven Project Management](http://courses.ics.hawaii.edu/ics314f19/modules/project-management/) practices. In a nutshell:

* Development consists of a sequence of Milestones.
* Each Milestone is specified as a set of tasks.
* Each task is described using a GitHub Issue, and is assigned to a single developer to complete.
* Tasks should typically consist of work that can be completed in 2-4 days.
* The work for each task is accomplished with a git branch named "issue-XX", where XX is replaced by the issue number.
* When a task is complete, its corresponding issue is closed and its corresponding git branch is merged into master.
* The state (todo, in progress, complete) of each task for a milestone is managed using a GitHub Project Board.

## Links
* [GitHub Organization](https://github.com/ICS496/aja-dropbox.github.io)

## Current Functionality
* file uploading
    * compares stats of file on local machine and in dropbox cloud, only re-uploads if metadata is changed
    * currently mirrors local directory's hierarchy when uploading
* OAuth account verification
* GUI interface using PyQt

## Project Milestones

### 1/23:
* initial meeting with sponsors

### 1/24-1/30:
* discussed scope of project
* set up Github page
* looked into dropbox file upload automating
* created rough pitch (outline) for sponsors

### 1/31-2/6:
* finalized project scope
* continued editing Github page
* read Dropbox API docs
* request Enterprise Dropbox Access (denied)
* create (trial) business Dropbox account

### 2/7-2/13:
* created Github website, aka this current page!
* continued reading Dropbox API docs (differences between regular and enterprise/business API?)
* started [Dropbox tutorial for Python](https://www.dropbox.com/developers/documentation/python#tutorial), installed dropbox package for Python, generated access token (will need to update to [standard OAuth flow](https://developers.dropbox.com/oauth-guide) in the future, however)
* created Dropbox Testing App, unfortunately not possible to add other devs so only owned/managed by a single person

### 2/14-2/20:
* timeline chart for sponsor (usable demo by 3/7)
* setup dropbox for individual environments
* implemented file uploading to dropbox from desktop
* research account authentication (i.e. how dropbox gets access to an account via oauth)

### 2/21-2/27:
* looked into how others can access Dropbox app
* looked into OAuth implementation (app_key, app_secret)
* work on functionality to upload people's files into their corresponding named folders (as of this week it just mirrors your local directory's hierarchy)

### 2/28-3/6:
* work on Dropbox folder uploading
* combined OAuth and file upload functionality

### 3/7-3/13:
* demo reveal
* fix minor debugs

### 3/28-4/3:
* finalize framework used for GUI
* start documentation for user guide

### 4/4-4/10
* complete manural and FAQ docomentation for user guide
* prepare for demo testing on client's computer
GUI Feedback
* change fixed window to resizeable window
* larger font size (minimal 12 pt font) or add option for sizeable font
* add gui for the link to retrieve access code
* improve GUI UX and UI 

  
## Team
AJA Dropbox Tool is designed and implemented by [Aaron Ancheta](https://aaron-ancheta.github.io/), [Adrienne Kaneshiro](https://amkanesh.github.io/), and [Jaira Pader](https://jairabp.github.io/).
