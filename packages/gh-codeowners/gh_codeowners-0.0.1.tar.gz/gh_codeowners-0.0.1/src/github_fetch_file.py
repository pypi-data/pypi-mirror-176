# Read fetch file from Github
# Inputs:  username, repository_name, file_path, github_token
# Returns: raw file

import base64
import requests
import json

class fetch:
    def read_file(self, username, repository_name, file_path, github_token):
        headers = {}
        if github_token:
            headers['Authorization'] = f"token {github_token}"
            
        url = f'https://api.github.com/repos/{username}/{repository_name}/contents/{file_path}'
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        file_content = data['content']
        file_content_encoding = data.get('encoding')
        if file_content_encoding == 'base64':
            file_content = base64.b64decode(file_content).decode()

        return file_content