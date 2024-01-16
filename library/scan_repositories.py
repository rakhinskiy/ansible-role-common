#!/usr/bin/env python3

from ansible.module_utils.basic import *
from collections import defaultdict

import configparser
import os
import re

DOCUMENTATION = '''
---
module: scan_repositories
short_description: Return list of available repositories
description:
     - Return list of available repositories for Debian / Ubuntu or AlmaLinux / CentOS / RockyLinux
version_added: "1.9"
options: [ ]
requirements: [ ]
author: Vyacheslav Rakhinskiy
'''

EXAMPLES = '''
# Example fact output:
# host | success >> {
#     "ansible_facts": {
#         "repositories": [
#             {
#                 "name": "epel",
#                 "file": "epel.repo",
#                 "state" "1"
#             },
#         ]
#     }
# }
'''


def main():

    module = AnsibleModule(argument_spec=dict())

    data = []

    if os.path.isdir("/etc/apt/sources.list.d"):
        data = apt_repositories()

    if os.path.isdir("/etc/yum.repos.d/"):
        data = yum_repositories()

    data = sorted(data, key=lambda d: d['name'])

    results = dict(ansible_facts=dict(repositories=data), changed=False)

    module.exit_json(**results)


def apt_repositories():

    result = []
    # r'^\s*deb(-src)?\s*(\[(.*)\])?\s*(https?|ftps?):\/\/(\S+)\s*((\S+))?(\s+.*)?'
    for f in os.listdir("/etc/apt/sources.list.d"):
        if f.endswith(".list"):
            with open(file="/etc/apt/sources.list.d/{}".format(f), mode='r', encoding='utf-8') as r:
                state = False
                for line in r.readlines():
                    state = bool(re.match(r'^\s*deb(-src)?(.*)$', line))
                    if state:
                        break
                result.append({'name': f.replace(".list", ""), 'file': f, 'state': state})

    return result


def yum_repositories():

    result = []

    for f in os.listdir("/etc/yum.repos.d/"):
        if not f.endswith('.repo'):
            continue
        repo_config = configparser.ConfigParser()
        repo_config.read("/etc/yum.repos.d/{}".format(f))
        for section in repo_config.sections():
            if repo_config[section]['enabled'] == "0":
                result.append({'name': section, 'file': f, 'state': False})
            else:
                result.append({'name': section, 'file': f, 'state': True})
    return result


if __name__ == '__main__':
    main()
