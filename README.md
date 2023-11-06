# OneClick-Drivers-Installer

[![en](https://img.shields.io/badge/README-en-green.svg)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/blob/main/docs/README-en.md)
[![zh-hk](https://img.shields.io/badge/README-zh--hk-yellow.svg)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/blob/main/docs/README-zh_hk.md)
![zh-tw](https://img.shields.io/badge/README-zh--tw-inactive.svg)

一鍵安裝電腦所需的基本軀動程式

- [OneClick-Drivers-Installer](#oneclick-drivers-installer)
  - [下載](#下載)
  - [安裝選項](#安裝選項)
  - [編輯軀動程式](#編輯軀動程式)

![main_window](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/assets/71750702/ec78e2e8-3f7c-4897-a409-99bd9a11f019)
![progress_window](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/assets/71750702/66e3a520-fc3c-4d07-80c7-88861cf9639f)


## 下載
主程式<br>
[![version](https://img.shields.io/badge/version-0.7.0-blue)](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/releases/tag/v0.7.0)

常用軀動程式集<br>
[Google Drive](https://drive.google.com/drive/folders/1VqND0o75oBR80Ft2IK8WjTTbXaezmajw?usp=sharing)

常用軀動安裝參數參考<br>
[Flags/options reference](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/tree/main/docs/driver%20install%20flag)

## 安裝選項

### 執行設定
| **選項**   | **意思**                                                                        |
|----------|-------------------------------------------------------------------------------|
| **自動安裝** | 軀動程式會在背景自動安裝，用戶毋須與安裝程序互動                                                      |
| **失敗重試** | 自動安裝失敗時，以手動模式重試                                                          |
| **同步安裝** | 自動安裝模式預設是以 _一個接一個（blocking）_ 的方式執行安裝程序。<br> 此選項更改安裝方式成 _同時執行（asynchronous）_ 所有安裝程序 |


### 關機選項
_只適用於自動安裝模，並且所有已選軀動程式都支援自動安裝_
    
## 編輯軀動程式
`管理 -> 編輯軀動程式`

![dri_conf_window](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/assets/71750702/48275781-7b4d-4429-825e-c400dc8ef6fb)

| **背景顏色** | **意思**    |
|----------|-----------|
| **紅色**   | 路徑不存在     |
| **黃色**   | 不能以自動模式安裝[（用戶自訂）](#autoable-descr) |

- 雙擊目標行（row）以編輯軀動程式
- 按 `新增` 以新增軀動程式

![dri_edit_window_new](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/assets/71750702/027d1683-dabf-4796-97e6-54abd81997fd)
![dri_edit_window_old](https://github.com/SuperDumbTM/OneClick-Drivers-Installer/assets/71750702/e3b289eb-8212-4f44-9d1f-d460fb3dc1cc)


1. 軀動分類<br>
    只有 `miscellaneous` 分類是「多選」<br>
    `display`, `network` 是單選。每次安裝只能從分類中選擇安裝其中一個軀動程式。
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
    
    或利用 [Silent Install Builder](https://www.silentinstall.org/) 等類似的軟件自行製作
4. <a name="autoable-descr">可自動安裝</a><br>
    勾選如軀動支援 [silent install](https://www.makeuseof.com/windows-silent-installation-explained/)。
    
    錯誤選擇會導致 *不能被自動安裝的軀動* 沒有以 _silent install_ 的方式執行（需要用戶在安裝介面操作），即使該軀動該未完成安裝，亦 **可能** 會被視作成功安裝。
