#! /usr/bin/env python3
# SPDX-License-Identifier: MIT
import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import *
from uuid import UUID

__version__ = "0.2.0"

logger = logging.getLogger(__name__)


VMID = Union[str, UUID]
"""VM identifier: name or UUID"""

VMInfoDictType = Dict[str, Union[int, str]]


def parse_vminfo(arg: str) -> VMInfoDictType:
    """Parse output from ``vboxmanager showvminfo --machinereadable`` into a `dict`

    Integers are returned as ints
    Strings in double quotes are returned with the quotes removed
    Some keys have unquoted strings as values, those are also returned as strings
    """
    result: VMInfoDictType = {}
    for line in arg.splitlines():
        if not line:
            continue
        if line.find("=") < 0:
            logger.warning("failed to parse line %r", line)
            continue
        k, v = line.split("=", 1)
        if len(k) >= 2 and k[0] == '"' and k[-1] == '"':
            k = k[1:-1]
        # handle quoted strings:
        if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
            result[k] = v[1:-1]
        # handle integers
        elif re.match("^[0-9]+$", v):
            result[k] = int(v)
        else:
            result[k] = v
    return result


class VBoxUartMode(ABC):
    """Represent "uartmode" settings for one vbox uart"""

    @abstractmethod
    def as_cmd_args(self) -> List[str]:
        """Format as argument list for VBoxManage

        This can be passed to ``controlvm VM changeuartmodeX`` or
        ``modifyvm VMNAME --uartmodeX``
        """
        ...

    @staticmethod
    def parse_machinereadable(
        arg: Optional[str],
    ) -> Optional["VBoxUartMode"]:
        """Parse uartmodeX keys from --machinereadable mode"""
        if arg is None:
            return None
        if arg == "disconnected":
            return VBoxUartModeDisconnected()
        if arg.startswith("file,"):
            return VBoxUartModeFile(arg[5:])
        if arg.startswith("tcpserver,"):
            return VBoxUartModeTCPServer(int(arg[10:]))
        raise ValueError(f"Dont know how to parse machinereadable uartmode {arg!r}")


@dataclass
class VBoxUartModeDisconnected(VBoxUartMode):
    def as_cmd_args(self):
        return ["disconnected"]


@dataclass
class VBoxUartModeFile(VBoxUartMode):
    path: str

    def __init__(self, path: str = ""):
        self.path = path

    def as_cmd_args(self):
        return ["file", self.path]


@dataclass
class VBoxUartModeTCPServer(VBoxUartMode):
    port: int

    def __init__(self, port: int = -1):
        self.port = port

    def as_cmd_args(self):
        return ["tcpserver", str(self.port)]


def parse_systemproperties(text: str) -> Dict[str, str]:
    """Parse output of `VBoxManage list systemproperties`"""
    res = dict()
    for line in text.splitlines():
        if not line.strip():
            continue
        m = re.match(r"(?P<key>.*?):\s*(?P<val>.*)", line)
        if not m:
            logger.error("Failed to parse %r", line)
            continue
        res[m.group("key")] = m.group("val")
    return res


def try_get_vboxmanage_exe() -> Optional[str]:
    """Try to find the vboxmanage executable

    If VBoxManage is found in PATH just return "VBoxManage"
    On windows check for a hardcoded location and return the absolute path

    Returns None on failure
    """
    result = shutil.which("VBoxManage")
    if result:
        return "VBoxManage"
    if sys.platform == "win32":
        # We could use the registry
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Oracle\VirtualBox"
            ) as key:
                installdir = winreg.QueryValueEx(key, "InstallDir")[0]
                result = os.path.join(installdir, "VBoxManage.exe")
                if os.path.exists(result):
                    return result
        except OSError:
            logger.debug(
                "Failed to read VirtualBox InstallDir from registry", exc_info=True
            )
            pass
        default_windows_path = r"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
        if os.path.exists(default_windows_path):
            return default_windows_path
    return None


def get_vboxmanage_exe() -> str:
    result = try_get_vboxmanage_exe()
    if result is None:
        raise ValueError("Failed to find VBoxManage")
    return result


