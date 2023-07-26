import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from src.github import (
    list_commits, 
    list_users, 
    list_organizations, 
    list_org_repos,
    list_contributors,
    check_rate_limit,
    paginate_github_resource
)

GITHUB_PERSONAL_ACCESS_TOKEN = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

owner = "awsdocs"
repo = "aws-doc-sdk-examples"

# commits = list_commits(owner, repo, token=GITHUB_PERSONAL_ACCESS_TOKEN, params={"per_page": 100, "page": 1})
# users = list_users(token=GITHUB_PERSONAL_ACCESS_TOKEN, params={"per_page": 100, "page": 1})
# orgs = list_organizations(token=GITHUB_PERSONAL_ACCESS_TOKEN, params={"per_page": 100, "page": 1})
# org_repos = list_org_repos(
#     owner, token=GITHUB_PERSONAL_ACCESS_TOKEN, params={"per_page": 100, "page": 1}
# )
# contributors = list_contributors(
#     owner, repo, token=GITHUB_PERSONAL_ACCESS_TOKEN, params={"per_page": 100, "page": 1}
# )

# rate_limit = check_rate_limit(token=GITHUB_PERSONAL_ACCESS_TOKEN)
# print(len(rate_limit))


for idx, org in enumerate(paginate_github_resource(list_organizations, token=GITHUB_PERSONAL_ACCESS_TOKEN)):
    print(idx, org["login"])

    if idx > 300:
        break

print("Done")