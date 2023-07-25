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

Role Variables
--------------

```yaml
# default: none
common_hostname: "{{ inventory_hostname }}"
```

Dependencies
------------

Zero

License
-------

MIT
