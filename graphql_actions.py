import requests
import json

def get_group_id(access_token, workspace_url, group_name):
    query = '''
    query GetGroups($workspaceUrl: String!) {
        desTeam(workspaceUrl: $workspaceUrl) {
            groups {
                id
                name
            }
        }
    }
    '''
    variables = {
        "workspaceUrl": workspace_url
    }
    response = send_graphql_request(query, variables, access_token)
    for group in response.json()['data']['desTeam']['groups']:
        if group['name'] == group_name:
            return group['id']
    return None

def get_user_id(access_token, workspace_url, user_email):
    query = '''
    query GetGroups($workspaceUrl: String!) {
        desTeam(workspaceUrl: $workspaceUrl) {
            users {
                userId
                email
            }
        }
    }
    '''
    variables = {
        "workspaceUrl": workspace_url
    }
    response = send_graphql_request(query, variables, access_token)
    for user in response.json()['data']['desTeam']['users']:
        if user['email'] == user_email:
            return user['userId']
    return None

def get_project_id(access_token, workspace_url, project_name):
    query = '''
        query GetProjects($workspaceUrl: String!) {
            desProjects(workspaceUrl: $workspaceUrl) {
                nodes {
                    id
                    name
                }
            }
        }
    '''
    variables = {
        "workspaceUrl": workspace_url
    }
    response = send_graphql_request(query, variables, access_token)
    for project in response.json()['data']['desProjects']['nodes']:
        if project['name'] == project_name:
            return project['id']
    return None

def get_folder_id(access_token, workspace_url, folder_path):
    query = '''
        query GetFolders($workspaceUrl: String!) {
            desLibrary(workspaceUrl: $workspaceUrl) {
                folders {
                    id
                    path
                }
            }
        }
    '''
    variables = {
        "workspaceUrl": workspace_url
    }
    response = send_graphql_request(query, variables, access_token)
    for folder in response.json()['data']['desLibrary']['folders']:
        if folder['path'] == folder_path:
            return folder['id']
    return None

def add_group_permission_to_folder(access_token, folder_id, group_id, read_only=False):
    query = '''
        mutation AddGroupPermission($folder_id: ID!, $group_id: ID!, $can_modify: Boolean!) {
            desUpdateFolderPermissions(
                input: {
                folderId: $folder_id
                permissions: [
                    {
                        canModify: $can_modify,
                        scope: GROUP,
                        groupId: $group_id
                    }
                ]
                }
            ) {
                folderId
            }
        }    
    '''
    variables = {
        "folder_id": folder_id,
        "group_id": group_id,
        "can_modify": read_only
    }
    response = send_graphql_request(query, variables, access_token)
    # Check if the response was successful, and the folder ID matches
    if response.status_code == 200 and response.json()['data']['desUpdateFolderPermissions']['folderId'] == folder_id:
        return True
    else:
        print(response.json()['errors'])
        return False

def add_user_permission_to_folder(access_token, folder_id, user_id, read_only=False):
    query = '''
        mutation AddGroupPermission($folder_id: ID!, $user_id: String!, $can_modify: Boolean!) {
            desUpdateFolderPermissions(
                input: {
                folderId: $folder_id
                permissions: [
                    {
                        canModify: $can_modify,
                        scope: USER,
                        userId: $user_id
                    }
                ]
                }
            ) {
                folderId
            }
        }    
    '''
    variables = {
        "folder_id": folder_id,
        "user_id": user_id,
        "can_modify": read_only
    }
    response = send_graphql_request(query, variables, access_token)
    # Check if the response was successful, and the folder ID matches
    if response.status_code == 200 and response.json()['data']['desUpdateFolderPermissions']['folderId'] == folder_id:
        return True
    else:
        print(response.json()['errors'])
        return False

def add_anyone_permission_to_folder(access_token, folder_id, read_only=False):
    query = '''
        mutation AddAnyonePermission($folder_id: ID!, $can_modify: Boolean!) {
            desUpdateFolderPermissions(
                input: {
                folderId: $folder_id
                permissions: [
                    {
                        canModify: $can_modify,
                        scope: ANYONE
                    }
                ]
                }
            ) {
                folderId
            }
        }    
    '''
    variables = {
        "folder_id": folder_id,
        "can_modify": read_only
    }
    response = send_graphql_request(query, variables, access_token)
    # Check if the response was successful, and the folder ID matches
    if response.status_code == 200 and response.json()['data']['desUpdateFolderPermissions']['folderId'] == folder_id:
        return True
    else:
        print(response.json()['errors'])
        return False
    
