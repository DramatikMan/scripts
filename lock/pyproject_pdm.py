"""
first arg = path to pyproject.toml
second arg = path to output of pdm list
"""

import re
import sys

if __name__ == "__main__":
    regex_req = re.compile(r"^│ (?P<name>\S+)\s+│ (?P<version>\S*)")
    req_map: dict[str, str] = {}

    with open(sys.argv[2]) as reqs:
        for line in reqs.readlines():
            matched = re.match(regex_req, line.lower())

            if matched is not None:
                req_map[matched.group("name")] = matched.group("version")

    regex_dep_with_version = re.compile(r'^\s*"(?P<name>\S+)[\>\=]\=(?P<version>\S+)",')
    regex_dep = re.compile(r'^\s*"(?P<name>\S+)",')

    with open(sys.argv[1]) as pyproject:
        for line in pyproject.readlines():
            matched = re.match(regex_dep_with_version, line.lower())

            if matched is not None:
                name = matched.group("name")

                if (idx := name.find("[")) != -1:
                    name = name[:idx]

                line = f'    "{matched.group("name")}>={req_map[name]}",\n'

            print(line, end="")
