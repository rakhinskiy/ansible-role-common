Common Role
------------

Server bootstrap role, see tasks in readme

Requirements
------------

 - ansible >= 2.16
 - python >= 3.6

Tasks
--------------

| Number |     Task      |                Description                |
|:------:|:-------------:|:-----------------------------------------:|
|   00   |    always     | Check OS and install ansible dependencies |
|   01   |   hostname    |            Set server hostname            |
|   02   |     hosts     |             Manage /etc/hosts             |
|   03   |   timezone    |            Set server timezone            |
|   04   | repositories  |    Add or enable/disable repositories     |
|   05   |   packages    |             Install packages              |
|   06   |    locale     |             Configure locales             |
|   07   |     users     |            Manage local users             |
|   08   |     sudo      |        Install sudo and configure         |
|   09   |      ssh      |         Configure ssh client keys         |
|   10   |     dirs      |           Create local folders            |
|   11   | environments  |            Configure env vars             |
|   12   |    limits     |           Configure limits.conf           |
|   13   |    sysctl     |           Configure sysctl.conf           |
|   14   |     sysfs     |     Install and configure sysfs utils     |
|   15   |   firewall    |   Configure firewalld / iptables / ufw    |
|   26   |      zsh      |               Configure ZSH               |

TODO
--------------

- Replace sysfsutils with tuned
- Add firewalld and ufw support
- Add molecule tests (docker with systemd images)

|     Task      | Description |
|:-------------:|:-----------:|
| --security--  |     --      |
|    selinux    |             |
| --software--  |     --      |
|     aide      |             |
|    auditd     |             |
|    chrony     |             |
|     cron      |             |
|   logwatch    |             |
|     nscd      |             |
|   rkhunter    |             |
| smartmontools |             |
|     sshd      |             |


Role Variables
--------------

By default, role only run always task, other tasks only if exist config in inventory

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
common_repositories_manager:
  # Debian / Ubuntu example:
  - option: "Acquire::http::proxy"
    value: "http://user:password@hostname:port"
  - option: "Acquire::https::proxy"
    value: "http://user:password@hostname:port"
  - option: "Acquire::::Proxy"
    value: "true"
  - option: "Acquire::ForceIPv4"
    value: "true"
  # CentOS / AlmaLinux / Rocky example (section main is default)
  - option: "gpgcheck"
    value: "1"
    section: "main"
  - option: "installonly_limit"
    value: "3"
    section: "main"
  - option: "clean_requirements_on_remove"
    value: "True"
    section: "main"
  - option: "skip_if_unavailable"
    value: "False"
    section: "main"

# default: []
common_repositories_add:
  # Debian / Ubuntu example:
  - name: "zabbix"
    url: "https://repo.zabbix.com/zabbix/6.4/ubuntu {{ dist_codename }} main"
    key: "https://repo.zabbix.com/RPM-GPG-KEY-ZABBIX-08EFA7DD"
    # deb or deb-src | default deb | ignored on dnf / yum
    type: "deb"
    options:
      arch: "amd64"
  # CentOS / AlmaLinux / Rocky example
  - name: "epel"
    url: "https://download.fedoraproject.org/pub/epel/$releasever/$basearch/"
    key: "https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-{{ dist_version }}"
    options:
      module_hotfixes: "1"
      skip_if_unavailable: "true"
  - name: "example"
    url: "http://example.com/...."
    options:
      gpgcheck: "0"

common_repositories_enable:
  # Debian / Ubuntu example:
  - "zabbix"  # Uncomment all deb / deb-src in /etc/apt/sources.list.d/zabbix.list
  # CentOS / AlmaLinux / Rocky example:
  - "crb"
  - "extras"
  - "highavailability"
  - "plus"

common_repositories_disable:
  # Debian / Ubuntu example:
  - "zabbix"  # Comment all deb / deb-src in /etc/apt/sources.list.d/zabbix.list
  # CentOS / AlmaLinux / Rocky example:
  - "epel"

# default: []
common_packages: 
  - "strace"
  - "tcpdump"
  - "nano"

# default: []
common_packages_additional:
  - "zsh"

# default: none
common_locale: "en_US.UTF-8"

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
common_sudo:
  # user example
  - name: "deploy"
    defaults:
      - "!requiretty"
      - "env_keep += 'TZ'"
    permissions:
      - host: "ALL"
        runas: "root"
        nopasswd: false
        cmd: "ALL"
  # group example
  - name: "%wheel"
    defaults:
      - "!requiretty"
      - "env_keep += 'TZ'"
    permissions:
      - host: "ALL"
        runas: "root"
        nopasswd: true
        cmd: "ALL"

# default: []
common_ssh_authorized_keys:
  - user: deploy
    key: "ssh-rsa AAAAB3..."
    state: "present"

# default: []
common_ssh_keys:
  - user: deploy
    key_name: "id_rsa"
    key_public: "ssh-rsa AAAAB3..."
    key_private: "..."

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
common_environments:
  - user: ~     # Global
    variables:
      YII_DEBUG: "no"
  - user: "deploy"
    variables:
      PATH: "${PATH}:/usr/local/bin:~/.bin/:~/bin/"

# default: []
common_limits:
  - domain: "root"        # Required user / @group
    limit_type: "hard"    # Required hard / soft
    limit_item: "core"    # Required
    value: "100000"       # Required
    use_min: "false"      # default: false | Use min between exist limits.conf and new values
    use_max: "true"       # default: false | Use max between exist limits.conf and new values
    comment: ""

# default: 
# common_sysctl_file: "ansible"
common_sysctl_file: "k8s"

# common_sysctl_keys: []
common_sysctl_keys:
  - name: "net.core.somaxconn"
    value: "50000"

# default: []
common_sysfs:
  - attribute: "power/state"
    value: 0660
    type: "mode"
  - attribute: "power/state"
    value: "root:power"
    type: "owner"
  - attribute: "devices/system/cpu/cpu0/cpufreq/scaling_governor"
    value: "userspace"
    type: "attribute"
  - attribute: "sys/kernel/mm/transparent_hugepage/enabled"
    value: "madvise"
    type: "attribute"

# default: 
#   Alma Linux / Rocky Linux -> firewalld
#   Debian / Ubuntu -> ufw
common_firewall_backend: "iptables"

# default: []
common_firewall:
  filter:
    - zone: "public"
      interfaces:
        - "eth0"
      services:
        - name: "web"
          ports:
            - "tcp/80"
            - "tcp/443"
          sources:
            - "any"
    - zone: "dmz"
      interfaces:
        - "eth1"
      services:
        - name: "whitelist"
          ports:
            - "any"
          sources:
            - "10.0.0.0/24"
        - name: "sshd"
          ports:
            - "tcp/22"
          sources:
            - "192.168.99.0/24"
        - name: "web"
          ports:
            - "tcp/80"
            - "tcp/443"
          sources:
            - "any"

# default: []
common_zsh:
  - user: "deploy"
  - user: "root"

```

Dependencies
------------

Zero

License
-------

MIT
