"""
first arg = path to pyproject.toml
second arg = path to output of pip freeze
"""

import re
import sys

if __name__ == "__main__":
    regex_dep = re.compile(r'^(\S*).*=\s"(\*)"')
    regex_req = re.compile(r"^(\S*)==(\S*)")
    req_map = {}
    exact = False

    if len(sys.argv) > 3 and sys.argv[3] == "--exact":
        exact = True

    with open(sys.argv[2]) as reqs:
        for line in reqs.readlines():
            req = re.match(regex_req, line.lower())

            if req:
                req_map[req.group(1)] = req.group(2)

    prefix = "" if exact else "^"

    with open(sys.argv[1]) as deps:
        for line in deps.readlines():
            dep = re.match(regex_dep, line.lower())

            if dep:
                line = line.replace("*", prefix + req_map[dep.group(1)])

            print(line, end="")
