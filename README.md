# OnClick-Drivers-Installer

Easy to use driver installer<br>
一鍵安裝電腦所需的基本軀動程式

![main_window](https://user-images.githubusercontent.com/71750702/226848983-19594222-11b6-4e89-8b8b-2a10ca2cbda6.png)

![progress_window](https://user-images.githubusercontent.com/71750702/226849659-71b77b32-eefb-4649-9865-74050818e249.png)


## 安裝選項
1. 自動安裝<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226850047-1d67eebd-2a97-414f-a44a-e7aa05f6980c.png)<br>
    軀動程式會在背景自動安裝，用戶毋須與軀動程式安裝程序互動
2. 失敗重試<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226852116-544d01ce-919d-4a37-b463-e33ceaa60a82.png)<br>
    當有軀動程式在自動安裝模式下安裝失敗，以手動模式重試
3. 同步安裝<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226852351-3e44838b-ad04-48fb-b786-5bff2736daa0.png)<br>
    自動安裝模式預設是一個接一個的方式執行安裝程序（blocking）。
    此選項更改安裝方式成一次過執行所有安裝程序（asynchronous）
4. 自動關機<br>
    ![圖片](https://user-images.githubusercontent.com/71750702/226853670-8ce5c33e-b84c-4284-a466-d0ea7ddc718a.png)<br>
    在**自動安裝模式**下及**成功安裝所有**軀動程式時，執行選項的相應動作
    
## 修改／更新軀動
`管理 -> 編輯軀動程式`

![dri_conf_window](https://user-images.githubusercontent.com/71750702/226855062-e058efcd-a338-4a4a-8a34-46d49af5fbfe.png)

- 雙擊目標行（row）以編輯軀動程式
- 按 `新增` 以新增軀動程式

![dri_edit_window](https://user-images.githubusercontent.com/71750702/226859055-33cb78ed-ca79-4361-8be9-00fa35d8b2db.png)

1. 軀動分類<br>
    只有 `miscellaneous` 分類為「多選」<br>
    `display`, `network` 為單選，每次安裝只能從分類中選擇其中一個安裝。
2. 軀動路徑<br>
    選取軀動程式的安裝程式執行當（例如 `setup.exe`）

    在新增軀動程式時，建議先將軀動程式的檔案（執行檔 `.exe` 或資料夾）複製到程式 `driver/<分類>/` 資料夾內，以便管理及轉移（例如 USB）<br>