class VBoxManage:
    """Wrap the ``VBoxManage`` tool

    Official documentation: https://www.virtualbox.org/manual/ch08.html
    """

    _vboxmanage_exe = None
    explict_vboxmanage_exe = None

    def __init__(self, vboxmanage_exe: Optional[str] = None):
        self.explicit_vboxmanage_exe = vboxmanage_exe

    def get_vboxmanage_exe(self) -> str:
        """Get VBoxManage executable or raise ValueError"""
        if self.explicit_vboxmanage_exe is not None:
            return self.explicit_vboxmanage_exe
        if self._vboxmanage_exe is None:
            self._vboxmanage_exe = get_vboxmanage_exe()
        return self._vboxmanage_exe

    def run(self, args, **kw) -> subprocess.CompletedProcess:
        """Run VBoxManage"""
        return subprocess.run([self.get_vboxmanage_exe()] + args, **kw)

    def list_vms(self) -> Dict[str, UUID]:
        """List virtual machines by name and uuid"""
        runres = self.run(["list", "vms"], capture_output=True, text=True, check=True)
        res: Dict[str, UUID] = {}
        for line in runres.stdout.splitlines():
            m = re.match(r'"(?P<name>.*)" {(?P<guid>[a-f0-9-]+)}', line)
            if not m:
                logger.error("Failed to parse %r", line)
                continue
            res[m.group("name")] = UUID(m.group("guid"))
        return res

    def get_systemproperties(self) -> Dict[str, str]:
        """Returned parsed output of ``VBoxManage list systemproperties``"""
        runres = self.run(
            ["list", "systemproperties"],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        return parse_systemproperties(runres.stdout)

    def get_machinefolder(self) -> str:
        """
        Get the default machinefolder from ``VBoxManage list systemproperties``

        See: https://www.virtualbox.org/manual/UserManual.html#vboxconfigdata-machine-folder
        """
        return self.get_systemproperties()["Default machine folder"]

    def get_vminfo_dict(self, vmid: VMID) -> VMInfoDictType:
        out = self.run(
            ["showvminfo", str(vmid), "--machinereadable"],
            encoding="UTF-8",
            capture_output=True,
        )
        return parse_vminfo(out.stdout)

    def get_vminfo_string(
        self,
        vmid: VMID,
        key: str,
        default: Optional[str] = None,
    ) -> str:
        """Get a string from `.get_vminfo_dict` or raise ValueError if missing"""
        val = self.get_vminfo_dict(vmid).get(key)
        if val is None:
            if default is None:
                raise ValueError(f"Missing {key} for vm {vmid}")
            else:
                return default
        else:
            if not isinstance(val, str):
                raise ValueError(f"Unexpected {key}={val} for vm {vmid}")
            else:
                return val

    def get_vm_state(self, vmid: VMID, default=None) -> str:
        """Get current VMState field as a string

        VMState transitions are documented here: https://www.virtualbox.org/sdkref/_virtual_box_8idl.html#a80b08f71210afe16038e904a656ed9eb
        """
        return self.get_vminfo_string(vmid, "VMState", default=default)

    def get_uart_mode(self, vmid: VMID, port: int) -> str:
        return self.get_vminfo_string(vmid, f"uartmode{port}")

    def get_uart_mode_all(self, vmid: VMID) -> Dict[int, str]:
        """Get all UART modes as a dict of port -> mode"""
        data = self.get_vminfo_dict(vmid)
        result = dict()
        for port in range(1, 5):
            key = f"uartmode{port}"
            val = data.get(key, "off")
            if not isinstance(val, str):
                raise ValueError(f"Unexpected {key}={val} type {type(val)}")
            else:
                result[port] = val
        return result

    def _modifyvm_uartmode(
        self,
        vmid: VMID,
        port: int,
        mode_args: List[str],
    ):
        cmd = ["modifyvm", str(vmid), f"--uartmode{port}"] + mode_args
        self.run(cmd, check=True)

    def _controlvm_changeuartmode(
        self,
        vmid: VMID,
        port: int,
        mode_args: List[str],
    ):
        cmd = ["controlvm", str(vmid), f"changeuartmode{port}"] + mode_args
        self.run(cmd, check=True)

    def set_uart_mode_args(self, vmid: VMID, port: int, mode_args: List[str]):
        if self.get_vm_state(vmid) == "running":
            self._controlvm_changeuartmode(vmid, port, mode_args)
        else:
            self._modifyvm_uartmode(vmid, port, mode_args)

    def get_uart_mode_object(self, vmid: VMID, port: int) -> VBoxUartMode:
        mode = self.get_uart_mode(vmid, port)
        result = VBoxUartMode.parse_machinereadable(mode)
        if result is None:
            raise ValueError(f"Failed to parse uartmode={mode}")
        return result

    def set_uart_mode_object(self, vmid: VMID, port: int, mode: VBoxUartMode):
        self.set_uart_mode_args(vmid, port, mode.as_cmd_args())

    def get_vboxmanage_version(self) -> str:
        """Get the version of the vboxmanage command"""
        proc = self.run(["--version"], text=True, check=True, capture_output=True)
        out = proc.stdout
        return out.splitlines()[-1].strip()

    def check_user_versus_kernel_version(self) -> Optional[bool]:
        """Check if userspace and kernel components are in sync"""
        vboxmanage_version = self.get_vboxmanage_version()
        vboxmanage_revision = parse_vboxmanage_version_revision(vboxmanage_version)
        if sys.platform == "linux":
            vboxdrv_version_path = Path("/sys/module/vboxdrv/version")
            if not vboxdrv_version_path.exists():
                logger.error("Missing %r", vboxdrv_version_path)
                return False
            vboxdrv_version = vboxdrv_version_path.read_text().strip()
            vboxdrv_revision = parse_vboxdrv_version_revision(vboxdrv_version)
            if vboxdrv_revision == vboxmanage_revision:
                logger.debug(
                    "Matching vboxmanage %r and vboxdrv %r",
                    vboxmanage_version,
                    vboxdrv_version,
                )
                return True
            else:
                logger.error(
                    "Mismatch vboxmanage %r and vboxdrv %r",
                    vboxmanage_version,
                    vboxdrv_version,
                )
                return False
        else:
            logger.warning(
                "Version check not implemented for platform %r", sys.platform
            )
            return None


def parse_vboxmanage_version_revision(ver: str) -> int:
    m = re.search(r"r(\d+)$", ver)
    if not m:
        raise ValueError(f"Failed to parse vboxmanage version {ver}")
    return int(m[1])


def parse_vboxdrv_version_revision(ver: str) -> int:
    m = re.search(r" r(\d+) ", ver)
    if not m:
        raise ValueError(f"Failed to parse vboxdrv version {ver}")
    return int(m[1])


def _bump_logging(delta, logger_name=None):
    """Adjust logging on one logger."""
    logger = logging.getLogger(logger_name)
    old_level = logger.getEffectiveLevel()
    logger.setLevel(old_level + delta)


def _add_logging_arguments(parser):
    """Add -v --verbose -q --quiet args to an ArgumentParser.

    The options have a callback action which immediately enforces the log level.
    """

    class IncreaseLogLevelAction(argparse.Action):
        def __call__(self, *args, **kwargs):
            _bump_logging(-10)

    class DecreaseLogLevelAction(argparse.Action):
        def __call__(self, *args, **kwargs):
            _bump_logging(+10)

    parser.add_argument(
        "-v",
        "--verbose",
        nargs=0,
        help="Increase logging level.",
        action=IncreaseLogLevelAction,
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        nargs=0,
        help="Decrease logging level.",
        action=DecreaseLogLevelAction,
        default=argparse.SUPPRESS,
    )


def create_parser(extra_subcmd_callback=None):
    parser = argparse.ArgumentParser(description=__doc__, prog="pyvboxcli")
    _add_logging_arguments(parser)
    sub = parser.add_subparsers(dest="subcmd", metavar="SUBCMD", required=True)
    sub.add_parser("list-vms", help="List virtual machines by name and uuid")

    subparser = sub.add_parser(
        "get-vm-state",
        help="Get VMState via showvminfo",
    )
    subparser.add_argument("-j", "--json", action="store_true", help="Output JSON")
    subparser.add_argument(
        "vmname",
        help="vmname or uuid. If missing show a table with VMState for all vms",
        nargs="?",
    )

    subparser = sub.add_parser("get-uart-mode", help="Get uart mode")
    subparser.add_argument("vmname", help="target")
    subparser.add_argument(
        "port", help="port number (1-4), default show all", type=int, nargs="?"
    )

    subparser = sub.add_parser("set-uart-mode", help="Set uart mode")
    subparser.add_argument("vmname", help="target")
    subparser.add_argument("port", help="port number (1-4)", type=int)
    subparser.add_argument("mode_args", nargs="+")

    subparser = sub.add_parser(
        "connect-uart", help="Connect to UART in current mode (limited support)"
    )
    subparser.add_argument("vmname", help="target")
    subparser.add_argument("port", help="port number (1-4)", type=int)

    subparser = sub.add_parser(
        "picocom-uart",
        help="Interact with an UART using picocom",
    )
    subparser.add_argument("vmname", help="target")
    subparser.add_argument("port", help="port number (1-4)", type=int)
    subparser = sub.add_parser(
        "getmachinefolder",
        help="Get the ``machinefolder`` property, see https://www.virtualbox.org/manual/UserManual.html#vboxconfigdata-machine-folder",
    )

    subparser = sub.add_parser(
        "check-user-versus-kernel-version",
        help="Check vboxmanage and vboxdrv match",
    )

    if extra_subcmd_callback:
        extra_subcmd_callback(parser, sub)

    return parser


@contextmanager
def vbox_change_uartmode(
    vbox: VBoxManage, vmid: VMID, port: int, newmode: VBoxUartMode
):
    """Change uartmode on a virtualbox vm and then restore it"""
    oldmode = vbox.get_uart_mode_object(vmid, port)
    try:
        vbox.set_uart_mode_object(vmid, port, newmode)
        yield
    finally:
        vbox.set_uart_mode_object(vmid, port, oldmode)


@contextmanager
def socat_pty_link(arg):
    from tempfile import TemporaryDirectory

    import waiting

    with TemporaryDirectory() as tmp:
        pty_path = tmp + "/pty"
        cmd = ["socat", arg, f"PTY,rawer,link={pty_path}"]

        def check_pty_path():
            return os.path.exists(pty_path)

        subprocess.Popen(cmd)
        waiting.wait(check_pty_path, timeout_seconds=5, sleep_seconds=0.1)

        yield pty_path


def picocom_tcpserver_console(tcp_server_port: int):
    socat_arg = f"TCP-CONNECT:127.0.0.1:{tcp_server_port}"
    with socat_pty_link(socat_arg) as pty_path:
        cmd = ["picocom", pty_path]
        subprocess.run(cmd)


def get_free_local_port() -> int:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("", 0))
        return sock.getsockname()[1]