def clear_all_permissions_on_folder(access_token, folder_id):
    query = '''
        mutation ClearPermissions($folder_id: ID!) {
            desUpdateFolderPermissions(
                input: {
                folderId: $folder_id
                replaceExisting: true,
                permissions: []
                }
            ) {
                folderId
            }
        }    
    '''
    variables = {
        "folder_id": folder_id
    }
    response = send_graphql_request(query, variables, access_token)
    if response.status_code == 200:
        return True
    else:
        print(response.json()['errors'])
        return False

def add_group_permission_to_project(access_token, project_id, group_id, read_only=False):
    query = '''
        mutation AddGroupPermission($project_id: ID!, $group_id: ID!, $can_modify: Boolean!) {
            desUpdateProjectPermissions(
                input: {
                projectId: $project_id
                permissions: [
                    {
                        canModify: $can_modify,
                        scope: GROUP,
                        groupId: $group_id
                    }
                ]
                }
            ) {
                projectId
            }
        }    
    '''
    variables = {
        "project_id": project_id,
        "group_id": group_id,
        "can_modify": read_only
    }
    response = send_graphql_request(query, variables, access_token)
    # Check if the response was successful, and the project ID matches
    if response.status_code == 200 and response.json()['data']['desUpdateProjectPermissions']['projectId'] == project_id:
        return True
    else:
        print(response.json()['errors'])
        return False

def add_user_permission_to_project(access_token, project_id, user_id, read_only=False):
    query = '''
        mutation AddGroupPermission($project_id: ID!, $user_id: String!, $can_modify: Boolean!) {
            desUpdateProjectPermissions(
                input: {
                projectId: $project_id
                permissions: [
                    {
                        canModify: $can_modify,
                        scope: USER,
                        userId: $user_id
                    }
                ]
                }
            ) {
                projectId
            }
        }    
    '''
    variables = {
        "project_id": project_id,
        "user_id": user_id,
        "can_modify": read_only
    }
    response = send_graphql_request(query, variables, access_token)
    # Check if the response was successful, and the project ID matches
    if response.status_code == 200 and response.json()['data']['desUpdateProjectPermissions']['projectId'] == project_id:
        return True
    else:
        print(response.json()['errors'])
        return False


def add_anyone_permission_to_project(access_token, project_id, read_only=False):
    query = '''
        mutation AddAnyonePermission($project_id: ID!, $can_modify: Boolean!) {
            desUpdateProjectPermissions(
                input: {
                projectId: $project_id
                permissions: [
                    {
                        canModify: $can_modify,
                        scope: ANYONE
                    }
                ]
                }
            ) {
                projectId
            }
        }    
    '''
    variables = {
        "project_id": project_id,
        "can_modify": read_only
    }
    response = send_graphql_request(query, variables, access_token)
    # Check if the response was successful, and the project ID matches
    if response.status_code == 200 and response.json()['data']['desUpdateProjectPermissions']['projectId'] == project_id:
        return True
    else:
        print(response.json()['errors'])
        return False

def clear_all_permissions_on_project(access_token, project_id):
    query = '''
        mutation ClearPermissions($project_id: ID!) {
            desUpdateProjectPermissions(
                input: {
                projectId: $project_id
                replaceExisting: true,
                permissions: []
                }
            ) {
                projectId
            }
        }    
    '''
    variables = {
        "project_id": project_id
    }
    response = send_graphql_request(query, variables, access_token)
    if response.status_code == 200:
        return True
    else:
        print(response.json()['errors'])
        return False

def send_graphql_request(query, variables, access_token, graphql_endpoint = 'https://api.nexar.com/graphql'):
    payload = { "query": query, "variables": variables }
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    response = requests.post(graphql_endpoint, data=json.dumps(payload), headers=headers, verify=True)
    return response    
