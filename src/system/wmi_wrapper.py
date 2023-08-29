import wmi


class WmiWrapper:
    """Providing system hardware information
    """

    def __init__(self) -> None:
        self.c = wmi.WMI()

    def get_cpu_dets(self) -> list[wmi._wmi_object]:
        return self.c.Win32_Processor()

    def get_gpu_dets(self) -> list[wmi._wmi_object]:
        return self.c.Win32_VideoController()

    def get_ram_dets(self) -> list[wmi._wmi_object]:
        return self.c.Win32_PhysicalMemory()

    def get_mb_dets(self) -> list[wmi._wmi_object]:
        return self.c.Win32_BaseBoard()

    def get_nic_dets(self) -> list[wmi._wmi_object]:
        return self.c.Win32_NetworkAdapter()

    def get_disk_dets(self) -> list[wmi._wmi_object]:
        return self.c.Win32_DiskDrive()
