import os
import sys
from typing import Final

DIR_ROOT: Final[os.PathLike] = os.path.dirname(sys.executable) \
    if getattr(sys, 'frozen', False) \
    else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIR_CONF: Final[os.PathLike] = os.path.join(DIR_ROOT, "conf")
DIR_PIC: Final[os.PathLike] = os.path.join(DIR_ROOT, "pic")
DIR_DRI: Final[os.PathLike] = os.path.join(DIR_ROOT, "driver")

DIR_FLAG_PRESETS = {
    "Intel Lan Driver": ["/s"],
    "Realtek Lan Driver": ["-s"],
    "Nvidia Display": ["-s", "-noreboot", "Display.Driver"],
    "AMD Display": ["-install"],
    "Intel Wifi": ["-q"],
    "Intel BT": ["/quiet", "/norestart"],
    "Intel Chipset": ["-s", "-norestart"],
    "AMD Chipset": ["/S"]
}
