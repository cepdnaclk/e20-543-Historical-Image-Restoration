import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        
        #setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.title('Image Historation')
        self.minsize(800,500)
        
        # Center the window
        width,height = 1000,600
        screen_width = self.winfo_screenwidth()  
        screen_height = self.winfo_screenheight()  
        x_coordinate = int((screen_width - width) / 2) 
        y_coordinate = int((screen_height - height) / 2)  
        self.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}") 
        
        #layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)
        
        #widgets
        self.image_import=ImageImport(self,self.import_image)
        
        #run
        self.mainloop()
        
    
    def import_image(self,path):
        self.image = Image.open(path)
        # self.image=self.original
        self.image_ratio = self.image.size[0]/self.image.size[1]
        self.image_tk=ImageTk.PhotoImage(self.image)

        self.image_import.grid_forget()
        self.image_output=ImageOutput(self,self.resize_image)
        self.close_button=CloseOutput(self,self.close_edit)
        # self.menu=Menu(self,self.pos_vars,self.color_vars,self.effect_vars,self.export_image)
    
    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        # self.menu.grid_forget()
        self.image_import=ImageImport(self,self.import_image)
    
    def resize_image(self,event):
        # #current canvas ratio
        canvas_ratio=event.width/event.height

        #update canvas attributes
        self.canvas_width=event.width
        self.canvas_height=event.height

        # resize image
        if canvas_ratio>self.image_ratio:
            self.image_height=int(event.height)
            self.image_width=int(self.image_height*self.image_ratio)

        else:
            self.image_width=int(event.width)
            self.image_height=int(self.image_width/self.image_ratio)

        self.place_image()
    
    def place_image(self):
        self.image_output.delete('all')
        resized_image=self.image.resize((self.image_width,self.image_height))  
        self.image_tk=ImageTk.PhotoImage(resized_image) 
        self.image_output.create_image(self.canvas_width/2,self.canvas_height/2,image=self.image_tk)
    
App()