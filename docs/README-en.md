# OneClick-Drivers-Installer

![en](https://img.shields.io/badge/README-en-inactive.svg)
[![zh-hk](https://img.shields.io/badge/README-zh--hk-green.svg)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/blob/main/docs/README-zh_hk.md)
[![zh-tw](https://img.shields.io/badge/README-zh--tw-yellow.svg)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/blob/main/docs/README-zh_tw.md)

Easy-to-use driver installer

- [OneClick-Drivers-Installer](#oneclick-drivers-installer)
  - [Download](#download)
  - [Install Option For Common Driver](#install-option-for-common-driver)
  - [Install Setting](#install-setting)
  - [Driver Management](#driver-management)

![main_window](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/assets/71750702/89393ded-61d2-4d6b-b8b8-515fa17ae990)

![progress_window](https://user-images.githubusercontent.com/71750702/226849659-71b77b32-eefb-4649-9865-74050818e249.png)

## Download
The Program<br>
[![version](https://img.shields.io/badge/version-0.5.0-blue)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/releases/tag/v0.5.0)

Driver Pack<br>
[Google Drive](https://drive.google.com/drive/folders/1VqND0o75oBR80Ft2IK8WjTTbXaezmajw?usp=sharing)

- Driver Source<br>
    **Display**<br>
    [GeForce Game Ready Driver (version 531.29 WHQL)](https://www.nvidia.com.tw/download/driverResults.aspx/200222/tw)<br>
    [AMD Software: Adrenalin Edition (version 23.3.1 WHQL)](https://www.amd.com/en/support/graphics/amd-radeon-rx-7000-series/amd-radeon-rx-7900-series/amd-radeon-rx-7900xtx)<br>
    [Intel® 6th-10th Gen Processor Graphics - Windows (version 31.0.101.2115)](https://www.intel.com/content/www/us/en/download/762755/intel-6th-10th-gen-processor-graphics-windows.html)<br>
    [Intel® Arc™ & Iris® Xe Graphics - WHQL - Windows* (version 31.0.101.4146)](https://www.intel.com/content/www/us/en/download/726609/intel-arc-iris-xe-graphics-whql-windows.html)

    **Network**<br>
    [Intel Network Drivers (version 26.2.0.1)](https://tw.msi.com/Motherboard/MAG-Z590-TOMAHAWK-WIFI/support#driver)<br>
    [Intel® Ethernet Adapter Complete Driver Pack (version 28.0)](https://www.intel.com/content/www/us/en/download/15084/intel-ethernet-adapter-complete-driver-pack.html)<br>
    [Realtek PCI-E Ethernet Drivers (version 11-11.10.720.2022)](https://tw.msi.com/Motherboard/MAG-B760-TOMAHAWK-WIFI-DDR4/support#driver)

    **Miscellaneous**<br>
    [Windows® 10 and Windows 11* Wi-Fi Drivers for Intel® Wireless Adapters (version 22.200.0)](https://www.intel.com/content/www/us/en/download/19351/windows-10-and-windows-11-wi-fi-drivers-for-intel-wireless-adapters.html)<br>
    [Intel® Wireless Bluetooth® for Windows® 10 and Windows 11*  (version 22.200.0)](https://www.intel.com/content/www/us/en/download/18649/intel-wireless-bluetooth-for-windows-10-and-windows-11.html)<br>
    [Intel Chipset Driver 600/700 (version 10.1.19199.8340)](https://tw.msi.com/Motherboard/MAG-B660-TOMAHAWK-WIFI-DDR4/support#driver)<br>
    [AMD Chipset Drivers (version 5.02.19.2221)](https://www.amd.com/en/support/chipsets/amd-socket-am4/b550)

## Install Option For Common Driver
[driver install flag](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/tree/main/docs/driver%20install%20flag)

## Install Setting
1. Auto<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226850047-1d67eebd-2a97-414f-a44a-e7aa05f6980c.png)<br>
    All the selected drivers will be installed automatically in the background. No interaction required.
2. Retry<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226852116-544d01ce-919d-4a37-b463-e33ceaa60a82.png)<br>
    Fallback to manaul install if driver(s) installation failed in auto installation mode.
3. Parallel<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226852351-3e44838b-ad04-48fb-b786-5bff2736daa0.png)<br>
    By default, auto installation mode is *blocking* (i.e. executing one after the other finished).<br>
    This option make it to be *asynchronous* (i.e executing all at once), but this may cause installation failure.
4. Auto Shutdown<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226853670-8ce5c33e-b84c-4284-a466-d0ea7ddc718a.png)<br>
    After **ALL** drivers are installed successfully **using auto installation**, do the respected action.
    
## Driver Management
`管理 -> 編輯軀動程式`

![dri_conf_window](https://user-images.githubusercontent.com/71750702/226865796-6f39f684-18fb-4302-a7f3-c44fb9ac0c46.png)

Yellow backgroud means the driver cannot be installed using auto installation mode [(customizable)](#autoable-descr)

- double click a row to edit the driver setting
- click `新增` to create a new driver installation option

![dri_edit_window_new](https://user-images.githubusercontent.com/71750702/226859055-33cb78ed-ca79-4361-8be9-00fa35d8b2db.png)
![dri_edit_window_old](https://user-images.githubusercontent.com/71750702/226878600-0051f092-97b1-468c-adb3-2bc856253b7b.png)


1. Driver Category<br>
    Only `miscellaneous` is muliple choice<br>
    `display`, `metwork` are single choice, which means only 1 driver from those category can be selected and installed.
2. Executable Path<br>
    The path to the driver installer/executable (e.g. `setup.exe`, `xxxx.exe`)
    > driver\display\nvidia 531.29 WHQL\setup.exe
    >
    > driver\network\intel 26.2.0.1\APPS\SETUP\SETUPBD\Winx64\SetupBD.exe

    When creating a new driver installation option, you should first copy the driver file/executable to `driver/<category>/` in the program folder for easy management and transfer (e.g. copy the program, setting to a USB)
3. Installation Option<br>
    Used to tell the driver to use "unattended", "silent" mode, and apply additional setting to install. (for auto installation mode)
    
    ![flag_preset](https://user-images.githubusercontent.com/71750702/226869519-0a1b2680-791b-473a-928f-726925fc0df1.png)
    
    Install option preset has been provide for common drivers<br>
    If you need to enter manually, please follow the format `<1>,<2>,...` (seperate by comma)
    > -s,-norestart
    
    For driver options that is not included with the preset, you may try to search with `driver name` + `silent`／`unattended`／`command line install`
    > realtek audio silent install
    
    or DIY using [Silent Install Builder](https://www.silentinstall.org/)
4. <a name="autoable-descr">Autoable</a><br>
    Check this option if the driver can be installed using [slient installation](https://www.makeuseof.com/windows-silent-installation-explained/).<br>
    In most cases, you should have supplied the `install option`, then check this option. Otherwise, don't check. 
    
    Incorrect setting will cause the "un-autoable" driver being executed with normal/attended installation (require you to interact with the installation prompt/dialog), which may lead to unexpected shutdown (depends) even if the installation is not finished.
    
