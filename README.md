Common Role
------------

Server bootstrap role, add users / ssh keys, install tools / install chrony/nscd/...

Requirements
------------

Tasks
--------------

| Number |   Task   |                Description                |
|:------:|:--------:|:-----------------------------------------:|
|   00   |  always  | Check OS and install ansible dependencies |
|   01   | hostname |            Set server hostname            |
|   02   |  hosts   |             Manage /etc/hosts             |
|   03   | timezone |            Set server timezone            |
|   04   |  users   |            Manage local users             |
|   05   |   dirs   |           Create local folders            |
|   06   | packages |             Install packages              |


TODO
--------------

|     Task      | Description |
|:-------------:|:-----------:|
| --security--  |     --      |
|   firewall    |             |
|    limits     |             |
|    selinux    |             |
|      ssh      |             |
|     sshd      |             |
|     sudo      |             |
|     sysfs     |             |
|    sysctl     |             |
|  --system--   |     --      |
| environments  |             |
|    locale     |             |
| mail-aliases  |             |
| --software--  |     --      |
|     aide      |             |
|    auditd     |             |
|    chrony     |             |
|     cron      |             |
|   logwatch    |             |
|     nscd      |             |
|   rkhunter    |             |
| smartmontools |             |

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
    group: "deploy"       # default: item.name
    groups: ["docker"]    # default: []
    shell: "/bin/zsh"     # default: /bin/bash
    create_home: true     # default: true
    system: false         # default: false
    append: true          # default: false
    state: present        # default: present

# default: []
common_dirs:
  - path: "/var/shared/backups"
    state: "directory"
    owner: "root"
    group: "root"
    mode: "0750"
    force: "false"
    follow: "true"

# default: []
common_packages: 
  - "strace"
  - "tcpdump"
  - "nano"

# default: []
common_packages_additional:
  - "zsh"
```

Dependencies
------------

Zero

License
-------

MIT
