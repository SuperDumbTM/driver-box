# OneClick-Drivers-Installer

[![en](https://img.shields.io/badge/README-en-green.svg)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/blob/main/docs/README-en.md)
[![zh-hk](https://img.shields.io/badge/README-zh--hk-yellow.svg)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/blob/main/docs/README-zh_hk.md)
![zh-tw](https://img.shields.io/badge/README-zh--tw-inactive.svg)

一鍵安裝電腦所需的基本軀動程式

- [OneClick-Drivers-Installer](#oneclick-drivers-installer)
  - [下載](#下載)
  - [常用軀動安裝參數參考](#常用軀動安裝參數參考)
  - [安裝選項](#安裝選項)
  - [修改及更新軀動](#修改及更新軀動)

![main_window](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/assets/71750702/7af647cd-2ea1-4124-b74a-038a9397a8d3)

![progress_window](https://user-images.githubusercontent.com/71750702/226849659-71b77b32-eefb-4649-9865-74050818e249.png)

## 下載
主程式<br>
[![version](https://img.shields.io/badge/version-0.5.3-blue)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/releases/tag/v0.5.3)

軀動包<br>
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

## 常用軀動安裝參數參考
[driver install flag](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/tree/main/docs/driver%20install%20flag)

## 安裝選項
1. 自動安裝<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226850047-1d67eebd-2a97-414f-a44a-e7aa05f6980c.png)<br>
    軀動程式會在背景自動安裝，用戶毋須與軀動程式安裝程序互動
2. 失敗重試<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226852116-544d01ce-919d-4a37-b463-e33ceaa60a82.png)<br>
    當有軀動程式在自動安裝模式下安裝失敗，以手動模式重試
3. 同步安裝<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226852351-3e44838b-ad04-48fb-b786-5bff2736daa0.png)<br>
    自動安裝模式預設是以 *一個接一個（blocking）* 的方式執行安裝程序。
    此選項更改安裝方式成 *同時執行（asynchronous）* 所有安裝程序
4. 自動關機<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226853670-8ce5c33e-b84c-4284-a466-d0ea7ddc718a.png)<br>
    在**自動安裝模式**下及**成功安裝所有**軀動程式時，執行選項的相應動作
    
## 修改及更新軀動
`管理 -> 編輯軀動程式`

![dri_conf_window](https://user-images.githubusercontent.com/71750702/226865796-6f39f684-18fb-4302-a7f3-c44fb9ac0c46.png)

黃色背景代表該軀動程式不能以自動模式安裝[（用戶自訂）](#autoable-descr)
- 雙擊目標行（row）以編輯軀動程式
- 按 `新增` 以新增軀動程式

![dri_edit_window_new](https://user-images.githubusercontent.com/71750702/226859055-33cb78ed-ca79-4361-8be9-00fa35d8b2db.png)
![dri_edit_window_old](https://user-images.githubusercontent.com/71750702/226878600-0051f092-97b1-468c-adb3-2bc856253b7b.png)


1. 軀動分類<br>
    只有 `miscellaneous` 分類是「多選」<br>
    `display`, `network` 是單選，每次安裝只能從分類中選擇其中一個軀動來安裝。
2. 軀動路徑<br>
    軀動程式的安裝程序執行檔（例如 `setup.exe`, `xxxx.exe`）
    > driver\display\nvidia 531.29 WHQL\setup.exe
    >
    > driver\network\intel 26.2.0.1\APPS\SETUP\SETUPBD\Winx64\SetupBD.exe

    在新增軀動程式時，建議先將軀動程式的檔案（執行檔 `.exe` 或資料夾）複製到程式 `driver/<分類>/` 資料夾內，以便管理及轉移（例如複製程式、設定至 USB）<br>
3. 安裝參數<br>
    用作指示軀動程式以「unattended」、「silent」模式安裝（用於自動安裝模式），及任何安裝設定。
    
    ![flag_preset](https://user-images.githubusercontent.com/71750702/226869519-0a1b2680-791b-473a-928f-726925fc0df1.png)
    
    程式已提供常見軀動的安裝參數。<br>
    如自行輸入，須以 `<1>,<2>,...` 格式輸入（以逗號分隔）。
    > -s,-norestart
    
    不在預設集上的軀動可嘗試在網上以 `軀動名稱` + `silent`／`unattended`／`command line install` 搜尋
    > realtek audio silent install
    
    或利用 [Silent Install Builder](https://www.silentinstall.org/) 自行製作
4. <a name="autoable-descr">可自動安裝</a><br>
    勾選如軀動支援 [silent install](https://www.makeuseof.com/windows-silent-installation-explained/)。
    
    錯誤選擇會導致 *不能被自動安裝的軀動* 以手動模式的方式被執行（需要用戶在安裝介面操作），即使該軀動該未完成安裝，亦會被視作成功安裝，繼而自動關機（如適用）