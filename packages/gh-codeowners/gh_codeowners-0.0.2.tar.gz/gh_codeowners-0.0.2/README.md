#### Python-based Github CODEOWNERS retriever ####
Note:  requires the GITHUB_TOKEN environment var set with a valid token.
Suggested use:

from codeowners_lib import codeowners
co = codeowners
assignees = co.retrieve(<repo name, ie 'some repo name'>)

and you get a list of CODEOWNERS for ticket assignment/etc

