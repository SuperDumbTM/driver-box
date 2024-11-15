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



<!-- TABLE OF CONTENTS -->
<details>
  <summary>目錄</summary>
  <ol>
    <li>
      <a href="#about-the-project">Project 簡介</a>
      <ul>
        <li><a href="#built-with">利用工具</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">開始使用</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Project 簡介

<p align="center">
  <img src="https://github.com/user-attachments/assets/93f63be9-7a42-4c6a-984c-f9f197913675" width="70%">
<p align="right">

此程式旨在加快安裝大量硬件軀動的時間。用家可以將不同類型的軀動程式加入到本程式中。
之後每次只需選擇合適的軀動程式即可。

<p align="right">(<a href="#readme-top">回到最頂</a>)</p>



### 第三方軟件使用

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

<img src="https://github.com/user-attachments/assets/14ab9d9c-1d68-4fde-9fb3-926ae21108b1" width="40%">

1. 軀動分類<br>
    只有 `miscellaneous` 分類是「多選」<br>
    `display`, `network` 是單選。每次安裝只能從分類中選擇安裝其中一個軀動程式。
2. 軀動路徑<br>
    軀動程式的安裝程序執行檔（例如 `setup.exe`, `xxxx.exe`）
    > driver\display\nvidia 531.29 WHQL\setup.exe
    >
    > driver\network\intel 26.2.0.1\APPS\SETUP\SETUPBD\Winx64\SetupBD.exe

    在新增軀動程式時，建議先將軀動程式的檔案（執行檔 `.exe` 或資料夾）複製到程式的 `drivers/<分類>/` 資料夾內，以便管理及轉移（例如複製程式、設定至 USB）<br>
3. 安裝參數<br>
    用作指示軀動程式以「unattended」、「silent」模式安裝，及任何安裝設定。
   
    <img src="https://github.com/user-attachments/assets/90160433-5982-4462-a1ca-bb042f45c460" width="30%">
    
    此程式已提供常見軀動的安裝參數。<br>
    如自行輸入，須以 `<1>,<2>,...` 格式輸入（以逗號分隔）。
    > -s,-norestart
    
    不在預設集上的軀動可嘗試在網上以 `軀動名稱` + `silent`／`unattended`／`command line install` 搜尋
    > realtek audio silent install
    
    或利用 [Silent Install Builder](https://www.silentinstall.org/) 等類似的軟件自行製作
4. 不能同時安裝<br>
    勺選後，在使用「同步安裝」模式時，有關的軀動程式將不會在同一時間執行。

### 安裝

1. 關機設定<br>
   關機設定只會在所以工作執行成功及軀動安裝成功後才會執行。


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
