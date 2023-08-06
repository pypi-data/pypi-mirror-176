# SPDX-License-Identifier: MIT
import contextlib
import json
import logging
from subprocess import CompletedProcess
from unittest import mock

import pytest

import pyvboxcli
from pyvboxcli import (
    VBoxManage,
    VBoxUartMode,
    main,
    parse_vboxdrv_version_revision,
    parse_vboxmanage_version_revision,
    parse_vminfo,
)

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def mock_subprocess_module():
    with mock.patch("pyvboxcli.try_get_vboxmanage_exe", return_value="VBoxManage"):
        with mock.patch("pyvboxcli.subprocess") as mock_subprocess:
            yield mock_subprocess


def test_vbox_list_vms(capsys):
    def mock_run(args, **kwargs):
        if args == ["VBoxManage", "list", "vms"]:
            return CompletedProcess(
                args, 0, stdout='"mockvm" {bad4d6b9-10e9-4e65-ab56-41ec9a0ab9c5}'
            )
        else:
            raise Exception(f"Unexpected call {args} {kwargs}")

    with mock_subprocess_module() as mock_subprocess:
        mock_subprocess.run.side_effect = mock_run
        main(["list-vms"])
    out = capsys.readouterr().out
    assert out == "{'mockvm': UUID('bad4d6b9-10e9-4e65-ab56-41ec9a0ab9c5')}\n"


def test_vbox_vminfo(capsys):
    stdout = """
VMState="running"
Memory=8192
uartmode2="file,/tmp/vm.log"
"""
    with mock_subprocess_module() as mock_subprocess:
        mock_subprocess.run.return_value = CompletedProcess([], 0, stdout=stdout)
        main(["get-vm-state", "mockvm"])
        out = capsys.readouterr().out
        assert out == "running\n"
        main(["get-uart-mode", "mockvm", "2"])
        out = capsys.readouterr().out
        assert out == "file,/tmp/vm.log\n"


def test_vbox_vmstate_default(capsys):
    with mock_subprocess_module() as mock_subprocess:
        mock_subprocess.run.return_value = CompletedProcess(
            [], 0, stdout="Memory=8193\n"
        )
        vbox = VBoxManage()
        assert vbox.get_vm_state("aaa", default="none") == "none"
        mock_subprocess.run.return_value = CompletedProcess(
            [], 0, stdout='VMState="running"\n'
        )
        assert vbox.get_vm_state("bbb", default="none") == "running"


def test_vbox_vmstate_all(capsys):
    with mock.patch("pyvboxcli.VBoxManage") as vbox_ctor:
        vbox = vbox_ctor.return_value
        vbox.list_vms.return_value = dict(aaa=None, bbb=None)
        vbox.get_vm_state.return_value = "running"
        main(["get-vm-state"])
        out = capsys.readouterr().out
        assert vbox.list_vms.called
        assert out == "aaa\trunning\nbbb\trunning\n"


def test_vbox_vmstate_all_json(capsys):
    with mock.patch("pyvboxcli.VBoxManage") as vbox_ctor:
        vbox = vbox_ctor.return_value
        vbox.list_vms.return_value = dict(aaa=None, bbb=None)
        vbox.get_vm_state.return_value = "running"
        main(["get-vm-state", "--json"])
        out = capsys.readouterr().out
        assert vbox.list_vms.called
        assert json.loads(out) == dict(aaa="running", bbb="running")


def test_vbox_set_uart_mode(capsys):
    stdout = """
VMState="running"
"""
    with mock_subprocess_module() as mock_subprocess:
        mock_subprocess.run.return_value = CompletedProcess([], 0, stdout=stdout)
        main(["set-uart-mode", "mockvm", "2", "disconnected"])
        inner_cmd = [
            "VBoxManage",
            "controlvm",
            "mockvm",
            "changeuartmode2",
            "disconnected",
        ]
        mock_subprocess.run.assert_called_with(inner_cmd, check=True)


