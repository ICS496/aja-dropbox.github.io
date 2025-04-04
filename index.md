## Table of contents

* [Overview](#overview)
* [Deployment](#deployment)
* [User Guide](#user-guide)
* [Developer Guide](#developer-guide)
* [Development History](#development-history)
* [Links](#links)
* [Project Milestones](#project-milestones)
* [Team](#team)

## Overview
This script automates synchronizing files from a local directory to numerous Dropbox folders. It authenticates with Dropbox using OAuth2 (prompting the user for an authorization code). Then it determines the local source directory and the Dropbox folder using command-line parameters. The script recursively traverses the local files, checks for changes or new files (skipping temporary or hidden files), and uploads or refreshes files on Dropbox as needed. It also provides interactive prompts and performance timing for key operations.

* [Meteor](https://www.meteor.com/) for Javascript-based implementation of client and server code.
* [React](https://react.dev/) for component-based UI implementation and routing.
* [React](https://react-bootstrap.github.io/) Bootstrap CSS Framework for UI design.
* [Uniforms](https://uniforms.tools/) for React and Semantic UI-based form design and display.

## Deployment
View our website application here: **TO ADD**

## Activity Badges
[![ci-AJA_Dropbox](https://github.com/kalo-stems/kalo-kode/actions/workflows/ci.yml/badge.svg)](https://github.com/kalo-stems/kalo-kode/actions/workflows/ci.yml)

## User Guide
This section provides a walkthrough of the AJA Dropbox user interface and its capabilities.

### Landing Page
The landing page is presented to users when they visit the top-level URL to the site. It provides our motto and some previews of our application.

*We intend to enhance the UI design over the course of our project.*

### Usage Notes
* Individual file upload limit is **150 MB**.
* Application can move misplaced files to their correct Dropbox folders (for example, misplacing Smith_Amanda-document.txt in folder Lee_Bruce) and create new folders if necessary--HOWEVER, new folders do not have sharing permissions. User needs to manually give the intended recipent access to the newly created folder on Dropbox.

## Developer Guide
This section provides information of interest to developers wishing to use this code base as a basis for their own development tasks.

This application uses the [Dropbox for Python API.](https://dropbox-sdk-python.readthedocs.io/en/latest/index.html)

### Installation
**(to add)**

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

## Continuous Integration
AJA Dropbox uses [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions) to automatically run ESLint and TestCafe each time a commit is made to the default branch.  You can see the results of all recent "workflows" at [https://github.com/kalo-stems/kalo-stems.github.io/actions](https://github.com/kalo-stems/kalo-stems.github.io/actions).

## Links
* [GitHub Organization](https://github.com/ICS496/aja-dropbox.github.io)

## Current Functionality
* file uploading
    * compares stats of file on local machine and in dropbox cloud, only re-uploads if metadata is changed
    * currently mirrors local directory's hierarchy when uploading
* OAuth account verification

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
finalize framework used for GUI
start documentation for user guide

  
  
## Team
AJA Dropbox Tool is designed and implemented by [Aaron Ancheta](https://aaron-ancheta.github.io/), [Adrienne Kaneshiro](https://amkanesh.github.io/), and [Jaira Pader](https://jairabp.github.io/).
