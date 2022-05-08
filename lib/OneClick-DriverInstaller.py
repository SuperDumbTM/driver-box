import subprocess
import threading
import time
import ui
import driver as dri
import tkinter as tk
from tkinter import messagebox

class App:
    
    dri_instance: dict[str, dri.Driver]

    
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.ui = ui.UI(self.window)
        self.ui_stat = self.ui.init_toplevel(self.window)
        self.ui_stat.protocol("WM_DELETE_WINDOW", self.window.destroy) # kill master when close toplevel
        self.ui_stat.withdraw() # hide toplevel
        
        
        self.variable_setup()
        self.ui.init_hwinfo()
        self.ui.init_dri_sel(self.dri_instance, self.varible)
        self.ui.init_setting(self.setting)
        self.ui.init_btn(self.btn)
        self.window.mainloop()
    
    def variable_setup(self):
        self.dri_instance = {
            'lan': dri.LanDriver(),
            'display': dri.DisplayDriver(),
            'other': dri.OtherDriver()
        }

        self.varible = {
            'lan': {'lan': tk.StringVar(value="none")},
            'display': {'display': tk.StringVar(value="none")},
            'other': {key:tk.BooleanVar(value=False) for key in self.dri_instance['other'].get_dri_conf().keys()}
        }
        
        self.status = {
            'lan': tk.StringVar(value="----"),
            'display': tk.StringVar(value="----")
        }
        self.status.update({key:tk.StringVar(value="----") for key in self.dri_instance['other'].get_dri_conf().keys()})
        
        self.setting = {
            'at_halt': {'descr':"自動關機", 'var':tk.BooleanVar(value=False)},
            'at_inst': {'descr':"自動安裝", 'var':tk.BooleanVar(value=True)} # pre-select
        }

        self.btn = {
            "disk_mgt": {'descr':"開啟磁碟管理員", 'cmd':self.open_diskmgt},
            "exec": {'descr':"執行", 'cmd':self.install}
        }

    def open_diskmgt(self):
        subprocess.run("start diskmgmt.msc", shell=True)

    def install(self):
        self.ui.init_status(self.ui_stat, self.status)
        self.window.withdraw()
        self.ui_stat.deiconify()
        
        if self.setting['at_inst']['var'].get():
            self.__auto_install()
        else:
            self.__manual_install()
        
    
    def __manual_install(self):
        for key, val in self.varible.items(): # key: driver type, var: dict(input from user)
            for _key, _var in val.items(): # _key: driver name, _var: variable
                # ----- checkbox (boolean) -----
                if _var.get() == True:
                    self.dri_instance[key].manual_install(_key, self.status[_key])
                    self.status[_key].set("已開啟安裝程式")
                # ----- radiobutton (string) -----
                elif type(_var.get()) is str and _var.get() != "none":
                    self.dri_instance[key].manual_install(_var.get(), self.status[_key])
                    self.status[_key].set("已開啟安裝程式")

    def __auto_install(self):
        for key, val in self.varible.items(): # key: driver type, var: dict(input from user)
            for _key, _var in val.items(): # _key: driver name, _var: variable
                # ----- checkbox (boolean) -----
                if _var.get() == True:
                    self.dri_instance[key].auto_install(_key, self.status[_key])
                    self.status[_key].set("等待安裝中")
                # ----- radiobutton (string) -----
                elif type(_var.get()) is str and _var.get() != "none":
                    self.dri_instance[key].auto_install(_var.get(), self.status[_key])
                    self.status[_key].set("等待安裝中")
        # --------------- auto install routine ---------------
        dri.Driver.start_install()
        
        while not dri.Driver.is_finished():
            self.ui_stat.update()
            time.sleep(0.1)
            
        if not dri.Driver.has_error() and self.setting['at_halt']['var'].get():
            t = threading.Timer(5, self.halt)
            t.start()
            messagebox.showinfo(title="Success", message="安裝成功，即將自動關機")
        elif dri.Driver.has_error():
            messagebox.showerror(title="Failed", message="一個或多個軀動程式安裝失敗\n將以手動安裝模式重試")
            # fallback to manual install
            dri.Driver.reinstall_failed()
        else:
            messagebox.showinfo(title="Finished", message="完成")
            exit(0)
    
    def halt(self):
            subprocess.run(["shutdown", "/s", "/t", "1"])
        

if __name__ == "__main__":
    app = App()