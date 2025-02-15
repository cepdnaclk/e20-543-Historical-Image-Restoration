import customtkinter as ctk
from tkinter import filedialog,Canvas
from settings import *
class ImageImport(ctk.CTkFrame):
    def __init__(self, parent,import_func):
        super().__init__(master=parent)
        self.grid(column=0, row=0 ,columnspan=2, sticky='nsew')
        self.import_func=import_func

        ctk.CTkButton(self,text='open image',command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path=filedialog.askopenfilename()
        self.import_func(path)
    
class ImageOutput(Canvas):
    def __init__(self,parent,resize_image,brush_settings):
        super().__init__(master=parent,background=BACKGROUND_COLOR,bd=0, highlightthickness=0 , relief='ridge')
        self.grid(row = 0,column=1,sticky='nsew',padx=10,pady=10)
        self.bind('<Configure>',resize_image)
        
        self.brush_settings = brush_settings 
        
        # Binding mouse events
        self.bind("<Button-1>", self.start_painting)
        self.bind("<B1-Motion>", self.paint)
        self.bind("<ButtonRelease-1>", self.stop_painting)

        # Initialize drawing state
        self.last_x = None
        self.last_y = None
        
    def set_image_dimensions(self, x, y, width, height):
        self.image_x = x
        self.image_y = y
        self.image_width = width
        self.image_height = height
        

    def start_painting(self, event):
        # Start painting if within image bounds
        if self.is_within_image(event.x, event.y):
            self.last_x, self.last_y = event.x, event.y

    def paint(self, event):
        if self.last_x is not None and self.last_y is not None:
            if self.is_within_image(event.x, event.y):
                # Draw directly using event coordinates
                self.create_line(self.last_x, self.last_y, event.x, event.y,
                                 fill=self.brush_settings['color'].get(), 
                                 width=self.brush_settings['size'].get(), 
                                 capstyle='round', smooth=True)
                self.last_x, self.last_y = event.x, event.y

    def stop_painting(self, event):
        self.last_x, self.last_y = None, None
    
    def is_within_image(self, x, y):
        # Check if a point is within the bounds of the image
        return (self.image_x <= x < self.image_x + self.image_width) and (self.image_y <= y < self.image_y + self.image_height)
        
class CloseOutput(ctk.CTkButton):
    def __init__(self,parent,close_func):
        super().__init__(
            master=parent,
            command=close_func,
            text='x',
            text_color=WHITE,
            fg_color='transparent',
            width=40,
            height=40,
            corner_radius=0,
            hover_color=CLOSE_RED,
            )
        
        self.place(relx=0.99,rely=0.01,anchor='ne')