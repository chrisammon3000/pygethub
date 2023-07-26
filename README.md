# pygethub

`pygethub` is a simple Python library for working with the GitHub API. It provides easy-to-use functions for common tasks and supports pagination through the API responses.

## Features

- Get a list of commits for a specific repository.
- Get a list of branches for a specific repository.
- List GitHub users and organizations.
- List repositories for a specific organization or user.
- Get a list of contributors for a specific repository.
- Check the rate limit for the authenticated user.
- Start and resume pagination of global resources.

## Installation

To install `pygethub`, you can use pip:

```
pip install pygethub
```

## Usage

Here is an example of how you can use `pygethub`:

```python
from pygethub import list_commits, GitHubPaginator, list_users

# List commits for a specific repository
commits = list_commits('owner', 'repo', 'your-github-token')
print(commits)

# Use pagination to list users
paginator = GitHubPaginator('your-github-token')

# List users from the beginning
users = paginator.get_paginator(list_users)
for user in users:
    print(user)

# If you want to resume the listing from a certain user ID, use the `since` parameter
users = paginator.get_paginator(list_users, since=500)
for user in users:
    print(user)

# Similarly, you can use the `since` parameter with list_organizations to resume listing from a certain organization ID
```

## Development

To install `pygethub`, along with the tools you need to develop and run tests, run the following in your virtual environment:

```
pip install -e .[dev]
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) on how to contribute to `pygethub`.

## License

`pygethub` is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for the full license text.

---

Note: Replace `#` with the actual link to your documentation and contributing guide.