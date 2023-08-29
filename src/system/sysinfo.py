try:
    from wmi_wrapper import WmiWrapper
except ImportError:
    from .wmi_wrapper import WmiWrapper


class HwInfo:

    def __init__(self) -> None:
        self.hwd = WmiWrapper()

    def get_cpu_descr(self) -> list[str]:
        """Get system CPUs description (name)
        """
        output = []
        try:
            for cpu in self.hwd.cpu_info():
                output.append(cpu.name)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]

    def get_gpu_descr(self) -> list[str]:
        """Get system GPUs description (name + VRAM)
        """
        output = []
        try:
            for gpu in self.hwd.gpu_info():
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
            for mb in self.hwd.mother_board_info():
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
            for ram in self.hwd.ram_info():
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
            for nic in self.hwd.nic_info():
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
            for disk in self.hwd.disk_info():
                tmp = disk.Model + " @ " + \
                    str(int(disk.Size) // (1000**3)) + "GB"
                output.append(tmp)

            return output if len(output) > 0 else ["Not Found"]
        except Exception as e:
            return ["[ERROR]"]


if __name__ == "__main__":
    s = HwInfo()
    print(s.get_disk_descr())
