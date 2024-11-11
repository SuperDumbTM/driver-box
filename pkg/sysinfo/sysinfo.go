package sysinfo

import (
	"github.com/yusufpapurcu/wmi"
)

type SysInfo struct{}

func (i SysInfo) CpuInfo() ([]Win32_Processor, error) {
	var cls []Win32_Processor
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}

func (i SysInfo) MotherboardInfo() ([]Win32_BaseBoard, error) {
	var cls []Win32_BaseBoard
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}

func (i SysInfo) MemoryInfo() ([]Win32_PhysicalMemory, error) {
	var cls []Win32_PhysicalMemory
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}

func (i SysInfo) GpuInfo() ([]Win32_VideoController, error) {
	var cls []Win32_VideoController
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}

func (i SysInfo) NicInfo() ([]Win32_NetworkAdapter, error) {
	var cls []Win32_NetworkAdapter
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}

func (i SysInfo) DiskInfo() ([]Win32_DiskDrive, error) {
	var cls []Win32_DiskDrive
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}

func (i SysInfo) DiskParitionInfo() ([]Win32_DiskPartition, error) {
	var cls []Win32_DiskPartition
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}

func (i SysInfo) UserAccountInfo() ([]Win32_UserAccount, error) {
	var cls []Win32_UserAccount
	q := wmi.CreateQuery(&cls, "")
	if err := wmi.Query(q, &cls); err != nil {
		return cls, err
	}
	return cls, nil
}
