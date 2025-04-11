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

3. **are we just having the user download from a specified branch?** In the AJA Github page, navigate to the [latest branch.](https://github.com/ICS496/aja-dropbox.github.io/tree/main_app_0.5) Under the green code button in the top right, click `Download ZIP` to download all the files.
4. After downloading, unzip the files to wherever you'd like.

Installation done! Move on to the **User Guide** for more information on how to run the app.

## User Guide
This section provides a walkthrough of how to use the AJA Dropbox user interface and its capabilities.

### How to Run the App
AJA Dropbox is able to be run via the command terminal, directly through Python. No IDE is necessary to run this.

1. Navigate to the AJA Dropbox folder you've unzipped on your machine.
2. Double click the folder to show its contents. Locate the file named `mvp_v1.py`, and right click to show more options.
3. Under the 'Open with' menu, there should be the option to run it in your current Python version. Click this.
4. A blank terminal window should open, along with an app interface. In the app, follow the instructions to link your account to the app and select your local folder to pull files from, and you should be good.

#### Naming Conventions
* Files to be uploaded to the Dropbox must follow this specified naming format: `Lastname_Firstname-Documentname.extension`
* example: `Smith_Amanda-document.pdf`

### Usage Notes
* Individual file upload limit is **150 MB**.
* The application can move misplaced files to their correct Dropbox folders (for example, misplacing Smith_Amanda-document.txt in folder Lee_Bruce) and create new folders if necessary--HOWEVER, new folders created through the app do not have sharing permissions. User needs to manually give the intended recipent access to the newly created folder on Dropbox.
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
* [Document for Project Milestones](https://docs.google.com/document/d/1C_hqmui0HNR1qMXpn6Xv6I94yqdIzfGoaImK_YHulBg/edit?usp=sharing)

  
## Team
AJA Dropbox Tool is designed and implemented by [Aaron Ancheta](https://aaron-ancheta.github.io/), [Adrienne Kaneshiro](https://amkanesh.github.io/), and [Jaira Pader](https://jairabp.github.io/).
