Common Role
------------

Server bootstrap role

Requirements
------------

 - ansible >= 2.16
 - python >= 3.6

Tasks
--------------

| Number |     Task      |                Description                | Tests |
|:------:|:-------------:|:-----------------------------------------:|:-----:|
|   00   |    always     | Check OS and install ansible dependencies |  ---  |
|   01   |   hostname    |            Set server hostname            |       |
|   02   |     hosts     |             Manage /etc/hosts             |  ---  |
|   03   |   timezone    |            Set server timezone            |       |
|   04   | repositories  |    Add or enable/disable repositories     |       |
|   05   |   packages    |             Install packages              |       |
|   06   |    locale     |             Configure locales             |       |
|   07   |     users     |            Manage local users             |       |
|   08   |     sudo      |        Install sudo and configure         |       |
|   09   |      ssh      |         Configure ssh client keys         |       |
|   10   |     dirs      |           Create local folders            |       |
|   11   | environments  |            Configure env vars             |       |
|   12   |    limits     |           Configure limits.conf           |       |
|   13   |    sysctl     |           Configure sysctl.conf           |       |
|   14   |     sysfs     |           Configure sysfs utils           |       |
|   15   |     tuned     |        Install and configure tuned        |       |
|   16   |   firewall    |            Configure iptables             |       |
|   17   |    selinux    |       Simple SELinux configuration        |       |
|   18   |     aide      |        Install and configure Aide         |       |
|   19   |     atop      |               Install atop                |       |
|   20   |    auditd     |             Configure auditd              |  ---  |
|   21   |    chrony     |             Configure chrony              |       |
|   22   |     cron      |      Configure cron[d] and add tasks      |       |
|   23   |   logwatch    |            Configure logwatch             |       |
|   24   |     nscd      |              Configure NSCD               |       |
|   25   |   rkhunter    |            Configure rkhunter             |       |
|   26   | smartmontools |          Configure smartmontools          |       |
|   27   |     sshd      |           Configure SSHD daemon           |       |
|   28   |      zsh      |               Configure ZSH               |       |

TODO
--------------

- Audisp plugins config for auditd
- Add support for go-audit (Slack) / go-libaudit (Elastic) versions of audit daemons
- Rewrite rkhunter configure tasks
- Add to iptables output zone rules | ```low priority```
- Add to iptables src nat / dst nat zone rules | ```low priority```
- Add iptables restart script with save docker / k8s rules | ```low priority```
- Add firewalld support | ```low priority```
- Add ufw support | ```low priority```

Role Variables
--------------

By default, role only run always task, other tasks only if exist config in inventory

