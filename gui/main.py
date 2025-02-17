import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk
from menu import Menu
import numpy as np
import cv2
from tkinter import Canvas
from PIL import ImageDraw

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

       
            
        for var in self.hsv_vars.values():
            var.trace('w',self.hsv_modified_image)
            
    
    def hsv_modified_image(self,*args):
        composite = self.composite.copy()
        
        # Convert to a numpy array for HSV manipulation
        np_image = np.array(composite.convert('RGB'))
        hsv_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2HSV)
        
        # Retrieve HSV slider values
        hMin = int(self.hsv_vars['hue'].get())
        sMin = int(self.hsv_vars['saturation'].get())
        vMin = int(self.hsv_vars['value'].get())
        hMax = 179  
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
        
    def generate_mask(self):
        # Work on a copy of the composite image (original + painting)
        composite = self.composite.copy()
        
        # Convert to a NumPy array and then to HSV
        np_image = np.array(composite.convert('RGB'))
        hsv_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2HSV)
        
        # Retrieve current HSV slider values
        hMin = int(self.hsv_vars['hue'].get())
        sMin = int(self.hsv_vars['saturation'].get())
        vMin = int(self.hsv_vars['value'].get())
        hMax = 179  
        sMax = 255
        vMax = 255

        lower = np.array([hMin, sMin, vMin])
        upper = np.array([hMax, sMax, vMax])
        
        # Create a binary mask: red-painted regions become white (255), the rest black (0)
        mask = cv2.inRange(hsv_image, lower, upper)
        
        # Save the raw composite image for inspection
        self.composite.save("debug_composite.png")
        # Save the raw mask to disk
        cv2.imwrite("debug_mask_raw.png", mask)
        
        # --- Debugging Code Start ---
        # Save the raw mask to disk for inspection
        cv2.imwrite('debug_mask.png', mask)
        
        
        # Optional: Clean up the mask (remove noise, fill small holes)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Save the mask for later use (e.g., for inpainting)
        self.mask = mask
        
        # Convert mask to an RGB image so it can be previewed in the GUI
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        mask_pil = Image.fromarray(mask_rgb)
        return mask_pil

        
    
    def import_image(self,path):
        self.original = Image.open(path)
        self.image=self.original.copy()
        
        self.draw = ImageDraw.Draw(self.image)
        
        # Store a composite image (original + strokes) for later processing
        self.composite = self.image.copy()
        
        self.image_ratio = self.image.size[0]/self.image.size[1]
        self.image_tk=ImageTk.PhotoImage(self.image)
        
        

        self.image_import.grid_forget()
        self.image_output=ImageOutput(self,self.resize_image,self.brush_settings)
        self.image_output.set_original_image(self.original) 
        self.close_button=CloseOutput(self,self.close_edit)
        self.menu=Menu(self,self.brush_settings,self.hsv_vars,self.image_output)
    
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
    
    def revert_image(self, original_image):
        """Revert the displayed image to the original image."""
        self.image = original_image.copy() # Set the current image to the original
        self.composite = self.image.copy()     # Update composite as well!
        self.draw = ImageDraw.Draw(self.image)
        self.image_tk = ImageTk.PhotoImage(self.image)  # Create a new PhotoImage
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
    
    def apply_inpainting(self, method="TELEA", inpaint_radius=3):
        # Ensure that a mask is available (generated previously)
        if not hasattr(self, "mask"):
            print("No mask available. Generate a mask first.")
            return

        # Convert the original image (kept intact) from PIL to a CV2 image (BGR)
        original_cv = cv2.cvtColor(np.array(self.original), cv2.COLOR_RGB2BGR)

        # Make sure the mask is in the proper format (uint8, single channel)
        mask_cv = self.mask.astype(np.uint8)
        
        # Choose the inpainting method based on the passed parameter:
        if method.upper() == "TELEA":
            flag = cv2.INPAINT_TELEA
        elif method.upper() in ["NS", "NAVIER-STOKES"]:
            flag = cv2.INPAINT_NS
        else:
            flag = cv2.INPAINT_TELEA

        # Apply the inpainting algorithm:
        inpainted_cv = cv2.inpaint(original_cv, mask_cv, inpaint_radius, flag)

        # Convert the inpainted image back to PIL format (convert BGR back to RGB)
        inpainted_pil = Image.fromarray(cv2.cvtColor(inpainted_cv, cv2.COLOR_BGR2RGB))
        inpainted_pil.save("debug_inpainted.png")

        # Update your images: we update self.image and self.composite to show the repaired image.
        self.image = inpainted_pil.copy()
        self.composite = inpainted_pil.copy()
        
        self.draw = ImageDraw.Draw(self.image)
        
        # Refresh the displayed image on the canvas.
        self.place_image()

App()