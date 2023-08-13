#!/usr/bin/python3
"""
first arg = path to package.json
second arg = path to output of "npm list" command
"""

import json
import re
import sys

if __name__ == "__main__":
    regex_req = re.compile(r"(?P<name>[\@\d\w\/\-\_]+)\s{1}(?P<version>[\d\.]+)")
    req_map: dict[str, str] = {}
    exact = False

    if len(sys.argv) > 3 and sys.argv[3] == "--exact":
        exact = True

    with open(sys.argv[2]) as actual:
        for line in actual.readlines():
            req = re.search(regex_req, line)

            if req is not None:
                req_map[req.group("name")] = req.group("version")

    prefix = "" if exact else "^"

    with open(sys.argv[1]) as package_json:
        deps = json.load(package_json)

        for target in ("dependencies", "devDependencies"):
            if (category := deps.get(target)) is None:
                continue

            for key in category:
                category[key] = prefix + req_map[key]

    print(json.dumps(deps, indent=4))
