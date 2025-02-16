import customtkinter as ctk
from panels import *
import tkinter as tk
from PIL import Image, ImageTk

class Menu(ctk.CTkTabview):
    def __init__(self, parent,brush_settings,hsv_vars,image_output):
        super().__init__(master=parent)
        self.grid(column=0, row=0 , sticky='nsew', padx=10, pady=10)

        #tabs
        self.add('Paint')
        self.add('HSV')
        self.add('Restore')
        self.add('Export')

        #widgets
        PaintFrame(self.tab('Paint'),brush_settings,image_output)
        HSVFrame(self.tab('HSV'),parent,hsv_vars)
        RestoreFrame(self.tab('Restore'), parent) 
        #ExportFrame(self.tab('Export'),export_image)
        
# class PositionFrame(ctk.CTkFrame):
#     def __init__(self, parent,pos_vars):
#         super().__init__(master=parent, fg_color='transparent')
#         self.pack(expand=True, fill='both')

#         SliderPanel(self,'Rotation',pos_vars['rotate'],0,360)
#         SliderPanel(self,'Zoom',pos_vars['zoom'],0,200)
#         SegmentedPanel(self,'Invert',pos_vars['flip'],FLIP_OPTIONS)

#         RevertButton(
#             self,
#             (pos_vars['rotate'],ROTATE_DEFAULT),
#             (pos_vars['zoom'],ZOOM_DEFAULT),
#             (pos_vars['flip'],FLIP_OPTIONS[0])
#         )

def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


class PaintFrame(ctk.CTkFrame):
    def __init__(self, parent, brush_settings,image_output):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.brush_settings = brush_settings
        self.image_output = image_output

        # Brush size control
        self.brush_size_slider = SliderPanel(self, "Brush Size", brush_settings['size'], 1, 50)
        self.brush_size_slider.pack(pady=10)

        # Brush color buttons
        colors = {
            "Red": (255, 0, 0),
            "Green": (0, 255, 0),
            "Blue": (0, 0, 255)
        }
        
        
        # Container frame for radio buttons and labels
        color_frame = ctk.CTkFrame(self, fg_color='transparent', width=1)  
        color_frame.pack(fill='x', pady=10, padx=10) 
        
        # Dictionary to store button references
        self.color_buttons = {}
        
        # Create buttons for color choices
        for color_name, rgb in colors.items():
            # Button for each color
            hex_color = rgb_to_hex(rgb) 
            color_button = ctk.CTkButton(color_frame, text=color_name,text_color="black", fg_color=hex_color,
                                         command=lambda rgb=rgb, cn=color_name: self.set_brush_color(rgb,cn))
            color_button.pack(side='top', pady=2)
            self.color_buttons[color_name] = color_button
            
        # Initialize the brush color properly using the default color in hex
        default_color = rgb_to_hex(colors["Red"])  # Assuming default is "Red"
        self.brush_settings['color'].set(default_color)
        self.set_brush_color(colors["Red"], "Red")
        
        # Undo button
        self.undo_button = UndoButton(self, image_output.undo)
            
        
    
    def set_brush_color(self, color,color_name):
        hex_color = rgb_to_hex(color) 
        self.brush_settings['color'].set(hex_color)
        # Update buttons' state to reflect the selection
        for name, btn in self.color_buttons.items():
            if name == color_name:
                btn.configure(state='disabled')  # Disable the selected button
            else:
                btn.configure(state='normal')  # Enable all other buttons
         
     

class HSVFrame(ctk.CTkFrame):
    def __init__(self, parent,app, hsv_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.app = app
        
        SliderPanel(self, 'Hue', hsv_vars['hue'], 0, 179)
        SliderPanel(self, 'Saturation', hsv_vars['saturation'], 0, 255)
        SliderPanel(self, 'Value', hsv_vars['value'], 0, 255)
        
        # Button to generate the mask based on current HSV settings
        self.generate_mask_button = ctk.CTkButton(self, text="Generate Mask", command=self.generate_mask)
        self.generate_mask_button.pack(pady=10)
        
        # Label to display the mask preview
        self.mask_label = ctk.CTkLabel(self, text="Mask Preview")
        self.mask_label.pack(pady=10)
        
    def generate_mask(self):
        # Generate the mask using the App's generate_mask() method (returns a PIL Image)
        mask_pil = self.app.generate_mask()
        
        # Define the desired preview width (adjust as needed)
        preview_width = 300
        # Calculate preview height to maintain the aspect ratio:
        preview_height = int(mask_pil.height * preview_width / mask_pil.width)
        
        # Resize the PIL mask image:
        mask_pil_resized = mask_pil.resize((preview_width, preview_height))
        
        # Convert the PIL image to a CTkImage (use dark_image; you could also set light_image)
        mask_ctk = ctk.CTkImage(dark_image=mask_pil_resized, size=(preview_width, preview_height))
        
        # Update the label with the new CTkImage:
        self.mask_label.configure(image=mask_ctk, text="")  # Remove text if any
        self.mask_label.image = mask_ctk  # Keep a reference to avoid GC
        
class RestoreFrame(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both', padx=10, pady=10)
        self.app = app  # This is the main App instance

        # Option menu for selecting the inpainting method.
        self.method_var = ctk.StringVar(value="TELEA")
        self.method_option = ctk.CTkOptionMenu(
            self, 
            values=["TELEA", "Navier-Stokes"],
            variable=self.method_var
        )
        self.method_option.pack(pady=10)

        # Button to apply inpainting.
        self.inpaint_button = ctk.CTkButton(
            self, 
            text="Apply Inpainting", 
            command=self.apply_inpainting
        )
        self.inpaint_button.pack(pady=10)

    def apply_inpainting(self):
        # Get the selected method from the option menu.
        method = self.method_var.get()
        # Call the App's inpainting method with the selected method.
        self.app.apply_inpainting(method=method)
