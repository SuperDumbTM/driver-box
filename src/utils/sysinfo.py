import wmi


class HwDetail:
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


class HwInfo:

    def __init__(self) -> None:
        self.hwd = HwDetail()

    def get_cpu_descr(self) -> list[str]:
        """Get system CPUs description (name)
        """
        output = []
        try:
            for cpu in self.hwd.get_cpu_dets():
                output.append(cpu.name)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]

    def get_gpu_descr(self) -> list[str]:
        """Get system GPUs description (name + VRAM)
        """
        output = []
        try:
            for gpu in self.hwd.get_gpu_dets():
                tmp = gpu.Name + \
                    " (" + str(int(abs(gpu.AdapterRAM)) // 1024**3) + " GB)"
                output.append(tmp)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]

    def get_mb_descr(self) -> list[str]:
        """Get system motherboard description (name)
        """
        output = []
        try:
            for mb in self.hwd.get_mb_dets():
                tmp = mb.Manufacturer.split(" ")[0] + " " + mb.Product
                output.append(tmp)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]

    def get_ram_descr(self) -> list[str]:
        """Get system motherboard description (name + size + speed (running speed))
        """
        output = []
        try:
            for ram in self.hwd.get_ram_dets():
                tmp = ram.Manufacturer + "\t" + ram.PartNumber.strip(" ") + "\t" + str(
                    int(ram.Capacity) // (1024**3)) + "GB@" + str(ram.Speed)
                output.append(tmp)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]

    def get_nic_descr(self) -> list[str]:
        """
        Get system NIC description (name)

        auto discard the following:

        `Microsoft Kernel Debug Network Adapter`, `WAN Miniport (SSTP)`, `WAN Miniport (IKEv2)`,`WAN Miniport (L2TP)`, `WAN Miniport (PPTP)`, `WAN Miniport (PPPOE)`, `WAN Miniport (IP)`, 
        `WAN Miniport (IPv6)`, `WAN Miniport (Network Monitor)`, `Microsoft Wi-Fi Direct Virtual Adapter`, `Microsoft Wi-Fi Direct Virtual Adapter #2`
        """
        output = []
        try:
            dump = ('Microsoft Kernel Debug Network Adapter', 'WAN Miniport (SSTP)', 'WAN Miniport (IKEv2)',
                    'WAN Miniport (L2TP)', 'WAN Miniport (PPTP)', 'WAN Miniport (PPPOE)', 'WAN Miniport (IP)',
                    'WAN Miniport (IPv6)', 'WAN Miniport (Network Monitor)', 'Microsoft Wi-Fi Direct Virtual Adapter',
                    'Microsoft Wi-Fi Direct Virtual Adapter #2', "Bluetooth Device (Personal Area Network)")  # ignor results
            for nic in self.hwd.get_nic_dets():
                if nic.Name not in dump:
                    output.append(nic.Name)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]

    def get_disk_descr(self) -> list[str]:
        """Get system disks description (name + size)
        """
        output = []
        try:
            for disk in self.hwd.get_disk_dets():
                tmp = disk.Model + " @ " + \
                    str(int(disk.Size) // (1000**3)) + "GB"
                output.append(tmp)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]


if __name__ == "__main__":
    s = HwInfo()
    print(s.get_disk_descr())
