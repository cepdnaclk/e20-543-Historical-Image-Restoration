import customtkinter as ctk
from tkinter import filedialog
from settings import *

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack(fill='x',pady=4, ipady =8)

class SliderPanel(Panel):
    def __init__(self, parent, text,data_var,min_value,max_value):
        super().__init__(parent=parent)

        self.data_var=data_var
        self.data_var.trace('w',self.update_text)
        
        #layout
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)
        
        ctk.CTkLabel(self,text=text).grid(row=0,column=0,sticky='W',padx=9)
        self.num_label=ctk.CTkLabel(self,text=data_var.get())
        self.num_label.grid(row=0,column=1,sticky='E',padx=9)

        ctk.CTkSlider(self,
                      fg_color=SLIDER_BG,
                      variable=self.data_var,
                      from_=min_value,
                      to=max_value).grid(row=1,column=0,columnspan=2,sticky='ew',padx=9,pady=5) 
        
    def update_text(self,*args):
        self.num_label.configure(text=f'{round(self.data_var.get(),2)}')
    
class RevertButton(ctk.CTkButton):
    def __init__(self,parent,*args):
        super().__init__(master=parent,text='Revert',command=self.revert)
        self.pack(side='bottom',pady=10)
        self.args=args

    def revert(self):
        for var,value in self.args:
            var.set(value)

class UndoButton(ctk.CTkButton):
    def __init__(self, parent, undo_action):
        super().__init__(master=parent, text='Undo', command=undo_action)
        self.pack(side='bottom',pady=10)
        
