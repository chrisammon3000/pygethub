import time
import requests
from urllib.parse import urlparse, parse_qs

session = requests.Session()

# Headers
session.headers = {
    "Authorization": "",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

def calculate_delay(response):
    """Calculate delay based on X-RateLimit-Remaining and X-RateLimit-Reset headers."""
    remaining = int(response.headers.get('X-RateLimit-Remaining', 0))
    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))  # UTC epoch seconds
    current_time = time.time()  # UTC epoch seconds

    # Calculate the time window until the rate limit resets
    window = max(reset_time - current_time, 1)

    # Calculate the delay to ensure we don't exceed the rate limit
    if remaining > 0:
        delay = window / remaining
    else:
        delay = window

    return delay

def fetch(url: str, token: str, **params) -> dict:
    session.headers["Authorization"] = f"token {token}"
    
    response = session.get(url, params=params)

    try:
        response.raise_for_status()
    except requests.HTTPError as http_err:
        # Add additional error information
        return {"success": False, "message": str(http_err)}
    except Exception as err:
        # Handle unexpected exceptions
        return {"success": False, "message": str(err)}
    
    # Respect rate limit by adding a delay between requests
    delay = calculate_delay(response)
    time.sleep(delay)
    
    # Return data along with link header for pagination
    return {"success": True, "data": response.json(), "link": response.headers.get('Link')}

def get_next_page_url(link_header):
    """Extract next page URL from link header"""
    if link_header is None:
        return None

    links = link_header.split(", ")
    for link in links:
        url, rel = link.split("; ")
        if "rel=\"next\"" in rel:
            return url.strip("<>")
    return None


def list_github_resource(resource_path: str, token: str, **kwargs) -> dict:
    """Return a list of GitHub resources based on the provided resource path"""
    base_url = "https://api.github.com"
    url = base_url + resource_path

    return fetch(url, token, **kwargs)

# Wrapper functions for better readability and resource path consistency
def list_commits(owner: str, repo: str, token: str, **kwargs) -> dict:
    """Return a list of GitHub commits for the specified repository"""
    resource_path = f"/repos/{owner}/{repo}/commits"
    return list_github_resource(resource_path, token, **kwargs)

def list_branches(owner: str, repo: str, token: str, **kwargs) -> dict:
    """Return a list of GitHub branches for the specified repository"""
    resource_path = f"/repos/{owner}/{repo}/branches"
    return list_github_resource(resource_path, token, **kwargs)

def list_users(token: str, since=None, **kwargs) -> dict:
    """Return a list of GitHub users"""
    resource_path = "/users"
    return list_github_resource(resource_path, token, since=since, **kwargs)

def list_organizations(token: str, since=None, **kwargs) -> dict:
    """Return a list of GitHub organizations"""
    resource_path = "/organizations"
    return list_github_resource(resource_path, token, since=since, **kwargs)

def list_org_repos(org_name: str, token: str, **kwargs) -> dict:
    """Return a list of GitHub repos for the specified organization"""
    resource_path = f"/orgs/{org_name}/repos"
    return list_github_resource(resource_path, token, **kwargs)

def list_user_repos(username: str, token: str, **kwargs) -> dict:
    """Return a list of GitHub repos for the specified user"""
    resource_path = f"/users/{username}/repos"
    return list_github_resource(resource_path, token, **kwargs)

def list_contributors(owner: str, repo: str, token: str, **kwargs) -> dict:
    """Return a list of contributors for the specified repository"""
    resource_path = f"/repos/{owner}/{repo}/contributors"
    return list_github_resource(resource_path, token, **kwargs)

def check_rate_limit(token: str, **kwargs) -> dict:
    """Return the rate limit information for the authenticated user"""
    resource_path = "/rate_limit"
    return list_github_resource(resource_path, token, **kwargs)


## Not Used ##
def paginate_github_resource(list_function, start_page=1, per_page=100, **kwargs):
    page = start_page
    while True:
        response = list_function(page=page, per_page=per_page, **kwargs)
        data = response.get("data", [])
        
        if not data:
            break

        for item in data:
            yield item

        print(f"Page {page}: {len(data)} items")

        # Get next page URL from link header
        next_page_url = get_next_page_url(response.get('link', ''))
        if not next_page_url:
            break

        # Update list function to use next page URL
        list_function = lambda **params: fetch(next_page_url, **params)


class GitHubPaginator:
    def __init__(self, token, per_page=100):
        self.token = token
        self.per_page = per_page

    def get_paginator(self, list_function, **kwargs):
        return PaginatedGitHubResource(list_function, self.token, self.per_page, **kwargs)

class PaginatedGitHubResource:
    def __init__(self, list_function, token, per_page, since=None, **kwargs):
        self.list_function = list_function
        self.per_page = per_page
        self.token = token
        self.since = since
        self.kwargs = kwargs
        self.data = []
        self.next_page_url = None
        self.page_counter = 0  # Create a page counter to count the pages.

    def __iter__(self):
        while True:
            if not self.data:
                if self.next_page_url:
                    # If we have a next page URL, we use it directly
                    response = self.list_function(token=self.token, **self.kwargs)
                else:
                    # If we don't have a next page URL, we fetch the first page
                    response = self.list_function(token=self.token, per_page=self.per_page, since=self.since, **self.kwargs)
                
                self.data = response.get("data", [])
                
                if not self.data:
                    break

                self.page_counter += 1  # Increment the page counter
                print(f"Page {self.page_counter}: {len(self.data)} items")

                # Get next page URL from link header
                self.next_page_url = get_next_page_url(response.get('link', ''))
                if self.next_page_url:
                    self.list_function = lambda token, **params: fetch(self.next_page_url, token, **params)
                else:
                    while self.data:
                        yield self.data.pop(0)

                    break # No more pages to fetch

            yield self.data.pop(0)


