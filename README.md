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
|   19   |    chrony     |       Install and configure chrony        |
|   20   |     cron      |       Install cron[d] and add tasks       |
|   21   |   logwatch    |      Install and configure logwatch       |
|   22   |     nscd      |        Install and configure NSCD         |
|   24   | smartmontools |    Install and configure smartmontools    |
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
- Optimize vars

| Number |     Task      | Description |
|:------:|:-------------:|:-----------:|
|        | --security--  |     --      |
|   16   |    selinux    |             |
|        | --software--  |     --      |
|   17   |     aide      |             |
|   18   |    auditd     |             |
|   23   |   rkhunter    |             |
|   25   |     sshd      |             |


Role Variables
--------------

By default, role only run always task, other tasks only if exist config in inventory

```yaml

# 01 # Hostname

# default: none
common_hostname: "{{ inventory_hostname }}"

# 02 # Hosts

# default: []
common_hosts:
  - ip: "192.168.0.1"
    name: "gw-1 gw-1.example.com"

# 03 # Timezone

# default: none
common_timezone: "Etc/UTC"

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

# 05 # Packages

# default: []
common_packages: 
  - "strace"
  - "tcpdump"
  - "nano"

# default: []
common_packages_additional:
  - "zsh"

# 06 # Locale

# default: none
common_locale: "en_US.UTF-8"

# 07 # Users

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

# 09 # SSh

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

# 10 # Dirs

# default: []
common_dirs:
  - path: "/var/shared/backups"
    state: "directory"
    owner: "root"
    group: "root"
    mode: "0750"
    force: "false"
    follow: "true"

# 11 # Environments

# default: []
common_environments:
  - user: ~     # Global
    variables:
      YII_DEBUG: "no"
  - user: "deploy"
    variables:
      PATH: "${PATH}:/usr/local/bin:~/.bin/:~/bin/"

# 12 # Limits

# default: []
common_limits:
  - domain: "root"        # Required user / @group
    limit_type: "hard"    # Required hard / soft
    limit_item: "core"    # Required
    value: "100000"       # Required
    use_min: "false"      # default: false | Use min between exist limits.conf and new values
    use_max: "true"       # default: false | Use max between exist limits.conf and new values
    comment: ""

# 13 # Sysctl

# default: 
# common_sysctl_file: "ansible"
common_sysctl_file: "k8s"

# common_sysctl_keys: []
common_sysctl_keys:
  - name: "net.core.somaxconn"
    value: "50000"

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

# 15 # Firewall

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

# 19 # Chrony

common_chrony_enable: false

common_chrony_allows:
  - "10/8"
  - "192.168/16"
  - "172.16/12"
common_chrony_command_key: ~
common_chrony_dump_dir: "/var/lib/chrony"
common_chrony_drift_file: "{{ common_chrony_dump_dir }}/chrony.drift"
common_chrony_dump_on_exit: true
common_chrony_generate_command_key: false
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
common_chrony_no_client_log: true
common_chrony_pools:
  - "pool.ntp.org iburst maxsources 5"
common_chrony_rtc_file: ~
common_chrony_rtc_on_utc: true
common_chrony_rtc_sync: true
common_chrony_servers: ~
common_chrony_stratum_weight: "0.001"

# 20 # Cron

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

# 21 # Logwatch

# default: false
common_logwatch_enable: true

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

# 22 # NSCD

# default: false
common_nscd_enable: true

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

# 24 # Smartmontools

# default: false
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

# 26 # ZSH

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