def get_free_local_port_for_vbox(port=None):
    if port is None:
        port = get_free_local_port()
        logger.debug("Using free local port %d for vbox uart tcpserver", port)
    return port


def picocom_uart(vbox: VBoxManage, vmid: VMID, port: int, tcp_server_port=None):
    """Run picocom against an uart on a VBOX vm"""
    tcp_server_port = get_free_local_port_for_vbox()
    newmode = VBoxUartModeTCPServer(tcp_server_port)
    with vbox_change_uartmode(vbox, vmid, port, newmode):
        picocom_tcpserver_console(tcp_server_port)


class Tool:
    """Command-line handler class"""

    def __init__(self):
        self.opts = argparse.Namespace()
        self._vbox = None

    def parse_args(self, argv):
        create_parser().parse_args(argv, self.opts)

    def main(self, argv=None):
        """Main function for command-line tool"""
        self.parse_args(argv)
        self.run()

    def init_vbox(self):
        return VBoxManage()

    @property
    def vbox(self) -> VBoxManage:
        if self._vbox is None:
            self._vbox = self.init_vbox()
        return self._vbox

    def run_get_uart_mode(self):
        if self.opts.port is None:
            mode_dict = self.vbox.get_uart_mode_all(self.opts.vmname)
            for port in range(1, 5):
                mode = mode_dict.get(port, "off")
                sys.stdout.write(f"{port}:\t{mode}\n")
        else:
            sys.stdout.write(
                f"{self.vbox.get_uart_mode(self.opts.vmname, self.opts.port)}\n"
            )

    def run_get_vm_state(self):
        if self.opts.vmname:
            state = self.vbox.get_vm_state(self.opts.vmname)
            if self.opts.json:
                sys.stdout.write(json.dumps(state, indent=2))
            else:
                sys.stdout.write(f"{state}\n")
            return
        else:
            data = {}
            for vmname in self.vbox.list_vms().keys():
                data[vmname] = self.vbox.get_vm_state(vmname)
            if self.opts.json:
                sys.stdout.write(json.dumps(data, indent=2))
            else:
                for name, stat in data.items():
                    sys.stdout.write(f"{name}\t{stat}\n")

    def run(self):
        opts = self.opts
        vbox = self.vbox

        def show_pprint(arg):
            import pprint

            sys.stdout.write(pprint.pformat(arg) + "\n")

        if opts.subcmd == "list-vms":
            res = vbox.list_vms()
            show_pprint(res)
        elif opts.subcmd == "get-vm-state":
            self.run_get_vm_state()
        elif opts.subcmd == "get-uart-mode":
            self.run_get_uart_mode()
        elif opts.subcmd == "set-uart-mode":
            vbox.set_uart_mode_args(opts.vmname, opts.port, opts.mode_args)
        elif opts.subcmd == "picocom-uart":
            picocom_uart(vbox, opts.vmname, opts.port)
        elif opts.subcmd == "connect-uart":
            mode = vbox.get_uart_mode(opts.vmname, opts.port)
            mode_type, mode_argv = mode.split(",", 1)
            if mode_type == "file":
                logger.warning("follow readonly file %r", mode_argv)
                cmd = ["tail", "-F", mode_argv]
                os.execvp(cmd[0], cmd)
            else:
                raise Exception("Can't connect to uartmode={mode}")
        elif opts.subcmd == "getmachinefolder":
            sys.stdout.write(f"{vbox.get_machinefolder()}\n")
        elif opts.subcmd == "check-user-versus-kernel-version":
            ret = vbox.check_user_versus_kernel_version()
            sys.exit(1 if ret is False else 0)
        else:
            raise Exception(f"Unknown subcmd {opts.subcmd}")


def main(argv=None):
    Tool().main(argv)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
