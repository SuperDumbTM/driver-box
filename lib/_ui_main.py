import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled
import tkinter.font as tkFont
import config
import sys_info
import _ui_install
import threading
import subprocess

# compile:
# pyinstaller -F -w --uac-admin -r main.exe.manifest,1 main.py
# pyinstaller -F -w --uac-admin lib/ui_main.py --icon=pic/icon.ico

class MainUI:
    
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.iconbitmap("pic/icon.ico")
        self.conf = config.Conf.get_instance()
        self.sinfo = sys_info.HwInfo.get_instance()
        self.attr_assign()

        self.__hw_info()
        self.__lan()
        self.__display()
        self.__wireless()
        self.__button()
        self.window.mainloop()

    def attr_assign(self):
        attrs = self.conf.get_app_conf()

        #self.window.title("OneClick Drivers Installer")
        self.window.title(attrs["prog_title"])
        self.window.geometry(attrs["resolution"])
        self.window.resizable(True,True)

        self.txtb_color = attrs["txtb_color"]
        self.driver_sel_height = attrs["driver_sel_height"]
        self.col_width = attrs["col_width"]
        self.dri_sel_txtwrap = attrs["dri_sel_txtwrap"]
        self.halt_time = float(attrs['halt_time'])
    
    def __hw_info(self):
        font_title = tkFont.Font(family="Arial Narrow", size=10)

        title_hwinfo = tk.Label(self.window, text="電腦硬件配置：")
        title_hwinfo.grid(column=0, row=0, sticky="w")

        info_container = tkscrolled.ScrolledText(self.window, height=20, width=self.col_width*3, cursor="arrow", background=self.txtb_color, bd=0, wrap="word")
        info_container.grid(column=0, row=1, columnspan=3, sticky="w")

        # CPU
        lb = tk.Label(info_container, text="中央處理器 CPU", font=font_title)
        info_container.window_create("end", window=lb)
        info_container.insert("end", "\n")
        for item in self.sinfo.get_cpu_info():
            info_container.insert(tk.INSERT, "\t"+item+"\n")
        
        # RAM
        lb = tk.Label(info_container, text="記憶體 RAM", font=font_title)
        info_container.window_create("end", window=lb)
        info_container.insert("end", "\n")
        for item in self.sinfo.get_ram_info():
            info_container.insert(tk.INSERT, "\t"+item+"\n")
        
        # MB
        lb = tk.Label(info_container, text="底版 MB", font=font_title)
        info_container.window_create("end", window=lb)
        info_container.insert("end", "\n")
        info_container.insert(tk.INSERT, "\t"+self.sinfo.get_mb_info()[0]+"\n")
        
        # GPU
        lb = tk.Label(info_container, text="顯示卡 GPU", font=font_title)
        info_container.window_create("end", window=lb)
        info_container.insert("end", "\n")
        for item in self.sinfo.get_gpu_info():
            info_container.insert(tk.INSERT, "\t"+item+"\n")

        # NIC
        lb = tk.Label(info_container, text="網絡介面卡 NIC", font=font_title)
        info_container.window_create("end", window=lb)
        info_container.insert("end", "\n")
        for item in self.sinfo.get_nic_info():
            info_container.insert(tk.INSERT, "\t"+item+"\n")

        # DISK
        lb = tk.Label(info_container, text="儲存裝置 STORAGE", font=font_title)
        info_container.window_create("end", window=lb)
        info_container.insert("end", "\n")
        for item in self.sinfo.get_disk_info():
            info_container.insert(tk.INSERT, "\t"+item+"\n")


        info_container.config(state="disable") # disable txt input 
        
    def __lan(self):
        self.lan_btns = []

        title_lan = tk.Label(self.window, text="有線網絡介面卡")
        title_lan.grid(column=0, row=2)
        self.lan_btn_container = tkscrolled.ScrolledText(self.window, height=self.driver_sel_height, width=self.col_width, cursor="arrow", background=self.txtb_color, bd=0)
        self.lan_btn_container.grid(column=0, row=3)

        self.input_lan = tk.StringVar(value="none")
        
        for choice in self.conf.get_lan_conf():
            rb = tk.Radiobutton(self.lan_btn_container, text=choice['text'], variable=self.input_lan, value=choice['iden'], background=self.txtb_color)
            self.lan_btns.append(rb)
            self.lan_btn_container.window_create("end", window=rb)
            self.lan_btn_container.insert("end", "\n") 
        
        self.lan_btn_container.config(state="disable") # disable txt input  
    
    def __display(self):
        self.display_btns = []

        title_display = tk.Label(self.window, text="顯示卡")
        title_display.grid(column=1, row=2)
        self.display_btn_container = tkscrolled.ScrolledText(self.window, height=self.driver_sel_height, width=self.col_width, cursor="arrow", background=self.txtb_color, bd=0)
        self.display_btn_container.grid(column=1, row=3)

        self.input_display = tk.StringVar(value="none")

        for choice in self.conf.get_display_conf():
            rb = tk.Radiobutton(self.display_btn_container, text=choice['text'], variable=self.input_display, value=choice['iden'], background=self.txtb_color)
            self.display_btns.append(rb)
            self.display_btn_container.window_create("end", window=rb)
            self.display_btn_container.insert("end", "\n") 
        
        self.display_btn_container.config(state="disable") # disable txt input  
    
    def __wireless(self):
        self.input_wireless = {}

        title_wireless = tk.Label(self.window, text="WiFi卡")
        title_wireless.grid(column=2, row=2)
        self.wireless_btn_container = tkscrolled.ScrolledText(self.window, height=self.driver_sel_height, width=self.col_width, cursor="arrow", background=self.txtb_color, bd=0)
        self.wireless_btn_container.grid(column=2, row=3)

        for choice in self.conf.get_wireless_conf():
            input_wireless = tk.BooleanVar(value=False) # local var for store diff chk val

            cb = tk.Checkbutton(self.wireless_btn_container, text=choice['text'], variable=input_wireless, background=self.txtb_color)
            self.input_wireless[choice['iden']] = input_wireless
            self.wireless_btn_container.window_create("end", window=cb)
            self.wireless_btn_container.insert("end", "\n") 

        self.wireless_btn_container.config(state="disable") # disable txt input 
    
    def other(self):
        pass
   
    # row = 4
    def __button(self):
        self.input_at_halt = tk.BooleanVar(value=False)
        self.input_at_install = tk.BooleanVar(value=True)

        cb_auto_halt = tk.Checkbutton(self.window, text="自動關機", variable=self.input_at_halt)
        cb_auto_install = tk.Checkbutton(self.window, text="自動安裝", variable=self.input_at_install)
        cb_auto_halt.grid(column=0, row=4, sticky="w")
        cb_auto_install.grid(column=0, row=5, sticky="w")

        btn_install = tk.Button(self.window, text="安裝", command=self.install_ui_init_exec)
        btn_install.grid(column=1, row=5)

    def install_ui_init_exec(self):
        self.window.destroy()
        inst = _ui_install.InstallUI(
            lan = self.input_lan.get(),
            display = self.input_display.get(),
            wireless = self.input_wireless,
            at_install = self.input_at_install,
            at_halt = self.input_at_halt
        )
        err = inst.start()
        
        def halt():
            subprocess.run(["shutdown", "/s", "/t", "1"])
            
        if not err and (self.input_at_halt.get() and self.input_at_install.get()):
            t = threading.Timer(self.halt_time, halt)
            t.start()
            messagebox.showinfo(title="Success", message="安裝成功，"+str(int(self.halt_time))+"秒後將自動關機")
        elif err:
            messagebox.showwarning(title="Failed", message="一個或多個軀動程式安裝失敗")
        

u = MainUI()