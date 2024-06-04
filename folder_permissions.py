import argparse
import os
import dotenv
from graphql_actions import get_folder_id, get_group_id, get_user_id, add_group_permission_to_folder, add_user_permission_to_folder, add_anyone_permission_to_folder
from nexar_token_py.nexar_token import get_token

class Options:
    def __init__(self):
        # Load the environment variables from the .env file
        dotenv.load_dotenv()

        # These options can only come from the environment or the .env file
        self.client_id = os.getenv('NEXAR_CLIENT_ID')
        self.client_secret = os.getenv('NEXAR_CLIENT_SECRET')
        
        # The scopes are set to the required scopes for this script
        self.scopes = ["user.access", "design.domain"]

        parsed_args = self.parse_args()
        
        # Workspace can be passed via an argument, an environment variable, or the .env file
        self.workspace = parsed_args.workspace if (parsed_args.workspace is not None) else os.getenv('WORKSPACE_URL')
        
        # Remaining values are passed through arguments
        self.folder = parsed_args.folder
        self.group = parsed_args.group
        self.user = parsed_args.user
        self.anyone = parsed_args.anyone
        self.read_only = parsed_args.read_only

    def parse_args(self):
        # Add the argument parser
        args = argparse.ArgumentParser(description='Add permissions to a folder')
        args.add_argument('-w', '--workspace', help='The URL of the workspace')
        args.add_argument('-f', '--folder', help='The name of the FOLDER which permissions should be modified', required=True)
        args.add_argument('-g', '--group', help='The name of the GROUP to add permissions for')
        args.add_argument('-u', '--user', help='The email of the USER to add permissions for')
        args.add_argument('-a', '--anyone', help='Control the permissions for all workspace members', action='store_true')
        args.add_argument('-r', '--read-only', help='Set the permission as read-only', action='store_false')
        return args.parse_args()

def group_actions(options, access_token, folder_id, folder_path):
    group_name = options.group
    group_id = None
    if group_name is not None:
        group_id = get_group_id(access_token, options.workspace, group_name)
        if group_id is None:
            print(f"Group '{group_name}' not found.")
        else:
            print(f"Group ID for '{group_name}': {group_id}")

    if group_id is not None:
        if (add_group_permission_to_folder(access_token, folder_id, group_id, options.read_only)):
            print(f"{ "Read" if not options.read_only else "Write" } permission added successfully for group '{group_name}' on folder '{folder_path}'!")
        else:
            print(f"Failed to add permission for group '{group_name}' on folder '{folder_path}'.")

def user_actions(options, access_token, folder_id, folder_path):
    user_email = options.user
    user_id = None
    if user_email is not None:
        user_id = get_user_id(access_token, options.workspace, user_email)
        if user_id is None:
            print(f"User '{user_email}' not found.")
        else:
            print(f"User ID for '{user_email}': {user_id}")
    
    if user_id is not None:
        if (add_user_permission_to_folder(access_token, folder_id, user_id, options.read_only)):
            print(f"{ "Read" if not options.read_only else "Write" } permission added successfully for user '{user_email}' on folder '{folder_path}'!")
        else:
            print(f"Failed to add permission for user '{user_email}' on folder '{folder_path}'.")

def anyone_actions(options, access_token, folder_id, folder_path):
    if (add_anyone_permission_to_folder(access_token, folder_id, options.read_only)):
        print(f"{ "Read" if not options.read_only else "Write" } permission added successfully for all workspace members on folder '{folder_path}'!")
    else:
        print(f"Failed to add permission for all workspace members on folder '{folder_path}'.")

def main():
    # Load all the relevant environment and command line options
    options = Options()

    # Fetch the access token
    print("Fetching the access token. Please sign in using the browser...")
    access_token = None
    try:
        access_token = get_token(options.client_id, options.client_secret, options.scopes)["access_token"]
    except:
        access_token = None

    # Validate the access token
    if (access_token is None):
        print("Unable to retrieve access token.")
        exit()

    # Validate the workspace
    if options.workspace is None:
        print("Workspace URL is required.")
        exit()
    print(f"Workspace URL: {options.workspace}")

    # Find the folder
    folder_path = options.folder
    folder_id = get_folder_id(access_token, options.workspace, folder_path)
    if folder_id is None:
        print(f"Folder '{folder_path}' not found.")
        exit()
    print(f"Folder ID for '{folder_path}': {folder_id}")

    # Perform the action
    if options.group is not None:
        group_actions(options, access_token, folder_id, folder_path)
    elif options.user is not None:
        user_actions(options, access_token, folder_id, folder_path)
    elif options.anyone is not None:
        anyone_actions(options, access_token, folder_id, folder_path)

if __name__ == "__main__":
    main()
