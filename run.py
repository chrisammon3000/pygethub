import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv());

from src.github import *

GITHUB_PERSONAL_ACCESS_TOKEN = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

owner = "nmdp-bioinformatics"
repo = "gfe-db"

# # COMMITS
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_commits, owner=owner, repo=repo)

# for commit in pages:
#     print(commit['sha'])

# # BRANCHES
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_branches, owner=owner, repo=repo)

# for branch in pages:
#     print(branch['name'])

# # USERS
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_users)

# for user in pages:
#     print(user['login'])

# # ORGS
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_organizations)

# for org in pages:
#     print(org['login'])

# ORG REPOS
paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
pages = paginator.get_paginator(list_org_repos, org_name="nmdp-bioinformatics")

for idx, repo in enumerate(pages):
    print(idx, repo['name'])

print("Done")