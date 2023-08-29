import subprocess
from wmi_wrapper import WmiWrapper

wmi = WmiWrapper()

disks = wmi.disk_info()
partition = wmi.partition_info()

# Set-Partition -DiskNumber 1 -PartitionNumber 1 -NewDriverLetter D


def get_raw_disk_index():
    non_raw_indexes = set(
        [partition.DiskIndex for partition in wmi.partition_info()])
    return [
        idx for idx in (disk.Index for disk in wmi.disk_info())
        if idx not in non_raw_indexes
    ]


def initialise_disk_by_index(disk_index: int, style: str = 'MBR') -> bool:
    proc = subprocess.run(
        f"powershell Initialize-Disk -Number {disk_index} -PartitionStyle {style}",
        shell=True)
    return proc.returncode == 0

# def create_parition(disk_index: int,)
