import wmi


class WmiWrapper:
    """Providing system hardware information
    """

    def __init__(self) -> None:
        self.c = wmi.WMI()

    def cpu_info(self) -> list[wmi._wmi_object]:
        return self.c.Win32_Processor()

    def gpu_info(self) -> list[wmi._wmi_object]:
        return self.c.Win32_VideoController()

    def ram_info(self) -> list[wmi._wmi_object]:
        return self.c.Win32_PhysicalMemory()

    def mother_board_info(self) -> list[wmi._wmi_object]:
        return self.c.Win32_BaseBoard()

    def nic_info(self) -> list[wmi._wmi_object]:
        return self.c.Win32_NetworkAdapter()

    def disk_info(self) -> list[wmi._wmi_object]:
        return self.c.Win32_DiskDrive()

    def partition_info(self) -> list[wmi._wmi_object]:
        return self.c.Win32_DiskPartition()
