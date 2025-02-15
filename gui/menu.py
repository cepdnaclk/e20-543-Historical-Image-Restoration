import customtkinter as ctk
from panels import *

class Menu(ctk.CTkTabview):
    def __init__(self, parent,pos_vars,hsv_vars):
        super().__init__(master=parent)
        self.grid(column=0, row=0 , sticky='nsew', padx=10, pady=10)

        #tabs
        self.add('Position')
        self.add('HSV')
        self.add('Effects')
        self.add('Export')

        #widgets
        PositionFrame(self.tab('Position'),pos_vars)
        HSVFrame(self.tab('HSV'),hsv_vars)
        #EffectFrame(self.tab('Effects'),effect_vars)
        #ExportFrame(self.tab('Export'),export_image)
        
class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent,pos_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        SliderPanel(self,'Rotation',pos_vars['rotate'],0,360)
        # SliderPanel(self,'Zoom',pos_vars['zoom'],0,200)
        # SegmentedPanel(self,'Invert',pos_vars['flip'],FLIP_OPTIONS)

        # RevertButton(
        #     self,
        #     (pos_vars['rotate'],ROTATE_DEFAULT),
        #     (pos_vars['zoom'],ZOOM_DEFAULT),
        #     (pos_vars['flip'],FLIP_OPTIONS[0])
        # )
        
# class ColorFrame(ctk.CTkFrame):
#     def __init__(self, parent,color_vars):
#         super().__init__(master=parent, fg_color='transparent') 
#         self.pack(expand=True, fill='both')

#         # SwitchPanel(self,(color_vars['grayscale'],'B/W'),(color_vars['invert'],'Invert'))
#         # SliderPanel(self,'Brightness',color_vars['brightness'],0,5)
#         # SliderPanel(self,'Vibrance',color_vars['vibrance'],0,5)
#         # RevertButton(
#         #     self,
#         #     (color_vars['brightness'],BRIGHTNESS_DEFAULT),
#         #     (color_vars['grayscale'],GRAYSCALE_DEFAULT),
#         #     (color_vars['invert'],INVERT_DEFAULT),
#         #     (color_vars['vibrance'],VIBRANCE_DEFAULT)
#         # )

class HSVFrame(ctk.CTkFrame):
    def __init__(self, parent, hsv_vars):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        SliderPanel(self, 'Hue', hsv_vars['hue'], 0, 179)
        SliderPanel(self, 'Saturation', hsv_vars['saturation'], 0, 255)
        SliderPanel(self, 'Value', hsv_vars['value'], 0, 255)