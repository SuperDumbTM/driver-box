<a id="readme-top"></a>



<!-- PROJECT SHIELDS -->
<div align="center">
  
  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  
</div>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/SuperDumbTM/driver-box">
    <img src="https://github.com/user-attachments/assets/25624c0f-ce52-44f9-8345-68577f80b1f2" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">driver-box</h3>

  <p align="center">
    程式／軀動安裝工具
    <br />
    <br />
    <a href="https://github.com/SuperDumbTM/driver-box/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/SuperDumbTM/driver-box/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## Project 簡介

<p align="center">
  <img src="https://github.com/user-attachments/assets/93f63be9-7a42-4c6a-984c-f9f197913675" width="70%">
<p align="right">

此程式旨在加快安裝大量硬件軀動的時間。用家可以將不同類型的軀動程式加入到本程式中。
之後每次只需選擇合適的軀動程式即可。

<p align="right">(<a href="#readme-top">回到最頂</a>)</p>

### 第三方工具使用

* [<img src="https://img.shields.io/badge/bootstrap%20icons-7532fa?style=for-the-badge&logo=bootstrap&logoColor=white">](https://icons.getbootstrap.com/)
* [<img src="https://img.shields.io/badge/go-01add8?style=for-the-badge&logo=go&logoColor=white">](https://go.dev/)
* [<img src="https://img.shields.io/badge/tailwindcss-38bdf8?style=for-the-badge&logo=tailwindcss&logoColor=white">](https://tailwindcss.com/)
* [<img src="https://img.shields.io/badge/vue.js-41b883?style=for-the-badge&logo=vue.js&logoColor=white">](https://vuejs.org/)
* [<img src="https://img.shields.io/badge/wails-d32a2d?style=for-the-badge&logo=wails&logoColor=white">](https://wails.io/)

<p align="right">(<a href="#readme-top">回到最頂</a>)</p>



<!-- GETTING STARTED -->
## 開發

### 所需軟件

- Go https://go.dev/doc/install
- Node 22 https://nodejs.org/en/download/package-manager

### 安裝 Dependency

- Wails
  ```sh
  go install github.com/wailsapp/wails/v2/cmd/wails@latest
  ```
- NPM Dependencies
  ```sh
  cd ./frontend
  npm install
  ```

### 常用指令

- Debug run
  ```sh
  wails dev
  ```

- Build Executable
  ```sh
  wails build
  ```
  
<p align="right">(<a href="#readme-top">回到最頂</a>)</p>



<!-- USAGE EXAMPLES -->
## 使用

### 加入、編輯軀動程式

<img src="https://github.com/user-attachments/assets/0f1b8490-10a2-447e-a148-1af3e8f14c23" width="50%">

#### 軀動路徑
軀動程式的路徑。

> driver\display\nvidia 531.29 WHQL\setup.exe
>
> driver\network\intel 26.2.0.1\APPS\SETUP\SETUPBD\Winx64\SetupBD.exe

在新增軀動程式時，建議先將軀動程式的檔案（執行檔 `.exe` 或資料夾）複製到程式的 `drivers/<分類>/` 資料夾內，以便管理及轉移（例如複製程式到 USB 上）

#### 安裝參數
用作指示軀動程式以「unattended」、「silent」模式安裝，及任何安裝設定。

須以 `<1>,<2>,...` 格式輸入（以逗號分隔）。
> -s,-norestart

此程式已提供常見軀動的安裝參數。<br>
<img src="https://github.com/user-attachments/assets/90160433-5982-4462-a1ca-bb042f45c460" width="30%">

| 選項           	| 適用的程式                                                                                                                                                       	|
|----------------	|------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| Intel LAN      	| [Intel® Ethernet Adapter Complete Driver Pack](https://www.intel.com/content/www/us/en/download/15084/intel-ethernet-adapter-complete-driver-pack.html)          	|
| Realtek LAN    	| [Realtek PCIe FE / GBE / 2.5G / 5G Ethernet Family Controller Software](https://www.realtek.com/Download/List?cate_id=584)                                       	|
| Nvidia Display 	| [GeForce Game Ready Driver/Nvidia Studio Driver](https://www.nvidia.com/en-us/drivers/)                                                                          	|
| AMD Display    	| [AMD Software: Adrenalin Edition](https://www.amd.com/en/support/download/drivers.html)                                                                          	|
| Intel Display  	| [Intel® Arc™ & Iris® Xe Graphics/7th-10th Gen Processor Graphics](https://www.intel.com/content/www/us/en/support/articles/000090440/graphics.html)              	|
| Intel WiFi     	| [Intel® Wireless Wi-Fi Drivers](https://www.intel.com/content/www/us/en/download/19351/intel-wireless-wi-fi-drivers-for-windows-10-and-windows-11.html)          	|
| Intel BT       	| [Intel® Wireless Bluetooth® Drivers](https://www.intel.com/content/www/us/en/download/18649/intel-wireless-bluetooth-drivers-for-windows-10-and-windows-11.html) 	|
| Intel Chipset  	| [Chipset INF Utility](https://www.intel.com/content/www/us/en/support/products/1145/software/chipset-software/intel-chipset-software-installation-utility.html)  	|
| AMD Chipset    	| [AMD Chipset Drivers](https://www.amd.com/en/support/download/drivers.html)                                                                                      	|
    
不在預設集上的軀動可嘗試在網上以 `軀動名稱` + `silent`／`unattended`／`command line install` 搜尋
> realtek audio silent install
    
或利用 [Silent Install Builder](https://www.silentinstall.org/) 等類似的軟件自行製作

#### 不能同時安裝
勺選後，在使用「同步安裝」模式時，有關的軀動程式將不會在同一時間執行。

### 安裝

<img src="https://github.com/user-attachments/assets/f0d7cf67-42b0-42f3-a647-404d7b54e50a" width="50%">

<p style='color: gray'>*在所有工作執行完成前，執行狀態視窗不能夠被關閉。</p>

#### 關機設定
關機設定只會在所有工作執行成功及軀動安裝成功後才會執行。

#### 取消執行
只有處於「等待中」或「執行中」的工作才能取消執行。<br>
按下相關工作的「取消」按鈕即可。但注意，程式並不保證相關工作能夠被終止執行。

<p align="right">(<a href="#readme-top">回到最頂</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/SuperDumbTM/driver-box.svg?style=for-the-badge
[contributors-url]: https://github.com/SuperDumbTM/driver-box/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/SuperDumbTM/driver-box.svg?style=for-the-badge
[forks-url]: https://github.com/SuperDumbTM/driver-box/network/members
[stars-shield]: https://img.shields.io/github/stars/SuperDumbTM/driver-box.svg?style=for-the-badge
[stars-url]: https://github.com/SuperDumbTM/driver-box/stargazers
[issues-shield]: https://img.shields.io/github/issues/SuperDumbTM/driver-box.svg?style=for-the-badge
[issues-url]: https://github.com/SuperDumbTM/driver-box/issues
[license-shield]: https://img.shields.io/github/license/SuperDumbTM/driver-box.svg?style=for-the-badge
[license-url]: https://github.com/SuperDumbTM/driver-box/blob/master/LICENSE.txt
