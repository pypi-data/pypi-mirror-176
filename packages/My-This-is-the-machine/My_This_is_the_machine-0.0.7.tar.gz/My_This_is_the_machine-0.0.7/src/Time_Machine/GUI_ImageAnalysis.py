#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:39:34 2022

@author: gorosti
"""

# import sys 
# sys.path.append('/home/gorosti/.local/lib/python3.6/site-packages')

import os                                                 
import numpy as np                                         # Numpy
import matplotlib.pyplot as plt                            # Plotting
import matplotlib.patches as patches                       # Just used to draw the rectangle defining the ROI
from matplotlib import colors
import cv2                                                 # For some of the image processing functions
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os.path import exists     
import tkinter as tk
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

from Time_Machine.Image_Process import ImageProcess 
from Time_Machine.Profile_Analysis import ProfileAnalysis



class DrawLineWidget(object):

    def __init__(self, contour_image):
        
        self.original_image = contour_image
        self.clone = self.original_image.copy()

        cv2.namedWindow('Drag Line with Mouse and press q')
        cv2.setMouseCallback('Drag Line with Mouse and press q', 
                             self.extract_coordinates)

        # List to store start/end points
        self.image_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            
            self.image_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:

            self.image_coordinates.append((x,y))
            x1 = self.image_coordinates[0][0]
            x2 = self.image_coordinates[1][0]
            y1 = self.image_coordinates[0][1]
            y2 = self.image_coordinates[1][1]
            length = ( (x1-x2)**2 + (y1-y2)**2 )**(1/2)
            self.length = length

            # Draw line
            cv2.line(self.clone, self.image_coordinates[0], self.image_coordinates[1], (0, 0, 255), 2)
            cv2.imshow('Drag Line with Mouse and press q', self.clone) 

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        
        return self.clone
    
    
#-----------------------------------------------#
#           MODIFY THE NAVIGATION TOOLBAR       #
#-----------------------------------------------#   
        
class My_Toolbar(NavigationToolbar2Tk):
    
    # Remove the display of coordinates

    def set_message(self, s):
        pass
        
            
        
        

#-----------------------------------------------#
#                START THE GUI                  #
#-----------------------------------------------#   


class ImageAnalysis_GUI(tk.Tk):
    
    def __init__(self, Data_path, var_to_abbrev):
        
        super().__init__()
    
        # Get screen size
        
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        
        # We define the title of the opening window
        
        self.title('Luminescence Analysis')
        
        # self.geometry("650x250")
        self.geometry( str(width) + "x" + str(height) )
        
        # self.attributes('fullscreen', True)
        self.configure(background='white')
        
        #Make the window jump above all
        self.lift()
        
        self.figsize = (6,4)
        self.dpi = np.minimum(width, height) / 13
        
        self.letter_type = "Roman, 12"
        self.letter_type_widgets = "Roman, 12"
        
        slider_length = 200
        
        #-----------------------------------------------#
        #         Define Initial Values                 #
        #-----------------------------------------------#  
        
        self.Data_path = Data_path
        self.var_to_abbrev = var_to_abbrev
        
        self.Calculation_Method = 6
        self.Rotation_angle = 0
        self.histogram_cut_contour = 80
        self.Smooth_factor = 1
        self.histogram_cut_mask = 60
        self.layer_thickness = 1
        self.layering_Method = 1
        self.mm_length = 50
        self.pixinmm = 1
        self.pixel_length = self.pixinmm * self.mm_length
        self.roi = np.array([118, 262, 250, 96])
        
        
        #-----------------------------------------------#
        #                 Create Frames                 #
        #-----------------------------------------------#   
        
        
        ### Method option ###
        
        self.frame_method = tk.Frame(self)
        self.frame_method.grid(row=0, column=0)
        self.frame_method.config(background='white')
        
        
        ### Contour options ###
        
        self.frame_opt_contour = tk.Frame(self)
        self.frame_opt_contour.grid(row=0, column=1)
        
        self.frame_th_contour = tk.Frame(self.frame_opt_contour)
        self.frame_th_contour.pack()
        self.frame_th_contour.config(background='white')
        
        self.frame_smooth_contour = tk.Frame(self.frame_opt_contour)
        self.frame_smooth_contour.pack()
        self.frame_smooth_contour.config(background='white')
        
        
        ### Layers options ###
        
        self.frame_opt_layers = tk.Frame(self)
        self.frame_opt_layers.grid(row=0, column=2)
        self.frame_opt_layers.config(background='white')
        
        self.frame_method_layers = tk.Frame(self.frame_opt_layers)
        self.frame_method_layers.pack()
        self.frame_method_layers.config(background='white')
        
        self.frame_method_layers_radio = tk.Frame(self.frame_method_layers)
        self.frame_method_layers_radio.pack( side = tk.LEFT)
        self.frame_method_layers_radio.config(background='white')
        
        self.frame_method_layers_info = tk.Frame(self.frame_method_layers)
        self.frame_method_layers_info.pack( side = tk.LEFT)  
        self.frame_method_layers_info.config(background='white')
        
        self.frame_thickness_layers = tk.Frame(self.frame_opt_layers)
        self.frame_thickness_layers.pack()
        self.frame_thickness_layers.config(background='white')
        
        
        ### Mask Option ###
        
        self.frame_opt_mask = tk.Frame(self)
        self.frame_opt_mask.grid(row=0, column=3)
        self.frame_opt_mask.config(background='white')
        
        
        ### Rotation Option ###
        
        self.frame_opt_rotation = tk.Frame(self)
        self.frame_opt_rotation.grid(row=7, column=2)
        self.frame_opt_rotation.config(background='white')
        
        
        ### Change ROI Option ###
        
        self.frame_opt_roi = tk.Frame(self)
        self.frame_opt_roi.grid(row=6, column=0)
        self.frame_opt_roi.config(background='white')
        
        
        # Pixel to mm Option ###
        
        self.frame_for_border = tk.Frame(self)
        self.frame_for_border.grid(row=4, column=0)
        self.frame_for_border['borderwidth'] = 2
        
        self.pixmm_frame = tk.Frame(self.frame_for_border)
        self.pixmm_frame.pack()
        self.pixmm_frame.config(background='white')
        
        self.frame_conversion = tk.Frame(self.pixmm_frame)
        self.frame_conversion.pack(padx=5, pady=(5, 0))
        self.frame_conversion.config(background='white')
        
        self.frame_opt_conversion = tk.Frame(self.pixmm_frame)
        self.frame_opt_conversion.pack(padx=5, pady=(0,5))
        self.frame_opt_conversion.config(background='white')
        
                        
        
        #-----------------------------------------------#
        #                 Define widgets                #
        #-----------------------------------------------#   
        
        
        ### Menu for choosing the calculation method ###
        
        self.label_method = tk.Label(self.frame_method,
                                       text="Select Calculation Method",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_method.pack(pady = 5, padx= (10, 5))  
               
        
        self.Method_options = ['Natural IRPL 880',
                               'Natural IRPL 955',
                               'IRPL 955/880',
                               'IRPL 880 Lx',
                               'IRPL 955 Lx',
                               'IRPL 880 Ln/Lx',
                               'IRPL 955 Ln/Lx',
                               'Delta IRPL 880',
                               'Delta IRPL 955',
                               'IRSL Ln',
                               'IRSL F1/Fx',
                               'IRSL Ln/Lx',
                               'IRSL Lx ']

        calc_method_variable = tk.StringVar()
        calc_method_variable.set(self.Method_options[self.Calculation_Method])
        
        self.method_title = self.Method_options[self.Calculation_Method]
        
        self.Method_Menu = tk.OptionMenu(self.frame_method,
                                         calc_method_variable,
                                         *self.Method_options,
                                         command = self.reset_calculation_method)
        
        self.Method_Menu.config(bg="white", font=self.letter_type_widgets)
    
        self.Method_Menu.pack(side = tk.LEFT, padx= (15, 5)) 
        
        
        
        ### Scale for choosing the rotation angle ###
        
        self.label_rotation = tk.Label(self.frame_opt_rotation,
                                       text="Rotation Angle [º]",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_rotation.pack()         
        
        self.Slider_rotation = tk.Scale(self.frame_opt_rotation,
                                        from_ = 0,
                                        to = 360, 
                                        highlightthickness = 0,
                                        orient = 'horizontal',
                                        length = 350)
        
        self.Slider_rotation.bind("<ButtonRelease-1>",
                                  self.reset_rotation_angle)
        self.Slider_rotation.set(self.Rotation_angle)
        
        self.Slider_rotation.configure(background='white')

        self.Slider_rotation.set(0)  # Set the initial value 
        self.Slider_rotation.pack(side = tk.LEFT, pady = 5) 
        
        
        
        
        ### Scale for choosing the contour histogram ###
        
        self.label_contour_histogram_cut = tk.Label(self.frame_th_contour,
                                            text="Brightness threshold Contour",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_contour_histogram_cut.pack(pady = (15, 5))          

        
        self.Slider_contour_histogram_cut = tk.Scale(self.frame_th_contour,
                                                     from_ = 40,
                                                     to = 90, 
                                                     highlightthickness = 0,
                                                     orient = 'horizontal',
                                                     length = slider_length)
        
        self.Slider_contour_histogram_cut.bind("<ButtonRelease-1>",
                                               self.reset_contour_histogram_cut)
        
        self.Slider_contour_histogram_cut.configure(background='white')
        
        self.Slider_contour_histogram_cut.set(self.histogram_cut_contour)  # Set the initial value 
        self.Slider_contour_histogram_cut.pack(side = tk.LEFT, pady = 5)      

        

        
        ### Scale for choosing the contour smoothening ###
        
        self.label_contour_smooth = tk.Label(self.frame_smooth_contour,
                                            text="Contour Smoothening",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_contour_smooth.pack(anchor='w', pady = 5)   
        
        
        self.Slider_contour_smoothening = tk.Scale(self.frame_smooth_contour,
                                                   from_ = 1,
                                                   to = 30, 
                                                   highlightthickness = 0,
                                                   orient = 'horizontal',
                                                   length = slider_length)
        
        self.Slider_contour_smoothening.bind("<ButtonRelease-1>", 
                                             self.reset_contour_smoothening)
        
        self.Slider_contour_smoothening.configure(background='white')
        
        self.Slider_contour_smoothening.set(self.Smooth_factor)  # Set the initial value
        self.Slider_contour_smoothening.pack(side = tk.LEFT, pady = 5)
        
        
        
        
        ### Radiobutton for the layering method selection ###
        
        self.label_radiobutton = tk.Label(self.frame_method_layers_radio,
                                            text="Select Layering Method",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_radiobutton.pack(pady = (15, 5), anchor='w')  
        
        # Choices are strings
 
        self.r1_model = tk.IntVar()
        
        # Assign default value
        
        self.r1_model.set(None) 
        
        self.Layer_Radiobutton_lr = tk.Radiobutton(self.frame_method_layers_radio,
                                                text = 'Layer Left to Right',
                                                highlightthickness = 0,
                                                variable = self.r1_model,
                                                value=0,
                                                font = self.letter_type_widgets,
                                                command = lambda : self.reset_layering_method(1))
        
        self.Layer_Radiobutton_lr.pack(anchor='w', pady=5, padx=5)
        
        self.Layer_Radiobutton_lr.config(bg='white', state='normal')
        
        
        self.Layer_Radiobutton_center = tk.Radiobutton(self.frame_method_layers_radio,
                                                text = 'Layer Towards the Center',
                                                highlightthickness = 0,
                                                variable = self.r1_model,
                                                value=1,
                                                font= self.letter_type_widgets,
                                                command = lambda : self.reset_layering_method(2))
        
        self.Layer_Radiobutton_center.pack(anchor='w', pady=5, padx=5)
        
        self.Layer_Radiobutton_center.config(bg='white')
    
        
        
        ### Scale for choosing the layer thickness ###
        
        self.label_thickness = tk.Label(self.frame_thickness_layers,
                                            text="Layer Thickness",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_thickness.pack(pady = 5, anchor='w')  
        
        
        self.Slider_layer_thickness = tk.Scale(self.frame_thickness_layers,
                                                   from_ = 1,
                                                   to = 30, 
                                                   highlightthickness = 0,
                                                   orient = 'horizontal',
                                                   length = slider_length)
        
        self.Slider_layer_thickness.bind("<ButtonRelease-1>", 
                                         self.reset_layer_thickness)
        
        self.Slider_layer_thickness.pack(side = tk.LEFT, pady=5)
        self.Slider_layer_thickness.set(self.layer_thickness)  # Set the initial value 
        
        self.Slider_layer_thickness.configure(background='white')
        
        
        
        ### Scale for choosing the mask histogram ###
        
        self.label_mask_histogram_cut = tk.Label(self.frame_opt_mask,
                                            text="Brightness threshold Mask",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_mask_histogram_cut.pack(pady = (15, 5), anchor='w')    
        
        self.Slider_mask_histogram_cut = tk.Scale(self.frame_opt_mask,
                                                  from_ = 0,
                                                  to = 100, 
                                                  highlightthickness = 0,
                                                  orient = 'horizontal',
                                                  length = slider_length)
        
        self.Slider_mask_histogram_cut.bind("<ButtonRelease-1>",
                                            self.reset_mask_histogram_cut)
        
        self.Slider_mask_histogram_cut.set(self.histogram_cut_mask)  # Set the initial value 
        self.Slider_mask_histogram_cut.pack(side = tk.LEFT, pady=5)
        
        self.Slider_mask_histogram_cut.configure(background='white')
        
        
        
        ### Button for re-selecting the ROI  ###
        
        
        self.label_roi = tk.Label(self.frame_opt_roi,
                                            text="Select Region \n of Interest",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_roi.pack(pady = (15, 5), anchor='w')  
        
        
        self.ChangeRoi_Button = tk.Button(self.frame_opt_roi,
                                          text = 'Select from Image',
                                          background='white',
                                          font = self.letter_type_widgets,
                                          command = self.update_ROI)
        self.ChangeRoi_Button.pack(side = tk.LEFT)
        
        
        
        ### Button for selecting pixel lenght  ###
        
        self.label_pixel = tk.Label(self.frame_conversion,
                                            text="Define the pixel \n to mm Conversion",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_pixel.pack(pady = 5, anchor='w', side = tk.LEFT)  
        
        
        self.ChangePixMm = tk.Button(self.frame_opt_conversion,
                                     text = 'Select line \n from Image',
                                     font=self.letter_type_widgets,
                                     command = self.update_pixel_length)
        self.ChangePixMm.pack(pady = 5, anchor='w')
        self.ChangePixMm.configure(background='white')
        
        
        
        ### Entry for mm input   ###
        
        self.label_mm = tk.Label(self.frame_opt_conversion,
                                            text="Insert length of \n selected line",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_mm.pack(pady = 5, anchor='w')          
        
        self.Entry_mm = tk.Entry(self.frame_opt_conversion,
                                 width=10,
                                 textvariable = tk.DoubleVar())
        
        self.Entry_mm.delete(0, tk.END)
        self.Entry_mm.insert(1, self.mm_length)
        
        self.Entry_mm.pack(pady = 5, anchor='w')
        
        
        
        ### Button for getting the new mm lenght ###
        
        self.label_update_pixmm = tk.Label(self.frame_opt_conversion,
                                            text="Update the Value",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_update_pixmm.pack(pady = 5, anchor='w')  
        
        
        self.Button_mm = tk.Button(self.frame_opt_conversion,
                                   font=self.letter_type_widgets,
                                   text = 'Update',
                                   command = self.update_mm_length)
        self.Button_mm.pack(pady=5)
        self.Button_mm.configure(background='white')
    
        
        
        ### Button for exporting the profile ###
        
        
        self.Export = tk.Button(self,
                                text = 'Export Profile Table',
                                background='white',
                                font=self.letter_type_widgets,
                                command = self.export_profile)
        self.Export.grid(row = 6, column = 3 )
        
        
        ### Button for closing Interface ###
        
        
        self.Button_close_interface = tk.Button(self,
                                text = 'Select this profile \n and close',
                                background='white',
                                font=self.letter_type_widgets,
                                command = self.close_interface)
        self.Button_close_interface.grid(row = 7, column = 3 )
        
        
        
        #-----------------------------------------------#
        #               Define Info Widgets             #
        #-----------------------------------------------#  
        

        ### Method ###
        
        
        self.Info_method = tk.Button(self.frame_method,
                                     text = '?',
                                     command = self.show_Info_Method)
        self.Info_method.pack(side = tk.LEFT)
        self.Info_method.configure(background='white')
        
        
        
        ### Brightness contour threshold ###
        
        
        self.Info_histo_contour = tk.Button(self.frame_th_contour,
                                            text = '?',
                                            command = self.show_Info_brightness_contour)
        self.Info_histo_contour.pack(side = tk.LEFT)
        self.Info_histo_contour.configure(background='white')
        
        
        
        ### Smooth contour ###
        
        
        self.Info_smooth_contour = tk.Button(self.frame_smooth_contour,
                                            text = '?',
                                            command = self.show_Info_smooth_contour)
        self.Info_smooth_contour.pack(side = tk.LEFT)
        self.Info_smooth_contour.configure(background='white')
        
        
        ### Choose layering method ###
        
        
        self.Info_layer_method = tk.Button(self.frame_method_layers_info,
                                            text = '?',
                                            command = self.show_Info_layer_method)
        self.Info_layer_method.pack(side = tk.LEFT)
        self.Info_layer_method.configure(background='white')
        
        
        
        ### Choose layer thickness ###
        
        
        self.Info_layer_thickness = tk.Button(self.frame_thickness_layers,
                                              text = '?',
                                              command = self.show_Info_layer_thickness)
        self.Info_layer_thickness.pack(side = tk.LEFT)
        self.Info_layer_thickness.configure(background='white')
             
        
        
        ### Brightness mask threshold ###
        
        
        self.Info_histo_mask = tk.Button(self.frame_opt_mask,
                                              text = '?',
                                              command = self.show_Info_brightness_mask)
        self.Info_histo_mask.pack(side = tk.LEFT)
        self.Info_histo_mask.configure(background='white')
        
        
        ### Rotation Angle ###
        
        self.Info_rotation = tk.Button(self.frame_opt_rotation,
                                              text = '?',
                                              command = self.show_Info_rotation)
        self.Info_rotation.pack(side = tk.LEFT)
        self.Info_rotation.configure(background='white')
        
        
        ### Change ROI ###
        
        self.Info_roi = tk.Button(self.frame_opt_roi,
                                  text = '?',
                                  command = self.show_Info_roi)
        self.Info_roi.pack(side = tk.LEFT)
        self.Info_roi.configure(background='white')
        
        
        ### Pixel to mm Conversion ###
        
        self.Info_pixtomm = tk.Button(self.frame_conversion,
                                  text = '?',
                                  command = self.show_Info_pixtomm)
        self.Info_pixtomm.pack(side = tk.LEFT, padx=10)
        self.Info_pixtomm.configure(background='white')
        
                
        #-----------------------------------------------#
        #                Call Functions                 #
        #-----------------------------------------------#   
        
        self.check_path()
        
        self.create_ImageProcessing_Class()        
        
        self.initialize_plots()
        
        

    #-----------------------------------------------#
    #      Create Functions to get Widget Values    #
    #-----------------------------------------------#   
    
    
    def reset_calculation_method(self, event):
        
        self.method_title = event
               
        self.Calculation_Method = self.Method_options.index(event)
        
        self.create_ImageProcessing_Class()   
        
        # Plots to update
                
        self.update_contour_plot() 
        self.update_layers_plot()    
        self.update_mask_plot()
        self.update_calculation_plot()
        self.update_profile_plot()
        
    
    def reset_rotation_angle(self, event):
               
        self.Rotation_angle = event.widget.get()
        
        self.create_ImageProcessing_Class()   
        
        # Plots to update
                
        self.update_contour_plot() 
        self.update_layers_plot()    
        self.update_mask_plot()
        self.update_calculation_plot()
        self.update_profile_plot()
    
    
    def reset_contour_histogram_cut(self, event):
               
        self.ImageProcess.histogram_cut_contour = event.widget.get()
        self.histogram_cut_contour = event.widget.get()
        
        # Plots to update
                
        self.update_contour_plot() 
        self.update_layers_plot()    
        self.update_mask_plot()
        self.update_calculation_plot()
        self.update_profile_plot()
        
        
    def reset_contour_smoothening(self, event):
                       
        self.ImageProcess.Smooth_factor = event.widget.get()
        self.Smooth_factor = event.widget.get()
                
        # Plots to update
        
        self.update_contour_plot() 
        self.update_layers_plot()    
        self.update_mask_plot()
        self.update_calculation_plot()
        self.update_profile_plot()
        
    
    def reset_layering_method(self, value):
        
        self.ImageProcess.layering_Method = value
        self.layering_Method = value
        
        # Plots to update
        
        self.update_layers_plot() 
        self.update_profile_plot()
        
        
    def reset_layer_thickness(self, event):
        
        self.ImageProcess.layer_thickness = event.widget.get()
        self.layer_thickness = event.widget.get()
        
        # Plots to update
        
        self.update_layers_plot() 
        self.update_profile_plot()
        
        
    def reset_mask_histogram_cut(self, event):
        
        self.ImageProcess.histogram_cut_mask = event.widget.get()
        self.histogram_cut_mask = event.widget.get()
        
        # Plots to update
        
        self.update_mask_plot() 
        self.update_calculation_plot()
        self.update_profile_plot()
        
        
    def update_ROI(self):
        
        self.ImageProcess.select_ROI()
        self.roi = self.ImageProcess.roi
        
        # Plots to update
        
        self.update_calculation_plot()
        self.update_profile_plot()
        
        
    def update_mm_length(self):
        
        self.mm_length = float( self.Entry_mm.get() )
        
        # Update
        
        self.update_pixel_to_mm()
        
        
    def update_pixel_length(self):
        
        contour_image = self.ImageProcess.image_with_contour
        
        draw_line_widget = DrawLineWidget(contour_image)
        
        while True:
            cv2.imshow('Drag Line with Mouse and press q',
                       draw_line_widget.show_image())
            
            key = cv2.waitKey(1)
        
            # Close program with keyboard 'q'
            if key == ord('q'):
                cv2.destroyAllWindows()
                break
            
        self.pixel_length = draw_line_widget.length
        
        # Update
        
        self.update_pixel_to_mm()
        
        
    def update_pixel_to_mm(self):
        
        self.pixinmm = self.mm_length / self.pixel_length 
        
        # Plots to update
        
        self.update_contour_plot() 
        self.update_layers_plot()    
        self.update_mask_plot()
        self.update_calculation_plot()
        self.update_profile_plot()
        
        
    def export_profile(self):

        # Convert depth array to pandas
        df_save = pd.DataFrame(self.ImageProcess.x * self.ImageProcess.layer_thickness * self.pixinmm, columns = ['Depth [mm]'])  
        
        # Add luminiscence signal
        df_save['Normalized Signal'] = pd.DataFrame(self.ImageProcess.profile_data)   
        
        # Add standard error             
        df_save['Standard Error'] = pd.DataFrame(self.ImageProcess.standard_error) 
        
        df_save.columns = range(df_save.shape[1])
        
        # Get saving path and name
        Save_path = filedialog.asksaveasfile(mode = 'w',
                                             title = "Save the file",
                                             initialdir = self.Data_path,
                                             defaultextension = ".txt",
                                             initialfile = 'Profile.txt')     
        
        df_save.to_csv(Save_path, line_terminator="\r", sep=" ",
                       header=None, index=False)
        
        
    def check_path(self):
        
        if exists(self.Data_path) == False:
            
            self.show_Error_Wrong_Path()
            
            # Ask for path
            Save_path = filedialog.askdirectory( title = "Select Folder Containing the Images",
                                                 initialdir = os.getcwd()) 
            
            self.Data_path = Save_path
        
        
    def close_interface(self):
        
        self.quit()        
        self.destroy()
    
        
        
              
    #-----------------------------------------------#
    #          Create ImageProcessing Class         #
    #-----------------------------------------------#   
    
    
        
    def create_ImageProcessing_Class(self):
                
        self.ImageProcess = ImageProcess(self.Calculation_Method,
                                         self.Data_path, 
                                         self.var_to_abbrev,
                                         self.Rotation_angle,
                                         self.histogram_cut_contour,
                                         self.Smooth_factor,
                                         self.histogram_cut_mask,
                                         self.layer_thickness,
                                         self.layering_Method,
                                         self.pixinmm,
                                         self.roi)
        
        if len(self.ImageProcess.missing_variables) > 0:
            
            answer = tk.messagebox.askquestion(parent = self,
                                               title = 'File not found',
                                    message= 'The file(s) for the variable(s) {} has/have not been found'.format(self.ImageProcess.missing_variables) + 
                                        '\n \n'+
                                        'Either the data path \n \n {}'.format(self.ImageProcess.Data_path) + 
                                        '\n \n or the file name(s) \n \n {}'.format( [self.ImageProcess.var_to_abbrev[x] for x in self.ImageProcess.missing_variables] )+ 
                                        '\n \n are incorrect '+
                                        '\n \n Do you want to manually select the file(s)?')
            
            if answer == 'yes':
            
                for x in self.ImageProcess.missing_variables:                                  
 
                    new_file_name = filedialog.askopenfilenames(parent = self,
                                                                title = "{} Signal".format(x),
                                                             initialdir = self.Data_path,
                                                             defaultextension = ".tif")
                    
                    file_name = new_file_name[0]
                        
                    rel_path = os.path.relpath( file_name, self.Data_path)
                    
                    # print('\n \n Data Path is {}'.format(self.Data_path))
                    # print('\n The file is {} \n'.format(file_name))
                    # print('The relative path is {} \n \n'.format(rel_path))
                    
                    self.var_to_abbrev[x] = rel_path
                    
                # print(new_file_name)   
                # print(self.Data_path)
                # print(os.path.relpath( str(new_file_name), str(self.Data_path)))
                # print(self.var_to_abbrev)    
                    
                self.ImageProcess = ImageProcess(self.Calculation_Method,
                                                 self.Data_path, 
                                                 self.var_to_abbrev,
                                                 self.Rotation_angle,
                                                 self.histogram_cut_contour,
                                                 self.Smooth_factor,
                                                 self.histogram_cut_mask,
                                                 self.layer_thickness,
                                                 self.layering_Method,
                                                 self.pixinmm,
                                                 self.roi)
                
                # print('The missing variables are ....')
                # print(self.ImageProcess.missing_variables)
                
                    
                    
        
    #-----------------------------------------------#
    #               Initialize Plots                #
    #-----------------------------------------------#   
        
    
    
    def initialize_plots(self):
             
        self.initialize_contour_plot()
        self.initialize_layer_mask()
        self.initialize_mask_plot()
        self.initialize_calculation_plot()
        self.initialize_profile_plot()
                
        
    def initialize_contour_plot(self):
               
        contour_image = self.ImageProcess.image_with_contour
        
        self.figure_contour = Figure(figsize = self.figsize,
                                     dpi = self.dpi)

        # create FigureCanvasTkAgg object
        self.figure_canvas_contour = FigureCanvasTkAgg(self.figure_contour, self)

        # create the toolbar
        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row= 3, column = 1)
        Contour_toolbar = My_Toolbar(self.figure_canvas_contour, toolbarFrame)
        Contour_toolbar.config(background='white')
        
        for button in Contour_toolbar.winfo_children():
            button.config(background='white')

        # create axes
        self.axes_contour = self.figure_contour.add_subplot()

        # create the barchart
        self.axes_contour.imshow(contour_image,
                                 extent=[0, len(contour_image)*self.pixinmm,
                                         0, len(contour_image)*self.pixinmm])
        
        self.axes_contour.set_title('Contour')
        self.axes_contour.set_xlabel('[mm]')
        self.axes_contour.set_ylabel('[mm]')
        

        self.figure_canvas_contour.get_tk_widget().grid(row = 4, column = 1 )
        
        
    def initialize_layer_mask(self):
                
        self.layer_mask = self.ImageProcess.layer_mask
        
        self.figure_layers = Figure(figsize = self.figsize,
                                    dpi = self.dpi)

        # create FigureCanvasTkAgg object
        self.figure_canvas_layers = FigureCanvasTkAgg(self.figure_layers, self)

        # create the toolbar
        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row = 3, column = 2)
        Layer_toolbar = My_Toolbar(self.figure_canvas_layers, toolbarFrame)
        Layer_toolbar.config(background='white')
        
        for button in Layer_toolbar.winfo_children():
            button.config(background='white')

        # create axes
        self.axes_layers = self.figure_layers.add_subplot()
        
        self.axes_layers.set_title('Depth Layers')
        self.axes_layers.set_xlabel('[mm]')
        self.axes_layers.set_ylabel('[mm]')
        
        self.layers_cbar = self.figure_layers.colorbar(self.axes_layers.imshow(self.ImageProcess.layer_mask * self.ImageProcess.layer_thickness * self.pixinmm,
                                                                               cmap = 'inferno',
                                                                               extent=[0, len(self.ImageProcess.layer_mask)*self.pixinmm,
                                                                                       0, len(self.ImageProcess.layer_mask)*self.pixinmm]))
        self.layers_cbar.set_label('[mm]')
        
        self.figure_canvas_layers.get_tk_widget().grid(row = 4, column = 2 )
        
        
    def initialize_mask_plot(self):
                
        self.mask = self.ImageProcess.mask
        
        self.figure_mask = Figure(figsize = self.figsize,
                                  dpi = self.dpi)

        # create FigureCanvasTkAgg object
        self.figure_canvas_mask = FigureCanvasTkAgg(self.figure_mask, self)

        # create the toolbar
        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row = 3, column = 3)
        Mask_toolbar = My_Toolbar(self.figure_canvas_mask, toolbarFrame)
        Mask_toolbar.config(background='white')
        
        for button in Mask_toolbar.winfo_children():
            button.config(background='white')

        # create axes
        self.axes_mask = self.figure_mask.add_subplot()

        # create the barchart
        color_map = plt.cm.viridis
        
        self.axes_mask.imshow(self.mask,
                              cmap= color_map,
                              extent=[0, len(self.ImageProcess.mask)*self.pixinmm,
                                      0, len(self.ImageProcess.mask)*self.pixinmm])
        
        yellow_patch = patches.Patch(color= color_map(255) , label='Included')
        blue_patch = patches.Patch(color= color_map(0), label='Excluded')

        self.axes_mask.set_title('Mask')
        self.axes_mask.legend(handles = [yellow_patch, blue_patch])
        
        self.axes_mask.set_xlabel('[mm]')
        self.axes_mask.set_ylabel('[mm]')
        

        self.figure_canvas_mask.get_tk_widget().grid(row = 4, column = 3 )
        
        
    def initialize_calculation_plot(self):
               
        calculation_image = self.ImageProcess.calculation
        
        self.figure_calculation = Figure(figsize = self.figsize,
                                         dpi = self.dpi)

        # create FigureCanvasTkAgg object
        self.figure_canvas_calculation = FigureCanvasTkAgg(self.figure_calculation, self)

        # create the toolbar
        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row = 5, column = 1)
        Calculation_toolbar = My_Toolbar(self.figure_canvas_calculation, toolbarFrame)
        Calculation_toolbar.config(background='white')
        
        for button in Calculation_toolbar.winfo_children():
            button.config(background='white')
    

        # create axes
        self.axes_calculation = self.figure_calculation.add_subplot()
        
        self.axes_calculation.cla()  

        # create the barchart
        self.axes_calculation.imshow(self.ImageProcess.calculation,
                                     extent=[0, len(self.ImageProcess.calculation)*self.pixinmm,
                                             0, len(self.ImageProcess.calculation)*self.pixinmm])
                                     
        self.axes_calculation.set_title('Normalized Brightness and ROI')
        
        self.axes_calculation.set_xlabel('[mm]')
        self.axes_calculation.set_ylabel('[mm]')
        
        self.figure_calculation.colorbar(self.axes_calculation.imshow(calculation_image))
        # cbar.set_label('Normalized brightness', rotation=270)
        
        # Define the rectangle containing the region of interest
        
        roi = self.ImageProcess.roi
        
        rectangle = patches.Rectangle((roi[0] * self.pixinmm, (len(self.ImageProcess.calculation)-roi[1]-roi[3]) * self.pixinmm),
                                       roi[2] * self.pixinmm, roi[3] * self.pixinmm,
                                       linewidth=1,
                                       edgecolor='r', 
                                       facecolor='none')
        
        self.axes_calculation.add_patch(rectangle)   #  Include the rectangle in the plot

        self.figure_canvas_calculation.get_tk_widget().grid(row = 6, column = 1 )
        
        
                    
    def initialize_profile_plot(self):
        
        self.figure_profile = Figure(figsize = self.figsize,
                                     dpi = self.dpi)
        
        self.figure_canvas_profile = FigureCanvasTkAgg(self.figure_profile, self)
        
        # Create the ProfileAnalysis object
        
        self.ProfileAnalysis = ProfileAnalysis(self.ImageProcess.profile_data,
                                               self.ImageProcess.standard_error, 
                                               self.ImageProcess.x,
                                               self.figure_profile,
                                               self.method_title)
        
        # self.figure_profile = self.ProfileAnalysis.figure_profile
        
        
        
        # create the toolbar
        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row = 5, column = 2)
        profile_toolbar = NavigationToolbar2Tk(self.figure_canvas_profile, toolbarFrame)
        profile_toolbar.config(background='white')
        
        for button in profile_toolbar.winfo_children():
            button.config(background='white')
        
        self.figure_canvas_profile.get_tk_widget().grid(row = 6, column = 2 )
        self.figure_canvas_profile.draw()
        
        
    #-----------------------------------------------#
    #                 Update Plots                  #
    #-----------------------------------------------#   
        
    def update_contour_plot(self):
                
        self.ImageProcess.create_contour()
        
        contour_image = self.ImageProcess.image_with_contour 
        
        self.axes_contour.imshow(self.ImageProcess.image_with_contour,
                                 extent=[0, len(contour_image)*self.pixinmm,
                                         0, len(contour_image)*self.pixinmm])
        self.figure_canvas_contour.draw()       
            
        
    def update_layers_plot(self):
               
        self.ImageProcess.create_layers()
        
        self.axes_layers.cla()  
        self.layers_cbar.remove() 
        
        # self.axes_layers.imshow(self.ImageProcess.layer_mask,
        #                         cmap = 'inferno',
        #                         extent=[0, len(self.ImageProcess.layer_mask)*self.pixinmm,
        #                                 0, len(self.ImageProcess.layer_mask)*self.pixinmm])
        
        self.axes_layers.set_title('Depth Layers')
        self.axes_layers.set_xlabel('[mm]')
        self.axes_layers.set_ylabel('[mm]')
        
        self.layers_cbar = self.figure_layers.colorbar(self.axes_layers.imshow(self.ImageProcess.layer_mask * self.ImageProcess.layer_thickness * self.pixinmm,
                                                                               cmap = 'inferno',
                                                                               extent=[0, len(self.ImageProcess.layer_mask)*self.pixinmm,
                                                                                       0, len(self.ImageProcess.layer_mask)*self.pixinmm]))
        self.layers_cbar.set_label('[mm]')
        
        self.figure_canvas_layers.draw()
        
    
    def update_mask_plot(self):
        
        self.ImageProcess.mask = self.ImageProcess.create_mask(self.ImageProcess.image_for_mask, 
                                                               self.ImageProcess.histogram_cut_mask,
                                                               self.ImageProcess.layer_mask )
        
        self.axes_mask.cla()  
        
        color_map = plt.cm.viridis
        bounds=[0,0.5,1]
        norm = colors.BoundaryNorm(bounds, color_map.N)
        
        # create the barchart
        color_map = plt.cm.viridis
        
        yellow_patch = patches.Patch(color= color_map(255) , label='Included')
        blue_patch = patches.Patch(color= color_map(0), label='Excluded')

        self.axes_mask.set_title('Mask')
        self.axes_mask.legend(handles = [yellow_patch, blue_patch])
        
        self.axes_mask.set_xlabel('[mm]')
        self.axes_mask.set_ylabel('[mm]')
        
        self.axes_mask.imshow(self.ImageProcess.mask,
                              cmap= color_map,
                              norm = norm,
                              extent=[0, len(self.ImageProcess.mask)*self.pixinmm,
                                      0, len(self.ImageProcess.mask)*self.pixinmm])
        
        self.figure_canvas_mask.draw()
        
        
    def update_calculation_plot(self):
        
        self.ImageProcess.make_calculation()
        
        self.axes_calculation.cla()  
        
        self.axes_calculation.imshow(self.ImageProcess.calculation,
                                     extent=[0, len(self.ImageProcess.calculation)*self.pixinmm,
                                             0, len(self.ImageProcess.calculation)*self.pixinmm])
                                     
        self.axes_calculation.set_title('Normalized Brightness and ROI')
        self.axes_calculation.set_xlabel('[mm]')
        self.axes_calculation.set_ylabel('[mm]')
        
        # Define the rectangle containing the region of interest
        
        roi = self.ImageProcess.roi
        
        rectangle = patches.Rectangle((roi[0] * self.pixinmm, (len(self.ImageProcess.calculation)-roi[1]-roi[3]) * self.pixinmm),
                                       roi[2] * self.pixinmm, roi[3] * self.pixinmm,
                                       linewidth=1,
                                       edgecolor='r', 
                                       facecolor='none')
        
        
        self.axes_calculation.add_patch(rectangle)   #  Include the rectangle in the plot
        
        self.figure_canvas_calculation.draw()
        
        
    def update_profile_plot(self):
        
        self.ImageProcess.make_profile()
        
        # Create the ProfileAnalysis object
        
        # self.ProfileAnalysis.axes_profile.cla()
        self.figure_profile.clear()
        
        self.ProfileAnalysis = ProfileAnalysis(self.ImageProcess.profile_data,
                                               self.ImageProcess.standard_error, 
                                               self.ImageProcess.x * self.pixinmm,
                                               self.figure_profile,
                                               self.method_title)
        
        self.figure_canvas_profile.draw()
        
        
    #-----------------------------------------------#
    #               Edit the Info Boxes             #
    #-----------------------------------------------#  
        
    
    def show_Error_Wrong_Path(self):        
    
        tk.messagebox.showerror(title = 'Missing path!', 
                               message = 'The introduced data path'
                               ' does not exist! \n \n'
                               '{} \n \n Select a valid directory instead:'.format(self.Data_path))
    

    def show_Info_Method(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'Signal', 
                               message = 'The luminescence profile can be derived'
                               ' from different signals (or combination of them). \n \n'
                               ' This option allows the user to choose'
                               ' different images to build the profile from.')
        
        
    def show_Info_brightness_contour(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'Brighness threhold', 
                               message = 'The program needs some help in order to'
                               ' find the contour defining the rock surface. \n \n'
                               ' The brightness threshold tells the programm how'
                               ' many pixels should be included within the contour'
                               ' and how many should be left out. \n \n'
                               ' Fit this value until the contour visually fits'
                               ' the rock sample')
        
        
        
    def show_Info_smooth_contour(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'Smooth the contour', 
                               message = 'Increase this value if the'
                               ' shape of the contour is reather noisy'
                               ' to remove some of the undesired features.')
        
        
    def show_Info_layer_method(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'Layering Method', 
                               message = 'Two different options can be chosen'
                               ' in order to create the "depth layers": \n \n'
                               ' 1- Left to right: if this option is selected the'
                               ' layers are created by columns starting from the'
                               ' left side of the contour. \n \n'
                               ' 2- Towards the center: this option takes the'
                               ' contour and erodes towards the center from all'
                               ' The biggest advantage of this approach is that'
                               ' it can handle curved surfaces and there is'
                               ' no need to have the rock surface properly aligned'
                               ' with the vertical.')
        
        
    def show_Info_layer_thickness(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'Layer thickness', 
                               message = 'This value represents the thickness'
                               ' of each "depth layer" in pixel units. \n \n'
                               ' it is recommended to keep it as low as possible'
                               ' so that no resolution is lost.')
        
        
    def show_Info_brightness_mask(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'Brighness threhold', 
                               message = 'It might be the case that some of the'
                               ' pixels are saturated and that it is convenient'
                               ' to remove (not take into account) the brightest'
                               ' of them. \n \n On the other hand if too many are'
                               ' removed relevant information might be lost'
                               ' in the process. \n \n'
                               ' The user has to choose a proper value of a threshold'
                               ' for a reasonable trade off of these two aspects.')

        
    def show_Info_rotation(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'Rotation Angle', 
                               message = 'Rotating the sample might be conveninent. \n \n'
                               'The rotation angle goes counter-clockwise.')
        
        
    def show_Info_roi(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'What is the Region of Interest (ROI)?', 
                               message = 'Only the pixels inside the ROI are'
                               ' taken into account while everything outside is ignored \n \n'
                               )
        
        
    def show_Info_pixtomm(self):        
   
        tk.messagebox.showinfo(parent=self, 
                               title = 'How many milimeters is one pixel?', 
                               message = 'The program only know the size of'
                               ' the rock surface in pixel units. \n \n'
                               'However, we want the luminescence profile as'
                               'a function of physical lenght (mm) \n \n'
                               'This means that the user has to specify'
                               ' the conversion from mm to pixel units by'
                               ' following the next steps: \n \n'
                               '1- Drag a line with the mouse along a representative'
                               ' part of the rock. \n \n'
                               '2- Measure the lenght of the equivalent line in'
                               ' the physical rock in milimiters and'
                               ' enter it into the program.')

