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
|   04   |  users   |                                   Manage local users                                   |


TODO
--------------

|     Task      |    Description     |
|:-------------:|:------------------:|
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

# default: []
common_users:
  - name: "deploy"
    group: "deploy"       # default: name
    groups: ["docker"]    # default: []
    shell: "/bin/zsh"     # default: /bin/bash
    create_home: true     # default: true
    system: false         # default: false
    append: true          # default: false
    state: present        # default: present
```

Dependencies
------------

Zero

License
-------

MIT
