import logging
import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import *
from uuid import UUID

import pexpect
import pytest
import vagrant
from vagrant import Vagrant

from pyvboxcli import (
    VBoxManage,
    VBoxUartMode,
    VBoxUartModeDisconnected,
    VBoxUartModeFile,
    VBoxUartModeTCPServer,
)

logger = logging.getLogger(__name__)


def get_vagrant_cwd() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "vagrant-target")


class VagrantTarget:
    """Vagrant target for selftest"""

    vagrant: Vagrant
    _was_running: Optional[bool] = None

    @property
    def cwd(self) -> str:
        return get_vagrant_cwd()

    def __init__(self) -> None:
        self.vagrant = Vagrant(
            root=self.cwd,
            out_cm=vagrant.stdout_cm,
            err_cm=vagrant.stderr_cm,
        )

    def run(self, argv: List[str], **kw):
        logger.info("RUN: vagrant %s", shlex.join(argv))
        return subprocess.run(["vagrant"] + argv, cwd=self.cwd, **kw)

    def run_ssh(self, script: str, **kw) -> subprocess.CompletedProcess:
        argv = ["ssh", "-c", script]
        return self.run(argv, **kw)

    def __enter__(self):
        status: List[vagrant.Status]
        status = self.vagrant.status()
        assert len(status) == 1
        if status[0].state == "running":
            logger.warning("vagrant was already running, skip up")
            self._was_running = True
        else:
            self._was_running = False
            self.vagrant.up()
        return self

    def __exit__(self, *a):
        if self._was_running:
            logger.warning("vagrant was already running, skip halt")
        else:
            self.vagrant.halt()
        self._was_running = None


@pytest.fixture(scope="session")
def vagrant_target():
    if not shutil.which("vagrant"):
        pytest.skip(f"Missing vagrant in PATH")
    with VagrantTarget() as t:
        yield t


class Test:
    target: VagrantTarget
    vbox = VBoxManage()
    _name: Optional[str] = None
    _uuid: Optional[UUID] = None

    def _fetch_name_uuid(self):
        full_list = self.vbox.list_vms()

        def fun(arg):
            # Name looks like ${VAGRANT_CWD}_${VMNAME}"
            return arg[0].startswith("vagrant-target_pyvboxcli_")

        match_list = list(filter(fun, full_list.items()))
        if len(match_list) != 1:
            raise ValueError("Expected exactly one match")
        self._name, self._uuid = match_list[0]

    @property
    def vbox_name(self) -> str:
        if self._name is None:
            self._fetch_name_uuid()
        assert self._name is not None
        return self._name

    @pytest.fixture(autouse=True)
    def init(self, vagrant_target):
        self.target = vagrant_target

    def test_ssh_hello(self):
        res = self.target.run_ssh(
            "echo $((1 + 2))",
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        )
        assert res.stdout.strip() == "3"

    def test_vmname(self):
        assert self.vbox.get_vm_state(self.vbox_name) == "running"

    def test_machinefolder(self):
        machinefolder = self.vbox.get_machinefolder()
        logger.info("vbox machinefolder: %r", machinefolder)
        assert os.path.exists(machinefolder)

    def test_uartmode(self):
        """Confirm expectations about remote status"""
        data = self.vbox.get_uart_mode_all(self.vbox_name)
        logger.info("data:\n%s", data)

        assert data[1].startswith("file")
        assert data[1].endswith("uart1.txt")
        uartmode1 = VBoxUartMode.parse_machinereadable(data[1])
        assert isinstance(uartmode1, VBoxUartModeFile)
        assert Path(uartmode1.path) == Path(get_vagrant_cwd()) / "uart1.txt"

        assert data[2].endswith("uart2.txt")
        assert data[3] == "disconnected"
        assert data[4] == "off"

    def test_ssh_echo_tty(self):
        msg = f"PING tty0 {time.time()}"
        self.target.run_ssh(f"sudo sh -c 'echo {msg} > /dev/ttyS0'")
        log_path = Path(get_vagrant_cwd()) / "uart1.txt"
        assert msg in log_path.read_text()

    @pytest.mark.skipif(sys.platform.startswith("win"), reason="Windows")
    def test_picocom(self):
        outer_argv = [
            sys.executable,
            "-m",
            "pyvboxcli",
            "picocom-uart",
            self.vbox_name,
            "2",
        ]
        outer_cmd = shlex.join(outer_argv)
        oldmode = self.vbox.get_uart_mode_object(self.vbox_name, 2)
        assert isinstance(oldmode, VBoxUartModeFile)
        with pexpect.spawn(outer_cmd, timeout=5, encoding="utf-8") as spawn:
            spawn.expect("Terminal ready")
            msg = f"PING tty1 {time.time()}"
            newmode = self.vbox.get_uart_mode_object(self.vbox_name, 2)
            assert isinstance(newmode, VBoxUartModeTCPServer)
            self.target.run_ssh(f"sudo sh -c 'echo {msg} > /dev/ttyS1'")
            spawn.expect(msg)
            spawn.sendcontrol("a")
            spawn.sendcontrol("x")
            spawn.expect("Thanks for using picocom")
            spawn.wait()
            newmode = self.vbox.get_uart_mode_object(self.vbox_name, 2)
            assert isinstance(newmode, VBoxUartModeFile)

    def test_disk_path(self):
        disk = self.vbox.get_vminfo_string(self.vbox_name, "SATA Controller-0-0")
        assert disk is not None
        assert os.path.exists(disk)

    def test_user_versus_kernel_version(self):
        assert self.vbox.check_user_versus_kernel_version()

    def test_user_versus_kernel_version_cli(self):
        argv = [
            sys.executable,
            "-m",
            "pyvboxcli",
            "check-user-versus-kernel-version",
        ]
        subprocess.run(argv, check=True)
