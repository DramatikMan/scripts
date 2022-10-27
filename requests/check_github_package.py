"""
GHCR_PAT env var = GitHub PAT with read permission for packages
first arg = repo_name as in https://github.com/{user_name}/{repo_name}
"""

import os
import sys

import requests

if __name__ == "__main__":
    token = os.environ["GHCR_PAT"]
    repo = sys.argv[1]
    url = f"https://api.github.com/user/packages/container/{repo}/versions"

    resp = requests.get(
        url=url,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        },
    )

    print(f"IMAGE_EXISTS={1 if resp.status_code == 200 else 0}")

    if resp.status_code == 200:
        latest_id = resp.json()[0]["id"]
        print(f"LATEST_IMAGE_ID={latest_id}")
