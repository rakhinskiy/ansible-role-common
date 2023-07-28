Common Role
------------

Server bootstrap role, add users / ssh keys, install tools / install chrony/nscd/...

Requirements
------------

Tasks
--------------

| Number |   Task   |                                      Description                                       |
|:------:|:--------:|:--------------------------------------------------------------------------------------:|
|   00   |  always  | Check distribution and Install ansible dependencies (python3-apt / python3-libselinux) |
|   01   | hostname |                                  Set server hostname                                   |
|   02   |  hosts   |                                   Manage /etc/hosts                                    |

Role Variables
--------------

```yaml
# default: none
common_hostname: "{{ inventory_hostname }}"

# default: []
common_hosts:
  - ip: "192.168.0.1"
    name: "gw-1 gw-1.example.com"
```

Dependencies
------------

Zero

License
-------

MIT
