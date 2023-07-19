#!/usr/bin/python3
"""
GHCR_PAT env var = GitHub PAT with read permission for packages
first arg = repo_name as in https://github.com/{user_name}/{repo_name}
"""

import os
import sys

import urllib3

if __name__ == "__main__":
    resp: urllib3.BaseHTTPResponse = urllib3.request(
        "GET",
        f"https://api.github.com/user/packages/container/{sys.argv[1]}/versions",
        headers={
            "Authorization": f"token {os.environ['GHCR_PAT']}",
            "Accept": "application/vnd.github.v3+json",
        },
    )

    print(f"IMAGE_EXISTS={1 if resp.status == 200 else 0}")

    if resp.status == 200:
        latest_id = resp.json()[0]["id"]
        print(f"LATEST_IMAGE_ID={latest_id}")
