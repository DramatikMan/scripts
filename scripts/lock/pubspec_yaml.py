#!/usr/bin/python3
"""
first arg = path to pubspec.yaml
second arg = path to output of "dart pub deps" command
"""

import re
import sys
from tempfile import TemporaryFile

import yaml

if __name__ == "__main__":
    regex_req = re.compile(r"── (?P<name>[\@\d\w\/\-\_]+)\s{1}(?P<version>[\d\.]+)")
    req_map: dict[str, str] = {}
    exact = False

    if len(sys.argv) > 3 and sys.argv[3] == "--exact":
        exact = True

    with open(sys.argv[2]) as actual:
        first_line = actual.readline()
        SDK = first_line[:-1].split(" ")[-1]

        for line in actual.readlines():
            req = re.search(regex_req, line)

            if req is not None:
                req_map[req.group("name")] = req.group("version")

    prefix = "" if exact else "^"

    with open(sys.argv[1]) as pubspec_yaml:
        deps = yaml.load(pubspec_yaml, Loader=yaml.Loader)

        for target in ("dependencies", "dev_dependencies"):
            if (category := deps.get(target)) is None:
                continue

            for key in category:
                category[key] = prefix + req_map[key]

        deps["environment"]["sdk"] = f"{prefix}{SDK}"

    with TemporaryFile(mode="w+") as temp:
        yaml.dump(deps, temp, Dumper=yaml.Dumper, indent=2, sort_keys=False)
        temp.seek(0)

        for line in temp.readlines():
            if (
                line.startswith("environment")
                or line.startswith("dependencies")
                or line.startswith("dev_dependencies")
            ):
                print(f"\n{line}", end="")
                continue

            print(line, end="")
