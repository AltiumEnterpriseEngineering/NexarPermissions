import argparse
import os
import dotenv
from graphql_actions import get_group_id, get_user_id, get_project_id, add_group_permission_to_project, add_user_permission_to_project, add_anyone_permission_to_project
from nexar_token_py.nexar_token import get_token

class Options:
    def __init__(self):
        # Load the environment variables
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
        self.project = parsed_args.project
        self.group = parsed_args.group
        self.user = parsed_args.user
        self.anyone = parsed_args.anyone
        self.read_only = parsed_args.read_only

        # Get the access token
        self.access_token = get_token(self.client_id, self.client_secret, self.scopes)["access_token"]

    def parse_args(self):
        # Add the argument parser
        args = argparse.ArgumentParser(description='Add permissions to a project')
        args.add_argument('-w', '--workspace', help='The URL of the workspace')
        args.add_argument('-p', '--project', help='The name of the PROJECT which permissions should be modified', required=True)
        args.add_argument('-g', '--group', help='The name of the GROUP to add permissions for')
        args.add_argument('-u', '--user', help='The email of the USER to add permissions for')
        args.add_argument('-a', '--anyone', help='Control the permissions for all workspace members', action='store_true')
        args.add_argument('-r', '--read-only', help='Set the permission as read-only', action='store_false')
        return args.parse_args()

def main():
    # Load all the relevant environment and command line options
    options = Options()

    # Validate the access token
    if (options.access_token is None):
        print("Unable to retrieve access token.")
        exit()

    # Validate the workspace
    if options.workspace is None:
        print("Workspace URL is required.")
        exit()
    print(f"Workspace URL: {options.workspace}")

    # Find the project
    project_name = options.project
    project_id = get_project_id(options.access_token, options.workspace, project_name)
    if project_id is None:
        print(f"Project '{project_name}' not found.")
        exit()
    print(f"Project ID for '{project_name}': {project_id}")

    # Actions for group permissions
    group_name = options.group
    group_id = None
    if group_name is not None:
        group_id = get_group_id(options.access_token, options.workspace, group_name)
        if group_id is None:
            print(f"Group '{group_name}' not found.")
        else:
            print(f"Group ID for '{group_name}': {group_id}")

    if group_id is not None:
        if (add_group_permission_to_project(options.access_token, project_id, group_id, options.read_only)):
            print(f"{ "Read" if not options.read_only else "Write" } permission added successfully for group '{group_name}' on project '{project_name}'!")
        else:
            print(f"Failed to add permission for group '{group_name}' on project '{project_name}'.")
    
    # Actions for user permissions
    user_email = options.user
    user_id = None
    if user_email is not None:
        user_id = get_user_id(options.access_token, options.workspace, user_email)
        if user_id is None:
            print(f"User '{user_email}' not found.")
        else:
            print(f"User ID for '{user_email}': {user_id}")
    
    if user_id is not None:
        if (add_user_permission_to_project(options.access_token, project_id, user_id, options.read_only)):
            print(f"{ "Read" if not options.read_only else "Write" } permission added successfully for user '{user_email}' on project '{project_name}'!")
        else:
            print(f"Failed to add permission for user '{user_email}' on project '{project_name}'.")

    # Actions for anyone permissions
    if options.anyone:
        if (add_anyone_permission_to_project(options.access_token, project_id, options.read_only)):
            print(f"{ "Read" if not options.read_only else "Write" } permission added successfully for all workspace members on project '{project_name}'!")
        else:
            print(f"Failed to add permission for all workspace members on project '{project_name}'.")

if __name__ == "__main__":
    main()
