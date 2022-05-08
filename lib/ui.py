import sys_info
import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as tkscrolled
import ui_element as elm
import config as cfg
import driver as dri

class UI:
    
    def __init__(self, master: tk.Tk) -> None:
        self.w = master
        self.elm = elm.UIElement()
        self.hwinfo = sys_info.HwInfo.get_instance()
        
        self.w.geometry("550x550")
        self.sel_wdg_w = 22
        self.sel_wdg_h = 10
        self.bgc = "SystemButtonFace" # background color
        self.w.title("OneClick Drivers Installer")
        self.w.iconbitmap(cfg.PICDIR + "\icon.ico")
        
    
    def init_hwinfo(self) -> None:
        heading = tk.Label(self.w, text="電腦硬件配置：")
        heading.grid(column=0, row=0, sticky="w")
        
        font_title = tkFont.Font(family="Arial Narrow", size=10, weight="bold")
        font_content = tkFont.Font(family="Courier New", size=10)
        
        widget = tkscrolled.ScrolledText()

        font_title = tkFont.Font(family="Arial Narrow", size=10, weight="bold")
        font_content = tkFont.Font(family="Courier New", size=10)
        widget.configure(font=font_content, cursor="arrow")

        # MB
        lb = tk.Label(widget, text="底版 MOTHERBOARD")
        widget.window_create("end", window=lb)
        widget.insert("end", "\n")
        
        widget.insert(tk.INSERT, "\t"+self.hwinfo.get_mb_descr()[0]+"\n")
        
        # CPU
        lb = tk.Label(widget, text="中央處理器 CPU")
        widget.window_create("end", window=lb)
        widget.insert("end", "\n")
        for item in self.hwinfo.get_cpu_descr():
            widget.insert(tk.INSERT, "\t"+item+"\n")
        
        # RAM
        lb = tk.Label(widget, text="記憶體 RAM")
        widget.window_create("end", window=lb)
        widget.insert("end", "\n")
        for item in self.hwinfo.get_ram_descr():
            widget.insert(tk.INSERT, "\t"+item+"\n")
        
        # GPU
        lb = tk.Label(widget, text="顯示卡 GPU")
        widget.window_create("end", window=lb)
        widget.insert("end", "\n")
        for item in self.hwinfo.get_gpu_descr():
            widget.insert(tk.INSERT, "\t"+item+"\n")

        # NIC
        lb = tk.Label(widget, text="網絡介面卡 NIC")
        widget.window_create("end", window=lb)
        widget.insert("end", "\n")
        for item in self.hwinfo.get_nic_descr():
            widget.insert(tk.INSERT, "\t"+item+"\n")

        # DISK
        lb = tk.Label(widget, text="儲存裝置 STORAGE")
        widget.window_create("end", window=lb)
        widget.insert("end", "\n")
        for item in self.hwinfo.get_disk_descr():
            widget.insert(tk.INSERT, "\t"+item+"\n")

        widget.config(state="disable") # disable txt input
        widget.configure(width=self.sel_wdg_w*3, height=20, font=font_content, bd=0)
        
        for elm in widget.children:
            widget.children[elm].configure(bg="white", font=font_title)
                   
        widget.grid(column=0, row=1, columnspan=4)
        
    def init_dri_sel(self, instances: dict[str, dri.Driver], variable: dict[str, dict[str, tk.Variable]]):
        
        h = tk.Label(self.w, text="有線網絡介面卡")
        h.grid(column=0, row=2)
        widget = self.elm.dri_rb(instances['lan'], variable['lan']["lan"])
        widget.configure(width=self.sel_wdg_w, height=self.sel_wdg_h, background=self.bgc, relief="groove")
        widget.grid(column=0, row=3)
        
        h = tk.Label(self.w, text="顯示卡")
        h.grid(column=1, row=2)
        widget = self.elm.dri_rb(instances['display'], variable['display']["display"])
        widget.configure(width=self.sel_wdg_w, height=self.sel_wdg_h, background=self.bgc, relief="groove")
        widget.grid(column=1, row=3)
        
        h = tk.Label(self.w, text="其他")
        h.grid(column=2, row=2)
        widget = self.elm.dri_cb(instances['other'], variable['other'])
        widget.configure(width=self.sel_wdg_w, height=self.sel_wdg_h, background=self.bgc, relief="groove")
        widget.grid(column=2, row=3)
        
    def init_setting(self, variable: dict[str, dict[str, tk.Variable]]):
        #widget.configure(width=self.sel_wdg_w, background=self.bgc, bd=0)
        row = 4
        for key, val in variable.items():
            cb = tk.Checkbutton(text=val['descr'], variable=val['var'])
            cb.grid(column=0, row=row, sticky="w")
            row += 1
            
        
    def init_btn(self, variable: dict[str, ]):
        row = 4

        for key, val in variable.items():
            btn = tk.Button(text=val['descr'], command=val['cmd'], bg="burlywood3", relief='groove', borderwidth=2)
            btn.grid(column=1, row=row, sticky="we")
            row += 1

    def init_toplevel(self, master) -> tk.Toplevel:
        top = tk.Toplevel(master)
        top.title("安裝狀態")
        top.minsize(300,150)
        top.iconbitmap(cfg.PICDIR + "\install.ico")
        return top
    
    def init_status(self, toplv, item):
        row = 1
        
        for key, val in item.items():
            lb = tk.Label(toplv,text=key)
            lb.grid(column=0, row=row)
            tk.Label(toplv, textvariable=val).grid(column=1, row=row, sticky='we')
            row +=1
        toplv.columnconfigure(0, minsize=100)
        toplv.columnconfigure(1, minsize=150)
                  
        
        
if __name__ == "__main__":
    ui = UI(tk.Tk())
    
    dri_instance = {
        'lan': dri.LanDriver(),
        'display': dri.DisplayDriver(),
        'other': dri.OtherDriver()
    }
    varible = {
        'lan': {'lan': tk.StringVar(value="none")},
        'display': {'display': tk.StringVar(value="none")},
        'other': {
            "wifi": tk.BooleanVar(value=False),
            "bluetooth": tk.BooleanVar(value=False),
            "intel_chipset": tk.BooleanVar(value=False),
            "amd_chipset": tk.BooleanVar(value=False)
        }
    }
    setting = {
        'at_halt': {'descr':"自動關機", 'var':tk.BooleanVar(value=False)},
        'at_inst': {'descr':"自動安裝", 'var':tk.BooleanVar(value=False)}
    }
    btn = {
        "exec": {'descr':"執行", 'cmd':print}
    }
    
    ui.init_hwinfo()
    ui.init_dri_sel(dri_instance, varible)
    ui.init_setting(setting)
    ui.init_btn(btn)
    ui.w.mainloop()
    
        