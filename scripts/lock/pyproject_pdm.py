#!/usr/bin/python3
"""
first arg = path to pyproject.toml
second arg = path to output of "pdm list" command
"""

import re
import sys
from typing import Generator


rd = re.compile(r'^\s{4}"(?P<name>\S+)",')
rdv = re.compile(r'^\s{4}"(?P<name>\S+)(?P<operator>\>\=|\<\=|\=\=|\<|\>)(?P<version>\S+)",')
rdl = re.compile(r'^\s{4}"(?P<name>\S+)\s{1}@\s{1}(?P<location>\S+)",')
with_options = re.compile(r"^(?P<name>\S+)\[\S+\]")


class DependencyNotFoundError(Exception):
    pass


def process_dependencies(lines: Generator[str, None, None], exact: bool) -> str:
    while not (line := next(lines)).startswith("]"):
        matched = re.match(rdl, line)

        if matched is not None:
            line = f"""    "{matched.group("name").lower()} @ {matched.group("location")}",\n"""
            print(line, end="")
            continue

        line = line.lower()   
        matched = re.match(rdv, line) or re.match(rd, line)

        if matched is not None:
            name = matched.group("name")
            req_name = name

            if (name_with_options := re.match(with_options, name)) is not None:
                req_name = name_with_options.group("name")

            version = req_map.get(req_name) or req_map.get(req_name.replace("-", "_"))

            if version is None:
                raise DependencyNotFoundError(
                    f'dependency {req_name} not found in "pdm list" output'
                )

            line = "".join(
                (
                    '    "',
                    name,
                    "==" if exact else matched.group("operator"),
                    f'{version}",\n',
                )
            )

            print(line, end="")

    return "]\n"


if __name__ == "__main__":
    regex_req = re.compile(r"^│ (?P<name>\S+)\s+│ (?P<version>\S*)\s+")
    req_map: dict[str, str] = {}
    exact = False

    if len(sys.argv) > 3 and sys.argv[3] == "--exact":
        exact = True

    with open(sys.argv[2]) as actual:
        for line in actual.readlines():
            req = re.match(regex_req, line.lower())

            if req is not None:
                req_map[req.group("name")] = req.group("version")

    with open(sys.argv[1]) as pyproject:
        lines = (i for i in pyproject.readlines())

        for line in lines:
            if line.startswith("dependencies"):
                print(line, end="")
                line = process_dependencies(lines, exact)

            if line.startswith("[tool.pdm.") and ("dependencies" in line or "group" in line):
                print(line, end="")
                print(next(lines), end="")
                line = process_dependencies(lines, exact)

            print(line, end="")
