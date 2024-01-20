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
|   15   |   firewall    |            Configure iptables             |
|   26   |      zsh      |               Configure ZSH               |

TODO
--------------

- Replace sysfs utils with tuned
- Add to iptables forward / output zone rules
- Add to iptables src nat / dst nat zone rules
- Add iptables restart script with save docker / k8s rules
- Fix ipset service restart in Debian / Ubuntu (ipset is symlink to netfilter-persistent)
- Add firewalld and ufw support
- Add molecule tests (docker with systemd images)

| Number |     Task      | Description |
|:------:|:-------------:|:-----------:|
|        | --security--  |     --      |
|   16   |    selinux    |             |
|        | --software--  |     --      |
|   17   |     aide      |             |
|   18   |    auditd     |             |
|   19   |    chrony     |             |
|   20   |     cron      |             |
|   21   |   logwatch    |             |
|   22   |     nscd      |             |
|   23   |   rkhunter    |             |
|   24   | smartmontools |             |
|   25   |     sshd      |             |


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
#   Only iptables currently supported
common_firewall_backend: "iptables"

# default: []
# default input / forward policy is DROP
# default zone chains policy is RETURN
common_firewall:
  tcp_mss: true
  masquerade:
    interfaces:
      - "eth0"
  filter:
    # eth0:vip VRRP
    - zone: "public"
      ip_addresses:
        - "10.0.10.10"
      default: "drop"  # Chain policy
      services:
        - name: "HTTP"
          ports:
            - "tcp/80"
            - "tcp/443"
          sources:
            - "any"
        - name: "Kubernetes"
          ports:
            - "tcp/6443"
          sources:
            - "any"
          action: "reject" # default action is accept
    # eth0 internal network
    - zone: "dmz"
      interfaces:
        - "eth0"
      default: "return"
      services:
        - name: "Whitelist"
          ports:
            - "any"
          sources:
            - "1.1.1.1"
            - "10.0.0.0/16"
        - name: "SSH"
          ports:
            - "tcp/22"
          sources:
            - "192.168.1.0/24"
            - "10.0.0.0/16"
        - name: "HTTP"
          ports:
            - "tcp/80"
            - "tcp/443"
          sources:
            - "any"
        - name: "IPSec"
          # ports rules:
          # udp/53 -> protocol: udp  / port: 53
          # tcp/80 -> protocol: tcp  / port: 80
          # 80     -> protocol: tcp  / port: 80
          # gre/   -> protocol: gre  / port: not used | enable GRE on chain
          # icmp/  -> protocol: icmp / port: not used | enable pings on chain
          ports:
            - "esp/"
            - "gre/"
            - "udp/500"
            - "udp/4500"
          sources:
            - "any"
  # Direct rules example
  direct:
    mangle: # *mangle table | first rules
      - "-A FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu"
    raw: # *raw table | first rules
      - "-A PREROUTING -s 10.0.0.0/8 -d 10.0.0.0/8 -j NOTRACK"
    filter: # *filter table | first rules
      - "-A INPUT -i eth0 -p esp -j ACCEPT"
      - "-A INPUT -i eth0 -p gre -j ACCEPT"
    nat: # *nat table | first rules
      - "-A POSTROUTING -o eht0 -j MASQUERADE"

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
