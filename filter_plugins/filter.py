from __future__ import annotations

from typing import Any, ClassVar

from ansible.parsing.yaml.objects import (
    AnsibleUnicode,
    AnsibleVaultEncryptedUnicode,
)
from ansible.utils.unsafe_proxy import AnsibleUnsafeText


class FilterModule:
    """
    Custom jinja filters
    """

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
        "Include",
    ]

    def filters(self) -> dict:
        """
        :return: filters dict
        """
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
            "get_all_pairs": self.get_all_pairs,
            "to_list": self.to_list,
            "get_key": self.get_key,
            "get_keys": self.get_keys,
        }

    @staticmethod
    def is_list(var: Any) -> bool:
        """
        :param var: any variable
        :return: true if var is list
        """
        return var and isinstance(var, list)

    def is_ne_list(self, var: Any) -> bool:
        """
        :param var: any variable
        :return: true if var is not empty list
        """
        return self.is_list(var) and len(var) > 0

    @staticmethod
    def is_dict(var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is dict
        """
        return var and isinstance(var, dict)

    def is_ne_dict(self, var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is not empty dict
        """
        return self.is_dict(var) and var != {}

    def is_ne_list_dicts(self, var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is list of dicts
        """
        if not self.is_ne_list(var):
            return False

        for element in var:
            if not self.is_ne_dict(element):
                return False

        return True

    @staticmethod
    def is_str(var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is one of instance of string
        """
        return var and isinstance(
            var,
            (
                str,
                AnsibleUnicode,
                AnsibleVaultEncryptedUnicode,
                AnsibleUnsafeText,
            ),
        )

    def is_ne_str(self, var: Any) -> bool:
        """
        :param var: any variable
        :return: true if variable is one of instance of string and not empty
        """
        return self.is_str(var) and len(var) > 0

    def is_sshd_options(self, var: list):
        """
        :param var: list of sshd options dict {option: "name", value: "value" }
        :return: true if all option names is correct
        """
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

    def get_sshd_option(self, var: Any) -> str:
        """
        :param var: sshd option name in any case
        :return: real name of sshd option
        """
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

    @staticmethod
    def get_all_pairs(var: list[str]) -> list[dict]:
        """
        :param var: list of interfaces / networks / zones
        :return: all pairs of list elements
        """
        if not isinstance(var, list) or len(var) < 2:
            return []

        result = [
            {"from": a, "to": b}
            for idx, a in enumerate(var)
            for b in var[idx + 1 :]
        ]
        return result

    @staticmethod
    def to_list(var: Any) -> list:
        if not isinstance(var, list):
            return [
                var,
            ]
        return var

    def get_key(self, var: dict, key: str, default: Any = None) -> Any:
        if "." in key:
            _current, _next = key.split(".", 1)
            _var = var.get(_current, None)

            if not _var or not isinstance(_var, dict):
                return default

            return self.get_key(var=_var, key=_next)

        return var.get(key, default)

    def get_keys(self, var: list[dict], key: str) -> list[Any]:
        """
        :param var: List of dicts
        :param key: Key for search
        :return: List with key values
        """

        result = []

        for v in var:
            data = self.get_key(v, key)
            if not data:
                continue
            result.extend(self.to_list(data))

        return list(set(result))
