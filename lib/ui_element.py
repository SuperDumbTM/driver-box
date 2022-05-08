import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkscrolled
import tkinter.font as tkFont
import sys_info
import driver

class UIElement:
    
    def __init__(self) -> None:
        self.hwinfo = sys_info.HwInfo.get_instance()
    
    # widget.configure(width = x)
    def dri_rb(self, dri: driver.Driver, _input: tk.StringVar) -> tkscrolled.ScrolledText:
        container = tkscrolled.ScrolledText(cursor="arrow")
        
        for key, dets in dri.get_conf().items():
            rb = tk.Radiobutton(container, text=dets['text'], variable=_input, value=key)
            container.window_create("end", window=rb)
            container.insert("end", "\n") 
        container.config(state="disable") # disable txt input
        
        return container
        
    def dri_cb(self, dri: driver.Driver,  _input: dict[str, tk.BooleanVar]) -> tkscrolled.ScrolledText:
        container = tkscrolled.ScrolledText( cursor="arrow")
        
        for key, dets in dri.get_conf().items():
            cb = tk.Checkbutton(container, text=dets['text'], variable=_input[key])
            container.window_create("end", window=cb)
            container.insert("end", "\n") 
        container.config(state="disable") # disable txt input
        
        return container
    
    def cb_box(self, _input: dict[str, ]) -> tkscrolled.ScrolledText:  
        container = tk.Label()
        for key, val in _input.items():
            cb = tk.Checkbutton(container, text=_input[key]['descr'], variable=_input[key]['var'])
            container.grid(column=0, row=4)
        
        return container
            
    
    # not in use
    def btn_area(self, _input: dict[str, ]) -> tkscrolled.ScrolledText:
        if master == None: master = self.master
        # container = tk.Frame(self.master)
        
        # bt = tk.Button(self.master, text="button")
        # bt.pack()
        # return(container)
        
        
if __name__ == "__main__":
    f = tk.Toplevel()
    f.geometry("300x300")
    u = UIElement()
    
    display = driver.DisplayDriver()
    #u.rb_dri_sel(display, tk.StringVar(value=False)).pack()
    u.btn_area(tk.StringVar(value="none")).pack()
    u.btn_area(tk.StringVar(value="none")).pack()
    f.mainloop()
    