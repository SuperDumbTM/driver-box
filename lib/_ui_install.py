from asyncio import subprocess
from sys import displayhook
import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled
import tkinter.font as tkFont
import config
import subprocess
from timeit import default_timer as timer

class InstallUI:

    def __init__(self, **kwarg) -> None:
        
        self.conf = config.Conf.get_instance()
        
        self.dri_lan = kwarg.get('lan')
        self.dri_display = kwarg.get('display')
        self.dri_wifi = kwarg.get('wireless').get('wifi').get()
        self.dri_bt = kwarg.get('wireless').get('bluetooth').get()
        self.atinst = kwarg.get('at_install', False).get()
        self.halt = kwarg.get('at_halt', False)
        self.has_error = False   
    
    def start(self) -> bool:
        self.__init_ui()
        self.__install()
        self.window.update()
        return self.has_error
        
        
    
    def __init_ui(self):
        self.window = tk.Tk()
        self.window.geometry("330x150")
        self.window.title("安裝狀態")
        self.window.iconbitmap("pic\\install.ico")
        self.window.columnconfigure(0, minsize=100)
        
        lb = tk.Label(self.window,text="Lan Driver")
        lb.grid(column=0, row=0, sticky="w")
        self.lan_stat = tk.StringVar()
        lb = tk.Label(self.window, textvariable=self.lan_stat)
        lb.grid(column=1, row=0, sticky="we")
        if self.dri_lan not in (None, "none"):
            self.lan_stat.set("等待安裝中...")
        else:
            self.lan_stat.set("----")
        
        lb = tk.Label(self.window,text="Display Driver")
        lb.grid(column=0, row=1, sticky="w")
        self.display_stat = tk.StringVar()
        lb = tk.Label(self.window, textvariable=self.display_stat)
        lb.grid(column=1, row=1, sticky="we")
        if self.dri_display not in (None, "none"):
            self.display_stat.set("等待安裝中...")
        else:
            self.display_stat.set("----")
        
        lb = tk.Label(self.window,text="WiFi Driver")
        lb.grid(column=0, row=2, sticky="w")
        self.wifi_stat = tk.StringVar()
        lb = tk.Label(self.window, textvariable=self.wifi_stat)
        lb.grid(column=1, row=2, sticky="we")
        if self.dri_wifi:
            self.wifi_stat.set("等待安裝中...")
        else:
            self.wifi_stat.set("----")
        
        lb = tk.Label(self.window,text="BT Driver")
        lb.grid(column=0, row=3, sticky="w")
        self.bt_stat = tk.StringVar()
        lb = tk.Label(self.window, textvariable=self.bt_stat)
        lb.grid(column=1, row=3, sticky="we")
        if self.dri_bt:
            self.bt_stat.set("等待安裝中...")
        else:
            self.bt_stat.set("----")
        
        self.window.update()
        
    def __install(self):
        if self.dri_lan not in (None, "none"):
            self.__install_lan(self.dri_lan)
        self.window.update()
        if self.dri_display not in (None, "none"):
            self.__install_display(self.dri_display)
        self.window.update()
        if self.dri_wifi:
            self.__install_wifi("wifi") 
        self.window.update()
        if self.dri_bt:
            self.__install_bt("bluetooth")
        self.window.update()
            
    def __install_lan(self, dri: str):
        try:
            self.lan_stat.set("安裝中...")
            self.window.update()
            detail = self.conf.find_lan_dri(dri)
            if self.atinst:
                p = subprocess.Popen([detail['path'], detail['flag']])
                start = timer()
                p.wait()
                end = timer()
                
                if not p.returncode == 0:
                    self.lan_stat.set("ERROR")
                    self.has_error = True
                elif end-start <= 5:
                    self.lan_stat.set("執行時間小於5秒，possible ERROR")
                    self.has_error = True
                else:
                    self.lan_stat.set("完成")
            else:
                subprocess.Popen([detail['path']])
                self.lan_stat.set("pass")
        except ValueError as e:
            self.lan_stat.set(e)
        
        
    
    def __install_display(self, dri: str):
        try:
            self.display_stat.set("安裝中...")
            self.window.update()
            print("display")
            detail = self.conf.find_display_dri(dri)
            if self.atinst:
                p = subprocess.Popen([detail['path'], *detail['flag'].split(",")])
                start = timer()
                p.wait()
                end = timer()
                
                if not p.returncode == 0:
                    self.display_stat.set("ERROR")
                    self.has_error = True
                elif end-start <= 5:
                    self.display_stat.set("執行時間小於5秒，possible ERROR")
                    self.has_error = True
                else:
                    self.display_stat.set("完成")
            else:
                subprocess.Popen([detail['path']])
                self.display_stat.set("pass")
        except ValueError as e:
            self.display_stat.set(e)
            
    def __install_wifi(self, dri: str):
        try:
            self.wifi_stat.set("安裝中...")
            self.window.update()
            detail = self.conf.find_wireless_dri(dri)
            if self.atinst:
                p = subprocess.Popen([detail['path'], detail['flag']])
                start = timer()
                p.wait()
                end = timer()
                
                if not p.returncode == 0:
                    self.wifi_stat.set("ERROR")
                    self.has_error = True
                elif end-start <= 5:
                    self.wifi_stat.set("執行時間小於5秒，possible ERROR")
                    self.has_error = True
                else:
                    self.wifi_stat.set("完成")
            else:
                subprocess.Popen([detail['path']])
                self.wifi_stat.set("pass")
        except ValueError as e:
            self.wifi_stat.set(e)
            
    def __install_bt(self, dri: str):
        try:
            self.bt_stat.set("安裝中...")
            self.window.update()
            detail = self.conf.find_wireless_dri(dri)
            if self.atinst:
                p = subprocess.Popen([detail['path'], detail['flag']])
                start = timer()
                p.wait()
                end = timer()
                
                if not p.returncode == 0:
                    self.bt_stat.set("ERROR")
                    self.has_error = True
                elif end-start <= 5:
                    self.bt_stat.set("執行時間小於5秒，possible ERROR")
                    self.has_error = True
                else:
                    self.bt_stat.set("完成")
            else:
                subprocess.Popen([detail['path']])
                self.bt_stat.set("pass")
        except ValueError as e:
            self.bt_stat.set(e)

if __name__ == "__main__":
    u = InstallUI()