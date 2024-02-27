from __future__ import annotations

from typing import ClassVar

from ansible.parsing.yaml.objects import (
    AnsibleUnicode,
    AnsibleVaultEncryptedUnicode,
)
from ansible.utils.unsafe_proxy import AnsibleUnsafeText


class FilterModule:
    STRING_CLASSES: ClassVar[list[str]] = [
        "str",
        "string",
        "AnsibleUnicode",
        "AnsibleUnsafeText",
        "AnsibleVaultEncryptedUnicode",
    ]

    SSHD_OPTIONS: ClassVar[list[str]] = [
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
        "ShowPatchLevel",
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
        "XAuthLocation",
    ]

    def filters(self):
        return {
            "is_list": self.is_list,
            "is_ne_list": self.is_ne_list,
            "is_ne_list_dicts": self.is_ne_list_dicts,
            "is_dict": self.is_dict,
            "is_ne_dict": self.is_ne_dict,
            "is_str": self.is_str,
            "is_ne_str": self.is_ne_str,
            "is_sshd_options": self.is_sshd_options,
            "get_sshd_option": self.get_sshd_option,
        }

    @staticmethod
    def is_list(var):
        return var and isinstance(var, list)

    def is_ne_list(self, var):
        return self.is_list(var) and len(var) > 0

    @staticmethod
    def is_dict(var):
        return var and isinstance(var, dict)

    def is_ne_dict(self, var):
        return self.is_dict(var) and var != {}

    def is_ne_list_dicts(self, var):
        if not self.is_ne_list(var):
            return False

        for element in var:
            if not self.is_ne_dict(element):
                return False

        return True

    @staticmethod
    def is_str(var):
        return var and isinstance(
            var,
            (
                str,
                AnsibleUnicode,
                AnsibleVaultEncryptedUnicode,
                AnsibleUnsafeText,
            ),
        )

    def is_ne_str(self, var):
        return self.is_str(var) and len(var) > 0

    def is_sshd_options(self, var):
        for item in var:
            find = False
            for option in self.SSHD_OPTIONS:
                if (
                    str(item.get("option", ""))
                    .lower()
                    .replace("_", "")
                    .replace("-", "")
                    == str(option).lower()
                ):
                    find = True
            if not find:
                return False

        return True

    def get_sshd_option(self, var):
        var = str(var).lower()
        var = var.replace("_", "")
        var = var.replace("-", "")
        for option in self.SSHD_OPTIONS:
            if var == str(option).lower():
                return str(option)

        raise Exception(
            "Can't find option %s in available sshd options",
            var,
        )
