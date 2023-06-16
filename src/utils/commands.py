import sys
from subprocess import Popen, check_output
from typing import Optional, Union
import wmi


_WMI = wmi.WMI()


def shutdown(timeout: Union[int, float] = 1):
    return Popen(["shutdown", "/s", "/t", str(timeout)], shell=True, stdout=sys.stdout)


def reboot(timeout: Union[int, float] = 1):
    return Popen(["shutdown", "/r", "/t", str(timeout)], shell=True, stdout=sys.stdout)


def cancel_halt():
    """Cancel scheduled shutdown/reboot
    """
    return Popen(["shutdown", "/a"], shell=True, stdout=sys.stdout)


def set_password(username: str, password: Optional[str]):
    if len(password) > 0:
        return Popen(
            ["powershell.exe", "Set-LocalUser", "-Name", username, "-Password",
                f"(ConverTo-SecureString {str(password)} -AsPlainText -Force)"],
            stdout=sys.stdout)
    else:
        return Popen(
            ["powershell.exe", "Set-LocalUser", "-Name", username,
                "-Password", "(new-object System.Security.SecureString)"],
            stdout=sys.stdout)


def get_current_usrname() -> str:
    return check_output(["powershell.exe", "$Env:UserName"]).strip().decode()


def get_users_info() -> list[wmi._wmi_object]:
    return _WMI.Win32_UserAccount()
