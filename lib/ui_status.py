import tkinter as tk
import tkinter.font as tkFont
import tkinter.scrolledtext as tkscrolled
import ui_element as elm
import config as cfg
import driver as dri

class UI:
    
    def __init__(self) -> None:
        self.w = tk.Tk()
        self.w.geometry("330x150")
        self.w.title("安裝狀態")
        self.w.iconbitmap("pic\\install.ico")
        self.w.columnconfigure(0, minsize=100)
        
    def init(self, item: dict[str, tk.Variable]):
        output = {}
        
        row = 0
        for key, val in item.items():
            tk.Label(text=key).grid(column=0, row=row, sticky="w")
            tk.Label(textvariable=val).grid(column=1, row=row)
            row += 1
            
        self.w.mainloop()
        
if __name__ == "__main__":
    ui = UI()
    
    item = {
        'lan': tk.StringVar(value="----"),
        'display': tk.StringVar(value="----"),
        'other': tk.StringVar(value="----")
    }
    
    ui.init(item)