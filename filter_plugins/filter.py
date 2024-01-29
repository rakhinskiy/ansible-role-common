# TODO: Rewrite filters

class FilterModule(object):

    STRING_CLASSES = [
        'str', 'string', 'AnsibleUnicode', 'AnsibleUnsafeText', 'AnsibleVaultEncryptedUnicode'
    ]

    SSHD_OPTIONS = [
        "AcceptEnv",
        "AddressFamily",
        "AllowAgentForwarding",
        "AllowGroups",
        "AllowTcpForwarding",
        "AllowUsers",
        "AuthorizedKeysFile",
        "Banner",
        "ChallengeResponseAuthentication",
        "ChrootDirectory",
        "Ciphers",
        "ClientAliveCountMax",
        "ClientAliveInterval",
        "Compression",
        "DenyGroups",
        "DenyUsers",
        "ForceCommand",
        "GatewayPorts",
        "GSSAPIAuthentication",
        "GSSAPIKeyExchange",
        "GSSAPICleanupCredentials",
        "GSSAPIStrictAcceptorCheck",
        "GSSAPIStoreCredentialsOnRekey",
        "HostbasedAuthentication",
        "HostbasedUsesNameFromPacketOnly",
        "HostKey",
        "IgnoreRhosts",
        "IgnoreUserKnownHosts",
        "KerberosAuthentication",
        "KerberosGetAFSToken",
        "KerberosOrLocalPasswd",
        "KerberosTicketCleanup",
        "KerberosUseKuserok",
        "KeyRegenerationInterval",
        "ListenAddress",
        "LoginGraceTime",
        "LogLevel",
        "MACs",
        "Match",
        "MaxAuthTries",
        "MaxSessions",
        "MaxStartups",
        "PasswordAuthentication",
        "PermitEmptyPasswords",
        "PermitOpen",
        "PermitRootLogin",
        "PermitTunnel",
        "PermitUserEnvironment",
        "PidFile",
        "Port",
        "PrintLastLog",
        "PrintMotd",
        "Protocol",
        "PubkeyAuthentication",
        "AuthorizedKeysCommand",
        "AuthorizedKeysCommandRunAs",
        "RequiredAuthentications",
        "RequiredAuthentications1",
        "RequiredAuthentications2",
        "RhostsRSAAuthentication",
        "RSAAuthentication",
        "ServerKeyBits",
        "ShowPatchLevel"
        "StrictModes",
        "Subsystem",
        "SyslogFacility",
        "TCPKeepAlive",
        "UseDNS",
        "UseLogin",
        "UsePAM",
        "UsePrivilegeSeparation",
        "X11DisplayOffset",
        "X11Forwarding",
        "X11UseLocalhost",
        "XAuthLocation"
    ]

    def filters(self):
        return {
            'is_list': self.is_list,
            'is_ne_list': self.is_not_empty_list,
            'is_dict': self.is_dict,
            'is_dicts_list': self.is_dicts_list,
            'is_ne_dict': self.is_not_empty_dict,
            'is_string': self.is_string,
            'is_ne_string': self.is_not_empty_string,
            'is_valid_sshd_options': self.is_valid_sshd_options,
            'correct_sshd_option': self.correct_sshd_option,
        }

    @staticmethod
    def is_list(var, *args, **kwargs):
        return var and \
               var.__class__.__name__ == 'list'

    @staticmethod
    def is_not_empty_list(var, *args, **kwargs):
        if var and isinstance(var, list) and len(var) > 0:
            return True
        return False

    @staticmethod
    def is_dict(var, *args, **kwargs):
        return var and \
               var.__class__.__name__ == 'dict'

    @staticmethod
    def is_not_empty_dict(var, *args, **kwargs):
        return var and \
               var.__class__.__name__ == 'dict' and \
               var != {}

    @staticmethod
    def is_dicts_list(var, *args, **kwargs):

        if not var.__class__.__name__ == 'list' or len(var) == 0:
            return False

        for d in var:
            if not d.__class__.__name__ == 'dict' or d == {}:
                return False

        return True

    def is_string(self, var, *args, **kwargs):
        return var and \
               var.__class__.__name__ in self.STRING_CLASSES

    def is_not_empty_string(self, var, *args, **kwargs):
        return var and \
               var.__class__.__name__ in self.STRING_CLASSES and \
               len(var) > 0

    def is_valid_sshd_options(self, var, *args, **kwargs):

        for item in var:
            find = False
            for option in self.SSHD_OPTIONS:
                if str(item.get('option', '')).lower().replace('_','').replace('-', '') == str(option).lower():
                    find = True
            if not find:
                return False

        return True

    def correct_sshd_option(self, var, *args, **kwargs):

        for option in self.SSHD_OPTIONS:
            if str(var).lower().replace('_', '').replace('-', '') == str(option).lower():
                return str(option)

        raise Exception("Can't find option {} in available sshd options".format(var))
