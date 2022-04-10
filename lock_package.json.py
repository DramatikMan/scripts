'''
first arg = path to package.json
second arg = path to output of npm list
'''

import json
import re
import sys


if __name__ == '__main__':
    regex_req = re.compile(r'^[+`]-- (\S*)@(\S*)')
    req_map = {}

    with open(sys.argv[2]) as reqs:
        for line in reqs.readlines():
            req = re.match(regex_req, line)

            if req:
                req_map[req.group(1)] = req.group(2)

    with open(sys.argv[1]) as package_json:
        deps = json.load(package_json)

        for target in ('dependencies', 'devDependencies'):
            for key in deps[target]:
                deps[target][key] = req_map[key]

    print(json.dumps(deps, indent=2))
