import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk
from menu import Menu
import numpy as np
import cv2
from tkinter import Canvas

class App(ctk.CTk):
    def __init__(self):
        
        #setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.title('Image Historation')
        self.minsize(800,500)
        self.init_parameters()
        
        # Center the window
        width,height = 1000,600
        screen_width = self.winfo_screenwidth()  
        screen_height = self.winfo_screenheight()  
        x_coordinate = int((screen_width - width) / 2) 
        y_coordinate = int((screen_height - height) / 2)  
        self.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}") 
        
        #layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2,uniform='a')
        self.columnconfigure(1, weight=6,uniform='a')
        
        #canvas data
        self.image_width=0
        self.image_height=0
        self.canvas_width=0
        self.canvas_height=0
        
        #widgets
        self.image_import=ImageImport(self,self.import_image)
        
        #run
        self.mainloop()
    
    
    def init_parameters(self):
        self.brush_settings={
            'size':ctk.IntVar(value=PENSIZE_DEFAULT),
            'color':ctk.StringVar(value=PENCOLOR_DEFAULT)
        }

        self.hsv_vars={
            'hue':ctk.DoubleVar(value=HUE_DEFAULT),
            'saturation':ctk.DoubleVar(value=SATURATION_DEFAULT),
            'value':ctk.DoubleVar(value=VALUE_DEFAULT)
        }

       
        # combined_vars=list(self.pos_vars.values())
        # #tracing
        # for var in combined_vars:
        #     var.trace('w',self.manipulate_image)
            
        for var in self.hsv_vars.values():
            var.trace('w',self.hsv_modified_image)
            
        for var in self.brush_settings.values():
            var.trace('w',self.paint_image)
            
    # def manipulate_image(self,*args):
    #     self.image=self.original

    #     #rotate
    #     if self.pos_vars['rotate'].get()!=ROTATE_DEFAULT:
    #         self.image=self.image.rotate(self.pos_vars['rotate'].get())
        
    #     self.place_image() 
    
    def paint_image(self,*args):
        self.image=self.original
        
        print(self.brush_settings['size'].get())
        print(self.brush_settings['color'].get())
    
    def hsv_modified_image(self,*args):
        self.image=self.original
        
        # Convert PIL image to a numpy array for HSV manipulation
        np_image = np.array(self.image.convert('RGB'))
        
        # Convert RGB to HSV
        hsv_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2HSV)
        
        # Retrieve HSV values from sliders
        h, s, v = (int(self.hsv_vars['hue'].get()),
                   int(self.hsv_vars['saturation'].get()),
                   int(self.hsv_vars['value'].get()))

        # Get current positions of all HSV sliders
        hMin = int(self.hsv_vars['hue'].get())
        sMin = int(self.hsv_vars['saturation'].get())
        vMin = int(self.hsv_vars['value'].get())

        # Set minimum and maximum HSV values to display (Assuming max values are static)
        hMax = 179  # This can be made dynamic if needed
        sMax = 255
        vMax = 255

        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])

        # Apply the HSV mask
        mask = cv2.inRange(hsv_image, lower, upper)
        result = cv2.bitwise_and(np_image, np_image, mask=mask)

        # Convert the numpy array back to a PIL Image
        self.image = Image.fromarray(result)
        
        # Update the displayed image
        self.place_image()
        
        
    
    def import_image(self,path):
        self.original = Image.open(path)
        self.image=self.original
        self.image_ratio = self.image.size[0]/self.image.size[1]
        self.image_tk=ImageTk.PhotoImage(self.image)

        self.image_import.grid_forget()
        self.image_output=ImageOutput(self,self.resize_image,self.brush_settings)
        self.close_button=CloseOutput(self,self.close_edit)
        self.menu=Menu(self,self.brush_settings,self.hsv_vars)
    
    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        self.image_import=ImageImport(self,self.import_image)
    
    def resize_image(self,event):
        # current canvas ratio
        canvas_ratio=event.width/event.height

        # update canvas attributes
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
        # Calculate centering position
        x_position = (self.canvas_width - self.image_width) // 2
        y_position = (self.canvas_height - self.image_height) // 2
        self.image_output.create_image(x_position, y_position, image=self.image_tk, anchor='nw')
        self.image_output.set_image_dimensions(x_position, y_position, self.image_width, self.image_height)
    
App()