from subprocess import check_output
from typing import Optional, Union
import wmi

try:
    from install.task import Task, ExecutableTask
except ImportError:
    from ..install.task import Task, ExecutableTask


_WMI = wmi.WMI()


def shutdown_task(timeout: Union[int, float] = 1):
    return ExecutableTask("Shutdown", "shutdown", ("/s", "/t", str(timeout)))


def reboot_task(timeout: Union[int, float] = 1):
    return ExecutableTask("Reboot", "shutdown", ("/r", "/t", str(timeout)))


def cancel_halt_task():
    """Cancel scheduled shutdown/reboot"""
    return ExecutableTask("Cancel Halt", "shutdown", ("/a",))


def set_password_task(username: str, password: Optional[str]):
    if len(password) > 0:
        return ExecutableTask(
            "Set Password",
            "powershell.exe",
            options=("Set-LocalUser", "-Name", username, "-Password",
                     f"(ConverTo-SecureString {str(password)} -AsPlainText -Force"))
    else:
        return ExecutableTask(
            "Set Password",
            "powershell.exe",
            options=("Set-LocalUser", "-Name", username,
                     "-Password", "(new-object System.Security.SecureString)"))


def get_current_usrname() -> str:
    return check_output(["powershell.exe", "$Env:UserName"]).strip().decode()


def get_users_info() -> list[wmi._wmi_object]:
    return _WMI.Win32_UserAccount()
