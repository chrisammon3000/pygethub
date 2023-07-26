import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv());

from src.github import *

GITHUB_PERSONAL_ACCESS_TOKEN = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

owner = "awsdocs"
repo = "aws-doc-sdk-examples"

# # COMMITS
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# paged_commits = paginator.get_paginator(list_commits, owner=owner, repo=repo)

# for commit in paged_commits:
#     print(commit['sha'])

# # BRANCHES
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# paged_commits = paginator.get_paginator(list_branches, owner=owner, repo=repo)

# for branch in paged_commits:
#     print(branch['name'])

# USERS
paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
pages = paginator.get_paginator(list_users)

for user in pages:
    print(user['login'])

# # ORGS
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_organizations)

# for org in pages:
#     print(org['login'])

print("Done")