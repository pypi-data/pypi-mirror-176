# This library grabs the CODEOWNERS file via an HTTPS web request
# since Github has decided NOT to return CODEOWNERS via their API search results
# Inputs: repo, username (or company name)
# Returns: raw CODEOWNERS file

import os
import github_fetch_file

class codeowners:
    def retrieve(repo, username):
        token = os.environ['GITHUB_TOKEN']
        file_path = 'CODEOWNERS'
        ghf = github_fetch_file.fetch()
        res = ghf.read_file(username, repo, file_path, token)
        list = res.split()
        return list