```yaml
# 01 # Hostname

# default: none
common_hostname: "{{ inventory_hostname }}"
```
```yaml
# 02 # Hosts

# default: []
common_hosts:
  - ip: "192.168.0.1"
    name: "gw-1 gw-1.example.com"
```
```yaml
# 03 # Timezone

# default: none
common_timezone: "Etc/UTC"
```
```yaml
# 04 # Repositories

# default: []
common_repositories_manager:
  # Debian / Ubuntu example:
  - option: "Acquire::http::proxy"
    value: "https://user:password@hostname:port"
  - option: "Acquire::https::proxy"
    value: "https://user:password@hostname:port"
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
    gpg: "https://repo.zabbix.com/RPM-GPG-KEY-ZABBIX-08EFA7DD"
    # deb or deb-src | default deb | ignored on dnf / yum
    type: "deb"
    options:
      arch: "amd64"
  # CentOS / AlmaLinux / Rocky example
  - name: "epel"
    url: "https://download.fedoraproject.org/pub/epel/$releasever/$basearch/"
    gpg: "https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-{{ dist_version }}"
    options:
      module_hotfixes: "1"
      skip_if_unavailable: "true"
  - name: "example"
    url: "https://example.com/...."
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
```
```yaml
# 05 # Packages

# default: []
common_packages:
  - "strace"
  - "tcpdump"
  - "nano"

# default: []
common_packages_additional:
  - "zsh"
```
```yaml
# 06 # Locale

# default: none
common_locale: "en_US.UTF-8"
```
```yaml
# 07 # Users

# default: []
common_users:
  - name: "deploy"
    group: "deploy"       # default: item.name
    groups: ["docker"]    # default: []
    shell: "/bin/zsh"     # default: /bin/bash
    create_home: yes      # default: yes
    system: no            # default: no
    append: yes           # default: no
    state: present        # default: present

# default: []
# Same as common_users and will be merged
#   into common_users before run tasks
common_users_additional: []
```
```yaml
# 08 # Sudo

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
        nopasswd: no
        cmd: "ALL"
  # group example
  - name: "%wheel"
    defaults:
      - "!requiretty"
      - "env_keep += 'TZ'"
    permissions:
      - host: "ALL"
        runas: "root"
        nopasswd: yes
        cmd: "ALL"
```
```yaml
# 09 # SSH

# default: []
common_ssh_authorized_keys:
  - user: deploy
    key: "ssh-rsa ..."
    state: "present"

# default: []
common_ssh_keys:
  - user: deploy
    key_name: "id_rsa"
    key_public: "ssh-rsa ..."
    key_private: "..."
```
```yaml
# 10 # Dirs

# default: []
common_dirs:
  - path: "/var/shared/backups"
    state: "directory"
    owner: "root"
    group: "root"
    mode: "0750"
    force: no
    follow: yes
```
```yaml
# 11 # Environments

# default: []
common_environments:
  - user: ~     # Global
    variables:
      YII_DEBUG: "no"
  - user: "deploy"
    variables:
      PATH: "${PATH}:/usr/local/bin:~/.bin/:~/bin/"
```
```yaml
# 12 # Limits

# default: []
common_limits:
  - domain: "root"        # Required user / @group
    limit_type: "hard"    # Required hard / soft
    limit_item: "core"    # Required
    value: "100000"       # Required
    use_min: no           # default: no | Use min between exist limits.conf and new values
    use_max: yes          # default: no | Use max between exist limits.conf and new values
    comment: ""
```
```yaml
# 13 # Sysctl

# default:
# common_sysctl_file: "ansible"
common_sysctl_file: "k8s"

# common_sysctl_keys: []
common_sysctl_keys:
  - name: "net.core.somaxconn"
    value: "50000"
```
```yaml
# 14 # SysFS

# default: []
common_sysfs:
  - attribute: "power/state"
    value: "0660"
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
```
```yaml
# 15 # Tuned

# default: no
common_tuned_enable: yes

# default: "profile-custom"
common_tuned_profile_name: "profile-kubernetes"

# default: []
common_tuned_profile_config:
  - name: "main"
    params:
      - option: "summary"
        value: "Test"
      - option: "include"
        value: "throughput-performance"
  - name: "sysctl"
    params:
      - option: "vm.dirty_ratio"
        value: "30"
      - option: "vm.swappiness"
        value: "30"
  - name: "vm"
    params:
      - option: "transparent_hugepages"
        value: "never"
```
```yaml
# 16 # Firewall

# default:
#   Alma Linux / Rocky Linux -> firewalld
#   Debian / Ubuntu -> ufw
#   Only iptables currently supported
common_firewall_backend: "iptables"

common_firewall_ipset_zones:
  - zone: "WHITELIST"
    sources:
      - "192.168.23.0/24"
      - "192.168.99.0/24"
  - zone: "VPN_OPEN_CONNECT_NETWORKS"
    sources:
      - "192.168.199.0/24"
  - zone: "VPN_IPSEC_NETWORKS"
    sources:
      - "192.168.200.0/24"
      - "192.168.201.0/24"
  - zone: "DMZ"
    sources:
      - "192.168.202.0/24"
  - zone: "ALL"
    sources:
        - "0.0.0.0/0"

# default: []
# default input / forward policy is DROP
# default zone chains policy is RETURN
common_firewall:
  tcp_mss: yes
  masquerade:
    interfaces:
      - "eth0"
  filter:
    input:
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
              - "BLACKLIST"
            action: "reject" # default action is accept

      # For IP / Network in sources for service
      #   created ipset zone Z-ZONE-S-SERVICE
      #   example Z-DMZ-S-SSH
      # And you can use custom zones from
      #   common_firewall_ipset_zones as sources

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
  forward:
    # Allow forward between all pairs
    #    ppp+ <-> tun+
    #    ppp+ <-> eth0
    #    tun+ <-> eth0
    - interfaces:
      - 'ppp+'
      - 'tun+'
      - 'eth0'
    - networks:
      - '192.168.23.0/24'
      - '192.168.24.0/24'
    - zones:
      - "ALL"
      - "DMZ"
    - zones:
      - "ALL"
      - "VPN_OPEN_CONNECT_NETWORKS"

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

# default: no
common_firewall_allow_restart_docker: yes
# default: no
common_firewall_allow_restart_kube_proxy: yes
```
```yaml
# 17 # SELinux

# default: no | yes only run selinux tasks
common_selinux_enable: yes

# default: targeted | ["targeted", "minimum", "mls"]
common_selinux_policy: "targeted"

# default: enforcing | ["disabled", "enforcing", "permissive"]
common_selinux_state: "enforcing"

# default: no
common_selinux_update_kernel: no

# default: []
# https://docs.ansible.com/ansible/latest/collections/ansible/posix/seboolean_module.html
common_selinux_booleans:
  - name: "httpd_can_network_connect"
    state: yes
    persistent: yes
  - name: "httpd_use_nfs"
    state: yes
    persistent: yes

# default: []
# https://docs.ansible.com/ansible/latest/collections/community/general/sefcontext_module.html
common_selinux_file_contexts:
  - target: "/srv/git_repos(/.*)?"
    setype: httpd_sys_rw_content_t
    state: present
  - target: /srv/containers
    substitute: /var/lib/containers
    state: present

# default: []
# https://docs.ansible.com/ansible/latest/collections/community/general/seport_module.html
common_selinux_ports:
  - port: 6443
    proto: tcp
    setype: http_port_t
    state: present

```
```yaml
# 18 # AIDE

# By default, only install aide and init database
# You can write your own aide.conf and put it to
# inventory and set common_aide_config_file
# then your config uploaded to servers
# don't forget to set common_aide_db_new
# and common_aide_db if not standard path used

# default: no
common_aide_enable: yes

# default: not defined | not required
common_aide_config_file: "{{ inventory_dir }}/.files/{{ ansible_os_family | lower }}/aide.conf"

# default:
#   debian family: /var/lib/aide/aide.db.new
#   redhat family: /var/lib/aide/aide.db.new.gz
common_aide_db_new: "/var/lib/aide/aide.db.new.gz"
# default:
#   debian family: /var/lib/aide/aide.db
#   redhat family: /var/lib/aide/aide.db.gz
common_aide_db: "/var/lib/aide/aide.db.gz"
```
```yaml
# 19 # Atop

# default: no
common_atop_enable: yes

# default: []
common_atop_options:
  # Load snapshot interval (default 600)
  - option: "LOGINTERVAL"
    value: "10"
  # Load history (default 28 days)
  - option: "LOGGENERATIONS"
    value: "14"
```
```yaml
# 20 # Auditd

# Before enable auditd, please open templates/auditd/audit.rules.j2
# Before enable `common_auditd_rules_predefined` READ RULES IN TEMPLATE

common_auditd_enable: yes

# default: []
# Your custom rules
common_auditd_rules:
  - '## Use these rules if you want to log container events'
  - '## watch for container creation'
  - '-a always,exit -F arch=b32 -S clone -F a0&0x7C020000 -F key=container-create'
  - '-a always,exit -F arch=b64 -S clone -F a0&0x7C020000 -F key=container-create'

# default: no
common_auditd_rules_predefined: no

# default: no | After enable immutable, you need to reboot for apply new rules
common_auditd_rules_immutable: no

common_auditd_rules_buffers: "8192"
common_auditd_rules_backlog_wait_time: "60000"
```
```yaml
# 21 # Chrony

common_chrony_enable: no

common_chrony_allows:
  - "10/8"
  - "192.168/16"
  - "172.16/12"
common_chrony_command_key: ~
common_chrony_dump_dir: "/var/lib/chrony"
common_chrony_drift_file: "{{ common_chrony_dump_dir }}/chrony.drift"
common_chrony_dump_on_exit: yes
common_chrony_generate_command_key: no
common_chrony_hw_clock_file: ~
common_chrony_hw_timestamp: ~
common_chrony_keyfile: "/etc/chrony/chrony.keys"
common_chrony_leap_sec_tz: "right/UTC"
common_chrony_local_stratum: "10"
common_chrony_log:
  - "tracking"
  - "measurements"
  - "statistics"
common_chrony_log_change: "1"
common_chrony_log_dir: "/var/log/chrony"
common_chrony_mail_on_change: ~
common_chrony_make_step: "1.0 3"
common_chrony_max_update_skew: "100.0"
common_chrony_min_sources: ~
common_chrony_no_client_log: yes
common_chrony_pools:
  - "pool.ntp.org iburst maxsources 5"
common_chrony_rtc_file: ~
common_chrony_rtc_on_utc: yes
common_chrony_rtc_sync: yes
common_chrony_servers: ~
common_chrony_stratum_weight: "0.001"
```
```yaml
# 22 # Cron

# default: []
common_cron_environments:
  - user: "deploy"
    vars:
      - name: "MAILTO"
        value: "{{ admin_email }}"

# default: []
common_cron_tasks:
  - name: "My super job"          # required
    job: "/opt/scripts/notify.sh" # required
    minute: "0"                   # default: 0
    hour: "1"                     # default: 0
    day: "*"                      # default: *
    month: "*"                    # default: *
    weekday: "*"                  # default: *
    user: "root"                  # default: root
    disabled: "no"                # default: no
```
```yaml
# 23 # Logwatch

# default: no
common_logwatch_enable: yes

common_logwatch_config: "/etc/logwatch/conf/logwatch.conf"
common_logwatch_packages:
  - "logwatch"
common_logwatch_log_dir: "/var/log"
common_logwatch_tmp_dir: "/var/cache/logwatch"
common_logwatch_output: "stdout"
common_logwatch_format: "text"
common_logwatch_encode: "none"
common_logwatch_mail_to: "root"
common_logwatch_mail_from: "logwatch"
common_logwatch_hostname: ~
common_logwatch_filename: ~
common_logwatch_archives: "Yes"
common_logwatch_range: "yesterday"
common_logwatch_detail: "Low"
common_logwatch_services:
  - "All"
  - "-zz-network"
  - "-zz-sys"
  - "-eximstats"
  - "-puppet"
common_logwatch_logfile: ~
common_logwatch_mailer: "/usr/sbin/sendmail -t"
common_logwatch_hostlimit: ~
```
```yaml
# 24 # NSCD

# default: no
common_nscd_enable: yes

common_nscd_logfile: "/var/log/nscd.log"
common_nscd_threads: ~
common_nscd_max_threads: ~
common_nscd_stat_user: ~
common_nscd_debug_level: "0"
common_nscd_reload_count: ~
common_nscd_paranoia: "no"
common_nscd_restart_interval: ~

common_nscd_passwd_enable_cache: "yes"
common_nscd_passwd_positive_time_to_live: "600"
common_nscd_passwd_negative_time_to_live: "20"
common_nscd_passwd_suggested_size: "211"
common_nscd_passwd_check_files: "yes"
common_nscd_passwd_persistent: "yes"
common_nscd_passwd_shared: "yes"
common_nscd_passwd_max_db_size: "33554432"
common_nscd_passwd_auto_propagate: "yes"

common_nscd_group_enable_cache: "yes"
common_nscd_group_positive_time_to_live: "3600"
common_nscd_group_negative_time_to_live: "60"
common_nscd_group_suggested_size: "211"
common_nscd_group_check_files: "yes"
common_nscd_group_persistent: "yes"
common_nscd_group_shared: "yes"
common_nscd_group_max_db_size: "33554432"
common_nscd_group_auto_propagate: "yes"

common_nscd_hosts_enable_cache: "yes"
common_nscd_hosts_positive_time_to_live: "3600"
common_nscd_hosts_negative_time_to_live: "20"
common_nscd_hosts_suggested_size: "211"
common_nscd_hosts_check_files: "yes"
common_nscd_hosts_persistent: "yes"
common_nscd_hosts_shared: "yes"
common_nscd_hosts_max_db_size: "33554432"

common_nscd_services_enable_cache: "yes"
common_nscd_services_positive_time_to_live: "28800"
common_nscd_services_negative_time_to_live: "20"
common_nscd_services_suggested_size: "211"
common_nscd_services_check_files: "yes"
common_nscd_services_persistent: "yes"
common_nscd_services_shared: "yes"
common_nscd_services_max_db_size: "33554432"

common_nscd_netgroup_enable_cache: "no"
common_nscd_netgroup_positive_time_to_live: "28800"
common_nscd_netgroup_negative_time_to_live: "20"
common_nscd_netgroup_suggested_size: "211"
common_nscd_netgroup_check_files: "yes"
common_nscd_netgroup_persistent: "yes"
common_nscd_netgroup_shared: "yes"
common_nscd_netgroup_max_db_size: "33554432"
```
```yaml
# 25 # RKHunter

common_rkhunter_enable: yes
common_rkhunter_options:
  - option: "SCRIPTWHITELIST"
    value: "/usr/sbin/adduser"
    state: "present"  # default: present
  - option: "DISABLE_TESTS"
    value: "(.*)"
    state: "absent"
```
```yaml
# 26 # Smartmontools

# default: no
# Enable on bare-metal servers
common_smartmontools_enable: "{{ ansible_virtualization_role != 'guest' }}"
common_smartmontools_daemon_options:
  - option: "smartd_opts"
    value: "-q never --capabilities"
    state: "present"
common_smartmontools_mail_to: "root"
# default:
#   Alma/Rocky Linux:    "-d removable -n standby,10,q -H -M exec /usr/libexec/smartmontools/smartdnotify"
#   Debian/Ubuntu Linux: "-d removable -n standby,10,q -H -M exec /usr/share/smartmontools/smartd-runner"
common_smartmontools_devicescan: "-H -d removable -n standby,10,q"
common_smartmontools_devices: ~
```
```yaml
# 27 # SSHD

# default: []
# config location: /etc/ssh/sshd_config.d/00-custom.conf
# option name converted at filter_plugins -> filter.py -> def get_sshd_option
common_sshd_options:
  - option: "pub_key_authentication"
    value: "yes"
  - option: "password_authentication"
    value: "no"
  - option: "gss_api_authentication"
    value: "no"
  - option: "kerberos_authentication"
    value: "no"
```
```yaml
# 28 # ZSH

# default: []
common_zsh:
  - user: "deploy"
  - user: "root"

# default: []
# Same as common_zsh and will be merged
#   into common_zsh before run tasks
common_zsh_additional:
  - user: "dba"
```

Dependencies
------------

```shell
ansible-galaxy collection install ansible.posix
ansible-galaxy collection install community.general
```

License
-------

MIT
