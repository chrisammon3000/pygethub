import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv());

from pygethub import GitHubPaginator, list_org_repos

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
#     print(user['id'])

# # USERS SINCE ID
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_users, since=547)

# for user in pages:
#     print(user['id'])

# # USER REPOS
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_user_repos, username="garystafford", type="all")

# for idx, repo in enumerate(pages):
#     print(idx, repo['name'])


# # ORGS
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_organizations)

# for idx, org in enumerate(pages):
#     print(idx, org['id'], org['login'])

# # ORGS SINCE ID
# paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
# pages = paginator.get_paginator(list_organizations, since=69404)

# for idx, org in enumerate(pages):
#     print(idx, org['id'], org['login'])

# ORG REPOS
paginator = GitHubPaginator(GITHUB_PERSONAL_ACCESS_TOKEN)
pages = paginator.get_paginator(list_org_repos, org_name="nmdp-bioinformatics", type="all")

for idx, repo in enumerate(pages):
    print(idx, repo['name'])

print("Done")