def test_vbox_uart_file(capsys):
    with mock_subprocess_module() as mock_subprocess:
        mock_subprocess.run.return_value = CompletedProcess(
            [], 0, stdout='VMState="running"\nuartmode2="file,/tmp/vm.log"'
        )
        with mock.patch("os.execvp") as mock_execvp:
            main(["connect-uart", "mockvm", "2"])
            assert mock_execvp.call_args.args == ("tail", ["tail", "-F", "/tmp/vm.log"])


def test_vbox_uart_abstract():
    """Deliberate test for exception on abstract class instantiation"""
    with pytest.raises(Exception):
        VBoxUartMode()  # type: ignore


def test_parse_vminfo():
    assert parse_vminfo('tracing-config=""').get("tracing-config") == ""
    assert parse_vminfo("Memory=4096").get("Memory") == 4096


def test_parse_vminfo_weird():
    text = """
VideoMode="800,600,32"@0,0 1
VRDEClients==0
GuestAdditionsFacility_VirtualBox Base Driver=50,1637864788949
GuestAdditionsFacility_Seamless Mode=0,1637864788958
GuestAdditionsFacility_Graphics Mode=0,1637864788942
"IDE Controller-0-0"="/home/leonard/VirtualBox VMs/somevm.vmdk"
"""
    data = parse_vminfo(text)
    assert data["VideoMode"] == '"800,600,32"@0,0 1'
    assert data["VRDEClients"] == "=0"
    assert data["GuestAdditionsFacility_VirtualBox Base Driver"] == "50,1637864788949"
    assert data["IDE Controller-0-0"] == "/home/leonard/VirtualBox VMs/somevm.vmdk"


def test_uartmode():
    m = pyvboxcli.VBoxUartMode.parse_machinereadable("tcpserver,19544")
    assert isinstance(m, pyvboxcli.VBoxUartModeTCPServer)
    assert m.port == 19544
    assert m == pyvboxcli.VBoxUartModeTCPServer(19544)
    assert m != pyvboxcli.VBoxUartModeTCPServer(123)
    assert m != pyvboxcli.VBoxUartModeDisconnected()
    assert m.as_cmd_args() == ["tcpserver", "19544"]
    assert pyvboxcli.VBoxUartModeDisconnected() == pyvboxcli.VBoxUartModeDisconnected()
    m = pyvboxcli.VBoxUartMode.parse_machinereadable("disconnected")
    assert m is not None
    assert m.as_cmd_args() == ["disconnected"]
    assert pyvboxcli.VBoxUartMode.parse_machinereadable(None) is None


def test_vbox_nocmd(capsys):
    with pytest.raises(SystemExit):
        main([])
    assert "arguments are required" in capsys.readouterr().err


def test_vbox_badsubcmd(capsys):
    with pytest.raises(SystemExit):
        main(["badbadbad"])
    assert "invalid choice" in capsys.readouterr().err


def test_parse_systemproperties():
    text = """
Maximum Devices per Floppy Port: 2
Default machine folder:          /home/leonard/VirtualBox VMs
Raw-mode Supported:              no
Maximum PIIX3 Floppy Controllers:1
    """
    data = pyvboxcli.parse_systemproperties(text)
    assert data["Maximum Devices per Floppy Port"] == "2"
    assert data["Default machine folder"] == "/home/leonard/VirtualBox VMs"
    assert data["Maximum PIIX3 Floppy Controllers"] == "1"


def test_parse_systemproperties_windows():
    text = r"""
Default machine folder:          C:\Users\leonard\VirtualBox VMs
    """
    data = pyvboxcli.parse_systemproperties(text)
    assert data["Default machine folder"] == r"C:\Users\leonard\VirtualBox VMs"


def test_parse_vboxmanage_version_revision():
    arg = "6.1.34_Ubuntur150636"
    assert parse_vboxmanage_version_revision(arg) == 150636


def test_parse_vboxdrv_version_revision():
    arg = "6.1.34_Ubuntu r150636 (0x00320000)"
    assert parse_vboxdrv_version_revision(arg) == 150636
