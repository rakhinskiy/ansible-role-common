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
|   03   | timezone |                                  Set server timezone                                   |

TODO
--------------

|     Task      |    Description     |
|:-------------:|:------------------:|
|     users     | Manage local users |
| environments  |                    |
|   packages    |                    |
|     sudo      |                    |
|     dirs      |                    |
|     cron      |                    |
|    sysctl     |                    |
|    limits     |                    |
|   firewall    |                    |
|   logwatch    |                    |
|     nscd      |                    |
|    chrony     |                    |
|      ssh      |                    |
|     sshd      |                    |
| smartmontools |                    |
|     sysfs     |                    |
|    locale     |                    |
|     aide      |                    |
|   rkhunter    |                    |
| mail-aliases  |                    |
|    selinux    |                    |
|    auditd     |                    |


Role Variables
--------------

```yaml
# default: none
common_hostname: "{{ inventory_hostname }}"

# default: []
common_hosts:
  - ip: "192.168.0.1"
    name: "gw-1 gw-1.example.com"

# default: none
common_timezone: "Etc/UTC"
```

Dependencies
------------

Zero

License
-------

MIT
