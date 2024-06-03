# Project and Folder Permissions

This project provides the ability to add permissions to Folders and Projects via the Nexar API.
This is not intended for production use, simply as a minimal example to get you started using the Nexar API.

## Setup
- Clone this repository to your local environment: `git clone https://github.com/AltiumEnterpriseEngineering/NexarPermissions.git`
- Get the submodules: `git submodule update --init --recursive`
- Set up a virtual environment: `python3 -m venv venv`
- Activate the virtual environment: `source venv/bin/activate`
- Install the requirements: `python3 -m pip install -r requirements.txt`
- Create your .env file: `cp .env.example .env`
- Populate your .env file with your workspace URL, and client credentials from: 'https://portal.nexar.com'

## Running the scripts
Make the projects folder read-only to all workspace members: 
```
python3 folder_permissions.py -f "Projects" --anyone --read-only
```
Make the projects folder writable by the Engineers group: 
```
python3 folder_permissions.py -f "Projects" --group "Engineers"
```
Make the projects folder writable by a specific user: 
```
python3 folder_permissions.py -f "Projects" --user "my.user@email.com"
```
Give the Librarians group write access to a specific project: 
```
python3 project_permissions.py -p "Sample - Kame-1" --group "Librarians"
```
Give a user read access to a specific project: 
```
python3 project_permissions.py -p "Sample - Kame-1" --user "my.user@email.com" --read-only
```

## Folder Permissions Script Help
```
usage: folder_permissions.py [-h] [-w WORKSPACE] -f FOLDER [-g GROUP] [-u USER] [-a] [-r]

Add permissions to a folder

options:
  -h, --help            show this help message and exit
  -w WORKSPACE, --workspace WORKSPACE
                        The URL of the workspace
  -f FOLDER, --folder FOLDER
                        The name of the FOLDER which permissions should be modified
  -g GROUP, --group GROUP
                        The name of the GROUP to add permissions for
  -u USER, --user USER  The email of the USER to add permissions for
  -a, --anyone          Control the permissions for all workspace members
  -r, --read-only       Set the permission as read-only
```
## Project Permissions Script Help
```
usage: project_permissions.py [-h] [-w WORKSPACE] -p PROJECT [-g GROUP] [-u USER] [-a] [-r]

Add permissions to a project

options:
  -h, --help            show this help message and exit
  -w WORKSPACE, --workspace WORKSPACE
                        The URL of the workspace
  -p PROJECT, --project PROJECT
                        The name of the PROJECT which permissions should be modified
  -g GROUP, --group GROUP
                        The name of the GROUP to add permissions for
  -u USER, --user USER  The email of the USER to add permissions for
  -a, --anyone          Control the permissions for all workspace members
  -r, --read-only       Set the permission as read-only
```