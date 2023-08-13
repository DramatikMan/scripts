#!/usr/bin/python3
"""
first arg = path to pyproject.toml
second arg = path to output of "pdm list" command
"""

import re
import sys

if __name__ == "__main__":
    regex_req = re.compile(r"^│ (?P<name>\S+)\s+│ (?P<version>\S*)")
    req_map: dict[str, str] = {}
    exact = False

    if len(sys.argv) > 3 and sys.argv[3] == "--exact":
        exact = True

    with open(sys.argv[2]) as actual:
        for line in actual.readlines():
            req = re.match(regex_req, line.lower())

            if req is not None:
                req_map[req.group("name")] = req.group("version")

    prefix = "==" if exact else ">="
    regex_dep_with_version = re.compile(r'^\s*"(?P<name>\S+)[\<\>\=]{2}(?P<version>\S+)",')
    regex_dep = re.compile(r'^\s*"(?P<name>\S+)",')

    with open(sys.argv[1]) as pyproject:
        for line in pyproject.readlines():
            lower = line.lower()
            matched = re.match(regex_dep_with_version, lower) or re.match(regex_dep, lower)

            if matched is not None:
                name = matched.group("name")

                if (idx := name.find("[")) != -1:
                    name = name[:idx]

                line = "".join(
                    (
                        '    "',
                        matched.group("name"),
                        prefix,
                        f'{req_map[name]}",\n',
                    )
                )

            print(line, end="")
