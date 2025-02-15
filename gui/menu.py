import customtkinter as ctk
from panels import *
import tkinter as tk

class Menu(ctk.CTkTabview):
    def __init__(self, parent,brush_settings,hsv_vars):
        super().__init__(master=parent)
        self.grid(column=0, row=0 , sticky='nsew', padx=10, pady=10)

        #tabs
        self.add('Paint')
        self.add('HSV')
        self.add('Effects')
        self.add('Export')

        #widgets
        PaintFrame(self.tab('Paint'),brush_settings)
        HSVFrame(self.tab('HSV'),hsv_vars)
        #EffectFrame(self.tab('Effects'),effect_vars)
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
    def __init__(self, parent, brush_settings):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.brush_settings = brush_settings

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
    def __init__(self, parent, hsv_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        SliderPanel(self, 'Hue', hsv_vars['hue'], 0, 179)
        SliderPanel(self, 'Saturation', hsv_vars['saturation'], 0, 255)
        SliderPanel(self, 'Value', hsv_vars['value'], 0, 255)