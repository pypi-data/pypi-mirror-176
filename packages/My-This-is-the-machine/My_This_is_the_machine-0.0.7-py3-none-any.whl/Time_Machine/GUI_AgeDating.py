#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:33:42 2022

@author: gorosti
"""

# Import libraries

import os
from os.path import exists, isfile, expanduser                                                      
import numpy as np                                       
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

# Import Classes and functions from other files

from Time_Machine.Profile_Analysis import ProfileAnalysis
from Time_Machine.GUI_ImageAnalysis import ImageAnalysis_GUI
from Time_Machine.Inversion_Class import InversionModel, select_model, age_calculation, r_square, get_bleach_depth
from Time_Machine.Multi_Stage import Multi_Stage_Model


# We define our Dating Interface Class

class Dating_GUI(tk.Tk):
    
    def __init__(self, Data_path, var_to_abbrev_cal, var_to_abbrev_ana):
        
        super().__init__()
        
        ### Get initial data and file names ###
        
        self.Data_path = Data_path
        self.var_to_abbrev_cal = var_to_abbrev_cal
        self.var_to_abbrev_ana = var_to_abbrev_ana
        
        
        ### Call functions ###
        
        # Set environment
        
        self.set_window_parameters()
        
        self.set_initial_values()
        
        # Start with the frame
        
        self.create_initial_frame()
        
        
    def set_window_parameters(self):
        
        """
        Set the parameters defining the Interface window itself
        """
        
        # We define the title of the opening window   
        
        self.title('First Page')
        
        # Allow this Interface window to go to a second level when
        # opening other windows
        
        self.attributes('-topmost', False)
        
        # Get screen size and define the geometry and figure size accordingly
        
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry( str(width) + "x" + str(height))
        self.figsize = (5,4)
        self.dpi = np.minimum(width, height) / 14
        
        # Set a white background of the window
        
        self.configure(background='white')
        
        # Define the type of font that will be displayed 
        
        self.letter_type = "Roman, 12"
        self.letter_type_widgets = "Roman, 12"
        
        # Define the lenth of the sliders in pixels
        
        self.slider_length = 200
        

    def set_initial_values(self):
        
        """
        Set initial values for the different parameters in the GUI.
        
        All of them can be changed within the GUI itself, however an initial
        guess is required
        """
    
        ### Values which are required in general ###
        
        # Initially no frame is defined
        
        self.current_frame = 0
        
        # One event model selected per default
        
        self.stage_number = '1'
        
        # Second order selected per default
        
        self.selected_model = 'Second Order'
        self.n_model = select_model(self.selected_model) 
        
        
        ### Values for the One Event Model ###
        
        # Known age of the calibration sample
        
        self.known_age = 0.37
        
        # Amount of iterations for the sigma-phi matrix 
        
        self.n_iterations = 500
        self.n_iterations_min = 300
        self.n_iterations_max = 1000
        
        # Don't force the mu from the calibration sample into the 
        # dating sample
        
        self.mu = 'None'
        self.mu_error = None
        
        
        ### Values for the Multi-Stage Event Model ###

        # Initial guess for the value of Sigma_Phi and F
        
        self.Initial_guess_Sigma_Phi = 5e3
        self.Initial_guess_F = 1 / 280
        
        # Initial value of the power factor for the MS model fitting
        
        self.Power_factor = 1
        
        
    #-----------------------------------------------#
    #                 MAIN WORKFLOW                 #
    #-----------------------------------------------#   
          
        
    def create_initial_frame(self):

        """
        Create the Frame that initially opens
        
        Different frames are defined inside of it in onder to make a better
        splitting of the screen
        
        This frame will ask the user to choose which model to use:
            One Event / Multi Event model
        
        When the accept button is pressed the next frame opens depending on
        the chosen model
        """
        
        #------------------------#
        #          Frame         #
        #------------------------#  
        
        ### Frame for the Menu for the model selection ###
        
        # We first create a border
        
        self.frame_menu_border = tk.Frame(self)
        self.frame_menu_border.grid(row=0, column=0, padx=5, pady=5)
        self.frame_menu_border['borderwidth'] = 2
        
        # Frame inside of it
        
        self.frame_menu = tk.Frame(self.frame_menu_border)
        self.frame_menu.grid(row=0, column=0)
        self.frame_menu.config(background='white')
        
        # We now split the frame for the menu into different sub-frames:
            
        # Frame for the model choices
        
        self.frame_events = tk.Frame(self.frame_menu)
        self.frame_events.grid(row=0, column=0)
        self.frame_events.config(background='white')  
        
        # Frame for the model choice title
        
        self.frame_events_text = tk.Frame(self.frame_events)
        self.frame_events_text.grid(row=0, column=0)
        self.frame_events_text.config(background='white')  
        
        # Frame for the model choice RadioButton
        
        self.frame_events_radio = tk.Frame(self.frame_events)
        self.frame_events_radio.grid(row=1, column=0)
        self.frame_events_radio.config(background='white')  
        
        # Frame for the Update button
        
        self.frame_menu_update = tk.Frame(self.frame_menu)
        self.frame_menu_update.grid(row=1, column=0)
        self.frame_menu_update.config(background='white')
        
        
        #------------------------#
        #         Widgets        #
        #------------------------# 
        
        ### Label ###
        
        # Define it
    
        self.label_model = tk.Label(self.frame_events_text,
                                       text="Select Model",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        
        # Position it
        
        self.label_model.pack(side = tk.LEFT, pady = (10, 5), padx= (10, 5))  
        
        
        ### Radiobutton with the model choices ###
        
        # Choices are strings
        
        self.r1_model = tk.StringVar()
        
        # Assign default value
        
        self.r1_model.set('One Event') 
        
        # Define first button
        
        self.Radio1_1s_model = tk.Radiobutton(self.frame_events_radio,
                            text='One Event Model', 
                            highlightthickness = 0,
                            variable=self.r1_model, 
                            value='One Event',
                            font = self.letter_type_widgets,
                            command = lambda : self.reset_Model(0))
        
        # Place it and configure its display
        
        self.Radio1_1s_model.pack(anchor='w')
        self.Radio1_1s_model.config(bg="white", font=self.letter_type_widgets)
        
        # Define second button
        
        self.Radio2_1s_model = tk.Radiobutton(self.frame_events_radio, 
                            text='Multi Event Model', 
                            highlightthickness = 0,
                            variable=self.r1_model, 
                            value='MS',
                            font = self.letter_type_widgets,
                            command = lambda : self.reset_Model(1))
        
        # Place it and configure display
        
        self.Radio2_1s_model.pack(anchor='w')
        self.Radio2_1s_model.config(bg="white", font=self.letter_type_widgets)
        
        self.r1_model.set('One Event') 
        
        ### Info Model ###
        
        # Question Mark button wich provides helpful information when clicked
        
        # Define
                    
        self.Info_Model = tk.Button(self.frame_events_text,
                                     text = '?',
                                     command = self.show_Info_Model)
        
        # Place and configure
        
        self.Info_Model.pack(side = tk.LEFT)
        self.Info_Model.configure(background='white')
        
        
        ###  Accept Button ###
        
        # When pressed the programm moves on with the selected model 
        
        # Definition, placing and display configuration        
        
        self.Button_update = tk.Button(self.frame_menu_update,
                                    font=self.letter_type_widgets,
                                    text = 'Accept',
                                    command = self.second_frame)
        
        self.Button_update.pack(pady=5)
        self.Button_update.configure(background='white')
        
        
    def second_frame(self):

        """
        First it cleans any previously existing frames (except for the model
        selection one). Later it calls the functions that creates the new
        frame
        """
        
        # Runs when the Accept button is pressed
        # Change the text of the Button to 'Update'
        
        self.Button_update.config(text="Update")
        
        # Clean current frame
        
        self.clear_frame()

        # Create New Frame 
        
        self.create_model_frame()
        
        
    def clear_frame(self):

        """
        Clears the frame that was in previous use in order to start a new
        empty one
        
        Two different frames are in use within this program:
            One Event (Stage) Frame
            Multi Stage Frame
        Depending on which one was in use the cleaning routine differs
        """
        
        ### If the 1 stage frame was in use we clear it ###
        
        if self.current_frame == 1:
        
            # Clear One Event frame
            
            self.frame_AgeDating.grid_forget()
            
            
        ### If the Multi-Stage frame was in use we clear it ###
            
        if self.current_frame == 2:
        
            self.frame_MS_border.grid_forget()
        
        
    def create_model_frame(self):

        """
        Create the frame for all the further analyses
        
        This frame will be different depending on the chosen 
        Model: One/Multiple Events
        """
        
        
        ### If One Event Model is selected  ###
               
        if self.stage_number == '1':
                
            # Establish that the current frame is for 1 stage
            
            self.current_frame = 1
            
            # Establish that the One Stage canvas is not yet created
            
            self.canvas_created_1s_calibration = False
            self.canvas_created_1s_dating = False
            
            self.calib_performed = False
            
            # Create the 1 stage frame
            
            self.create_one_Stage_frame()
                        
            
        ### If the multi stage model is selected   ###
        
        else:
            
            # We show a warning if this Model is selected
            
            self.show_Warning_Stages()
                            
            # Establish that the current frame is for 2 (for the MultiStage
            # Model)
                
            self.current_frame = 2 
            
            # Establish that the MS canvas is not yet created
            
            self.canvas_created_MS = False
            self.canvas_created_MS_Stages = False
            
            # Establish that the ages have not been calculated yet
            
            self.Age_calculated = False
            
            # Create the Multiple Stage frame
            
            self.create_MS_frame()
            
            
    #-----------------------------------------------#
    #                One Event Frame                #
    #-----------------------------------------------#  
    
    #---------------------------------------#
    #          Calibration sample           #
    #---------------------------------------#  
            

    def create_one_Stage_frame(self):
        
        """
        Create the initial frame for the One Event Model
        
        This frame will ask the user to choose a data source for the 
        calibration profile. When a profile data is selectd then this profile
        will be plotted and the window will move on
        """
        
        #------------------------#
        #          Frame         #
        #------------------------# 
        
        ### Frame for all the posterior analysis ###
        
        self.frame_AgeDating = tk.Frame(self)
        self.frame_AgeDating.grid(sticky="W", row=0, column=1)
        self.frame_AgeDating.config(background='white')
        
        ### CALIBRATION SAMPLE ###
        
        # We create a big frame for it with a border
        
        self.frame_calibration_border = tk.Frame(self.frame_AgeDating)
        self.frame_calibration_border.grid(sticky="W",
                                           row=0, column=0, 
                                           padx=(10,10), pady=(10, 10))
        self.frame_calibration_border['borderwidth'] = 2
        
        self.frame_calibration = tk.Frame(self.frame_calibration_border)
        self.frame_calibration.grid(row=0, column=0)
        self.frame_calibration.config(background='white')
        
        # We create all the sub-frames inside the calibration one
        
        ### Frame for the data source option ###
        
        self.frame_choose_profile_cal = tk.Frame(self.frame_calibration)
        self.frame_choose_profile_cal.grid(row=0, column=0)
        self.frame_choose_profile_cal.config(background='white')
        
        
        ### Frame to plot the selected Profile ###
        
        self.frame_cal_profile = tk.Frame(self.frame_calibration)
        self.frame_cal_profile.grid(row=2, column=0)
        self.frame_cal_profile.config(background='white')
        
        
        #------------------------#
        #         Widgets        #
        #------------------------#  
        
        ### Choose profile source for calibration ###
        
        # Define and place the label
        
        self.label_choose_profile_cal = tk.Label(self.frame_choose_profile_cal,
                                       text="Select Calibration Profile Data Source",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_choose_profile_cal.pack(pady = (10, 5), padx= (10, 5))  
        
        # Define the options
        
        self.Source_options = ['From txt File',
                               'From Image Analysis']

        source_method_variable = tk.StringVar()
        source_method_variable.set(self.Source_options[1])
        
        # Define, configure and place the Menu that allows the user to choose
        
        self.Source_Menu = tk.OptionMenu(self.frame_choose_profile_cal,
                                         source_method_variable,
                                         *self.Source_options,
                                         command = self.reset_profile_source_cal)
        
        self.Source_Menu.config(bg="white", font=self.letter_type_widgets)
    
        self.Source_Menu.pack(side = tk.LEFT, padx= (15, 5)) 
        
        
        ### Button for Information ###        
        
        self.Info_choose_profile = tk.Button(self.frame_choose_profile_cal,
                                     text = '?',
                                     command = self.show_Info_Choose_Profile)
        self.Info_choose_profile.pack(side = tk.LEFT)
        self.Info_choose_profile.configure(background='white')
        
        
    def reset_profile_source_cal(self, event):

        """
        Create the profile of the sample from which the model will be
        fitted and plot it 
        
        After its creation the window will move on depending on the chosen
        model: One/Multiple events
        """
        
        # Get the source: from a txt file or from image analysis
        
        self.profile_source = self.Source_options.index(event)
               
        # Get new profile
                
        self.get_new_profile(self.var_to_abbrev_cal)
        
        # We now define how to continue with the program
        
        if self.stage_number == '1':
            
            # Save dataframe to second variable
            
            self.df_cal = self.df
            
            # Plot it
            
            self.initialize_profile_plot(self.frame_cal_profile,
                                         self.df_cal)
            
            # If the canvas has not been defined yet we create it
            
            if self.canvas_created_1s_calibration == False:
        
                self.create_canvas_first_order()
                
            # If a previous analysis has already been carried out we proceed
            # to move on and do all the calibration analysis with the
            # existing setup
                
            if self.calib_performed == True:
                
                self.update_known_age()
                
            # We change the text of the label
            
            self.label_choose_profile_cal.config(text = 'Change Calibration Profile Data Source')
            
        
        else:
            
            # Save dataframe to second variable
            
            self.df_MS = self.df
            
            self.initialize_profile_plot(self.frame_MS_profile,
                                         self.df_MS)
            
            # If the canvas has not been defined yet we create it
            
            if self.canvas_created_MS == False:
        
                self.create_canvas_MS_order()
                
            # If a previous analysis has already been carried out we proceed
            # to move on and do all the analysis with the existing setup
                
            if self.canvas_created_MS_Stages == True:
                
                self.begin_MS_analysis()
            
            # We change the text of the label
            
            self.label_choose_profile.config(text = 'Change Profile Data Source')
        

            
            

    def create_canvas_first_order(self):
        
        """
        Creates the canvas where the user is asked to choose the order of
        the One Event model (First Order/Second Order) and to input the 
        age of the calculation sample
        """
        
        #------------------------#
        #          Frame         #
        #------------------------#  
        
        ### Frame for the Model Order and calibration Age entry menu ###
        
        # First we include a border
        
        self.frame_order_age_menu_bor = tk.Frame(self.frame_calibration)
        self.frame_order_age_menu_bor.grid(row=2, column=1)
        self.frame_order_age_menu_bor['borderwidth'] = 2
        
        self.frame_order_age_menu = tk.Frame(self.frame_order_age_menu_bor)
        self.frame_order_age_menu.grid(row=0, column=0)
        self.frame_order_age_menu.config(background='white')
        
        
        ### Frame to choose the order of the model ###
        
        self.frame_choose_model_cal = tk.Frame(self.frame_order_age_menu,
                                               width = self.frame_order_age_menu.winfo_width())
        self.frame_choose_model_cal.grid(sticky="W",
                                         padx=(5,2), pady=(2, 20),
                                         row=0, column=0)
        self.frame_choose_model_cal.config(background='white')
        
        
        ### Frame for the entry for known age, with text 1st and then entry ###
        
        self.frame_known_age = tk.Frame(self.frame_order_age_menu)
        self.frame_known_age.grid(sticky="W",
                                  padx=(5,2), pady=(2, 2),
                                  row=1, column=0)
        self.frame_known_age.config(background='white')
        
        self.frame_known_age_text = tk.Frame(self.frame_known_age)
        self.frame_known_age_text.grid(sticky="W",
                                       row=0, column=0)
        self.frame_known_age_text.config(background='white')
        
        self.frame_known_age_entry = tk.Frame(self.frame_known_age)
        self.frame_known_age_entry.grid(row=1, column=0)
        self.frame_known_age_entry.config(background='white')
        
        
        ### Frame for Fitted Plot ###
        
        self.frame_fit_plot_cal = tk.Frame(self.frame_calibration)
        self.frame_fit_plot_cal.grid(row=2, column=2)
        self.frame_fit_plot_cal.config(background='white')
        
        
        ### Frame for the Matrix Plot ###
        
        self.frame_matrix_plot_cal = tk.Frame(self.frame_calibration)
        self.frame_matrix_plot_cal.grid(row=2, column=3)
        self.frame_matrix_plot_cal.config(background='white')
        

        ### Frame for the Number of iterations ###
        
        self.frame_iterations = tk.Frame(self.frame_calibration)
        self.frame_iterations.grid(row=0, column=3)
        self.frame_iterations.config(background='white')
        
        
        ### Frame to print parameter values ###
        
        self.frame_parameters = tk.Frame(self.frame_calibration)
        self.frame_parameters.grid(row=2, column=4)
        self.frame_parameters.config(background='white')
        
        
        #------------------------#
        #         Widgets        #
        #------------------------#        
        
        ## Choose Exposure Model Order ###
        
        # Label definition and placing
    
        self.label_choose_model = tk.Label(self.frame_choose_model_cal,
                                        text="Select Exposure Model",
                                        borderwidth = 0,
                                        background='white',
                                        font = self.letter_type)
        self.label_choose_model.pack(pady = (10, 5))  
        
        # Model Order Choices        
        
        self.model_options = ['First Order',
                              'Second Order']

        model_variable = tk.StringVar()
        model_variable.set(self.model_options[1])
        
        # Order OptionMenu definition, display config and placing
        
        self.Model_Menu = tk.OptionMenu(self.frame_choose_model_cal,
                                          model_variable,
                                          *self.model_options,
                                          command = self.reset_profile_model_fit_1s)
        
        self.Model_Menu.config(bg="white", font=self.letter_type_widgets)
    
        self.Model_Menu.pack(side = tk.LEFT, anchor='e') 
        
        
        ### Info Order ###
        
        # Definintion, placing and display configuration
                    
        self.Info_Order = tk.Button(self.frame_choose_model_cal,
                                      text = '?',
                                      command = self.show_Info_Order)
        self.Info_Order.pack(side = tk.LEFT, anchor='e')
        self.Info_Order.configure(background='white')
        
        
        ### Entry for Known Age ###
        
        # Definition and placing of the label
        
        self.label_known_Age = tk.Label(self.frame_known_age_text,
                                            text="Insert the age of \n the calibration \n sample in years",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_known_Age.pack(side = tk.LEFT, pady = 5, anchor='w')    
        
        # Info Button of Age of Calibration Sample, definition, 
        # placing and config
                    
        self.Info_Age_cal = tk.Button(self.frame_known_age_text,
                                     text = '?',
                                     command = self.show_Info_Calibration_Age)
        self.Info_Age_cal.pack(side = tk.LEFT)
        self.Info_Age_cal.configure(background='white')
        
        # Enrtry for know age, definition, configuration and placing
        
        self.Entry_age = tk.Entry(self.frame_known_age_entry,
                                 width=10,
                                 textvariable = tk.DoubleVar())
        
        self.Entry_age.delete(0, tk.END)
        self.Entry_age.insert(1, self.known_age)
        
        self.Entry_age.pack(pady = 5, anchor='w')
        
        # Button for accepting the previous setting and move on with
        # the program
        
        self.Button_age = tk.Button(self.frame_known_age_entry,
                                    font=self.letter_type_widgets,
                                    text = 'Accept',
                                    command = self.update_known_age)
        
        self.Button_age.pack(pady=10)
        self.Button_age.configure(background='white')
        
                    
        ### Text for the parameters ###
        
        self.param_table = tk.Text(self.frame_parameters,
                              font = self.letter_type_widgets)
        
        # We establish that the canvas has been created
        
        self.canvas_created_1s_calibration = True
        
        
        
    def update_known_age(self):
        
        """
        Takes the current value of the calibration age and proceeds 
        to continue the program by calling the function which will 
        initialize the One stage model. If the canvas is not created yet
        then the corresponding function will be called in order to do so
        """
        
        # Change the text of the 'Accept' button to 'Update'
        
        self.Button_age.config(text="Update")
        
        # Take the age which is in the entry box
        
        self.known_age = float( self.Entry_age.get())
        
        # Create the 1 Event canvas if it's not already created
        
        # Initialize the One Event Model for the calibration sample
        
        self.initialize_model_fit_cal()
        
        # If the canvas for the dating sample is not yet created
        # we create it now
        
        if self.canvas_created_1s_dating == False:
            
            # Create canvas
        
            self.One_stage_canvas_Dating_Sample()
            
            # Establish that the canvas has been created
            
            self.canvas_created_1s_dating = True
            
        # We establish that the calibration has been done
            
        self.calib_performed = True

        

    def initialize_model_fit_cal(self):
        
        """
        This function starts the One Stage Event class (InversionModel)
        and fits the profile according to the previously chosen setup
        
        Plots the fitted profile as well as the Sigma_Phi vs Mu matrix
        
        Prints the values for the different fitting (and fitted) parameters
        
        Calls the function which starts the analysis of the Dating Sample
        """
        
        # Create the One Stage calibration Class
        
        self.CALIBRATION_SAMPLE = InversionModel(self.df_cal) 
        
        # Define the canvas for the figures which will contain the fitted
        # profile and the Sigma_Phi vs mu matrix

        self.figure_fit_cal_fit = Figure(figsize = self.figsize,
                                     dpi = self.dpi)
        
        self.figure_fit_cal_matrix = Figure(figsize = self.figsize,
                                     dpi = self.dpi)
        
        
        self.figure_canvas_fit_fit = FigureCanvasTkAgg(self.figure_fit_cal_fit,
                                                       self.frame_fit_plot_cal)
        self.figure_canvas_fit_matrix = FigureCanvasTkAgg(self.figure_fit_cal_matrix, 
                                                          self.frame_matrix_plot_cal)
        
        # Calibrate the One Stage Class
        
        self.CALIBRATION_SAMPLE.calibrate(self.n_model, 
                                          self.known_age * 365.25*24*3600, 
                                          self.n_iterations,
                                          self.figure_fit_cal_fit,
                                          self.figure_fit_cal_matrix,
                                          verbose = True)
        
        # Get the bleaching depth
        
        XMAX = 50        
        self.CALIBRATION_SAMPLE.BLEACH_DEPTH = get_bleach_depth(XMAX,
                                                self.CALIBRATION_SAMPLE.mu_median,
                                                self.CALIBRATION_SAMPLE.sigma_phi_median,
                                                self.known_age,
                                                self.n_model)
        
        # Calculate the R-square of the fitted function
        
        self.CALIBRATION_SAMPLE.r2 = r_square(self.CALIBRATION_SAMPLE,
                                              self.n_model, 
                                              "ignore_plateau")
        
        # Place the figure with the Fitted Profile
        
        self.figure_canvas_fit_fit.get_tk_widget().grid(row=0, column=0)
        self.figure_canvas_fit_fit.draw()
        
        # Create its toolbar: define, place and configure it
        
        toolbarFrame = tk.Frame (master = self.frame_fit_plot_cal)
        toolbarFrame.grid(row=1, column=0)
        fit_toolbar = NavigationToolbar2Tk(self.figure_canvas_fit_fit,
                                           toolbarFrame)
        fit_toolbar.config(background='white')
        
        # Set the backgroung of each button within the toolbar to white
        
        for button in fit_toolbar.winfo_children():
            button.config(background='white')
            
            
        # Repeat the process fot the figure containing the 
        # Sigma_Phi vs mu plot
        
        # Place the figure
        
        self.figure_canvas_fit_matrix.get_tk_widget().grid(row=0, column=0)
        self.figure_canvas_fit_matrix.draw()
        
        # Create its toolbar: define, place and configure it
        
        toolbarFrame = tk.Frame(master = self.frame_matrix_plot_cal)
        toolbarFrame.grid(row=1, column=0)
        matrix_toolbar = NavigationToolbar2Tk(self.figure_canvas_fit_matrix, 
                                              toolbarFrame)
        matrix_toolbar.config(background='white')
        
        # Set the backgroung of each button within the toolbar to white
        
        for button in matrix_toolbar.winfo_children():
            button.config(background='white')

            
        # Print the values of the fitted parameters
        
        self.print_parameters()
        
        # Move on and start with the analysis of the Dating Sample
        # if the profile for it already exists
        
        if hasattr(self, 'df_analysis'):
            
            self.initialize_model_fit_analysis()
            
            
    def print_parameters(self):
        
        """
        Prints the values of some of the relevant parameters of the 
        fitting of the calibration sample of the One Stage Model
        """
        
        list_to_print = self.CALIBRATION_SAMPLE.log
        
        list_to_print = ['\u03C3\u03C6 Median = {0:.2E} [s-1]'.format(self.CALIBRATION_SAMPLE.sigma_phi_median),
                         '\u03BC Median = {0:.2f} [mm-1]'.format(self.CALIBRATION_SAMPLE.mu_median),
                         'R-Square = {0:.2f}'.format(self.CALIBRATION_SAMPLE.r2),
                         'Bleaching Depth = {0:.2f} [mm]'.format(self.CALIBRATION_SAMPLE.BLEACH_DEPTH)]

        
        self.param_table.delete("1.0", "end")  # if you want to remove the old data
        
        for x in list_to_print:
            
            self.param_table.insert(tk.END, x + '\n \n')
            
        self.param_table.pack()
            
            
    #---------------------------------------#
    #             Dating Sample             #
    #---------------------------------------#  
            
       
    def One_stage_canvas_Dating_Sample(self):
        
        """
        Initialize the canvas for the Dating Sample in the case of the 
        One Event Model
        
        This canvas will include the option for the user to choose the 
        data source (Image Analysis / txt file) for the luminescence profile 
        as well as the option to choose the Mu value from either the 
        calibration sample or from the dating sample instead
        """
        
        #------------------------#
        #          Frame         #
        #------------------------#   
                
        # We create a big frame for it with a border 
        
        self.frame_analysis_border = tk.Frame(self.frame_AgeDating)
        self.frame_analysis_border.grid(sticky="W",
                                        row=1, column=0, 
                                        padx=(10,10), pady=(10, 10))
        self.frame_analysis_border['borderwidth'] = 2
        
        self.frame_analysis = tk.Frame(self.frame_analysis_border)
        self.frame_analysis.grid(row=0, column=0)
        self.frame_analysis.config(background='white')
        
        ### Frame for Data source option ###
        
        self.frame_choose_profile_analysis = tk.Frame(self.frame_analysis)
        self.frame_choose_profile_analysis.grid(row=0, column=0)
        self.frame_choose_profile_analysis.config(background='white')
        
        ### Frame for the Forced mu option ###
        
        # We create sub-frames for the text and the menu
        
        self.frame_choose_forced_mu = tk.Frame(self.frame_analysis)
        self.frame_choose_forced_mu.grid(row=0, column=1)
        self.frame_choose_forced_mu.config(background='white')      
        
        self.frame_choose_forced_mu_text = tk.Frame(self.frame_choose_forced_mu)
        self.frame_choose_forced_mu_text.grid(row=0, column=0)
        self.frame_choose_forced_mu_text.config(background='white') 
        
        self.frame_choose_forced_mu_menu = tk.Frame(self.frame_choose_forced_mu)
        self.frame_choose_forced_mu_menu.grid(row=1, column=0)
        self.frame_choose_forced_mu_menu.config(background='white') 
        
        #------------------------#
        #         Widgets        #
        #------------------------#   
                 
        ### Choose profile source analysis ###
        
        # Define and place the label
        
        self.label_choose_profile_analysis = tk.Label(self.frame_choose_profile_analysis,
                                       text="Select Dating Profile Data Source",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_choose_profile_analysis.pack(pady = (10, 5), padx= (10, 5)) 
        
        # Define possible methods: From image / from txt
        
        source_method_variable = tk.StringVar()
        source_method_variable.set(self.Source_options[1])
        
        # Define, config and place the method menu: Image / txt file                
        
        self.Source_Menu = tk.OptionMenu(self.frame_choose_profile_analysis,
                                         source_method_variable,
                                         *self.Source_options,
                                         command = self.reset_profile_source_analysis)
        
        self.Source_Menu.config(bg="white", font=self.letter_type_widgets)
    
        self.Source_Menu.pack(side = tk.LEFT, padx= (15, 5)) 
        
        
        ### Scale for the number of iterations ###
        
        # Label definition and placement
        
        self.label_iterations = tk.Label(self.frame_iterations,
                                            text="Number of Iterations",
                                            borderwidth = 0,
                                            background='white',
                                            font = self.letter_type)
        self.label_iterations.pack(pady = (15, 5), anchor='w')  
        
        # Slider definition
        
        self.Slider_iterations = tk.Scale(self.frame_iterations,
                                                  from_ = self.n_iterations_min,
                                                  to = self.n_iterations_max, 
                                                  highlightthickness = 0,
                                                  orient = 'horizontal',
                                                  length = self.slider_length)
        
        # Bind the slider to a command:
        # > When slider released reset the number of iterations
        
        self.Slider_iterations.bind("<ButtonRelease-1>",
                                     self.reset_iteration)
        
        # Set slider initial value, place and configure it
        
        self.Slider_iterations.set(self.n_iterations)  # Set the initial value 
        self.Slider_iterations.pack(side = tk.LEFT, pady=5)
        
        self.Slider_iterations.configure(background='white')
        
        
        ### Info Iterations ###
        
        # Definition, placing and configuration of the button
                    
        self.Info_Iterations = tk.Button(self.frame_iterations,
                                     text = '?',
                                     command = self.show_Info_Iterations)
        self.Info_Iterations.pack(side = tk.LEFT)
        self.Info_Iterations.configure(background='white')

        
        ### Choose if mu should be forced ###
        
        # Label definition and placing
        
        self.label_forced_mu = tk.Label(self.frame_choose_forced_mu_text,
                                       text="Forced mu",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_forced_mu.pack(side = tk.LEFT, pady = (10, 5), padx= (10, 5)) 
        
        # The options are strings
        
        self.r1_v = tk.StringVar()
        
        self.r1_v.set('Calibration') 
        
        # 1st radiobutton definition, placement and configuration
        
        self.Radio_mu1 = tk.Radiobutton(self.frame_choose_forced_mu_menu,
                            text='Mu from Calibration Sample', 
                            highlightthickness = 0,
                            variable=self.r1_v, 
                            value='Calibration',
                            font = self.letter_type_widgets,
                            command = lambda : self.reset_mu(0))
        self.Radio_mu1.pack(anchor='w')
        self.Radio_mu1.config(bg="white", font=self.letter_type_widgets)
        
        # 2nd radiobutton definition, placement and configuration
        
        self.Radio_mu2 = tk.Radiobutton(self.frame_choose_forced_mu_menu, 
                            text='Mu from Dating Sample', 
                            highlightthickness = 0,
                            variable=self.r1_v, 
                            value='Dating',
                            font = self.letter_type_widgets,
                            command = lambda : self.reset_mu(1))
        self.Radio_mu2.pack(anchor='w')
        self.Radio_mu2.config(bg="white", font=self.letter_type_widgets)
        
        self.r1_v.set('Calibration') 
        
        ### Info Non/forced mu ###
        
        # Definition, placing and configuration of the Info button
                    
        self.Info_Forced_mu = tk.Button(self.frame_choose_forced_mu_text,
                                     text = '?',
                                     command = self.show_Info_Forced_Mu)
        self.Info_Forced_mu.pack(side = tk.LEFT)
        self.Info_Forced_mu.configure(background='white')
        
        
        
    def reset_profile_source_analysis(self, event):
        
        """
        Create the profile of the sample from which the model will be
        fitted and plot it 
        
        After its creation the window will move on and create the dating
        analysis
        """
        
        # Get how the profile has to be loaded (From Images / txt file)
        
        self.profile_source = self.Source_options.index(event)
               
        # Show warning to tell the user to be consistent in the methods 
        # used in the analysis of the calibration sample 
        
        self.show_Warning_Method()
        
        # Get profile
                
        self.get_new_profile(self.var_to_abbrev_ana)
        
        # Store the dataframe containing the profile data
        
        self.df_analysis = self.df
        
        # Update the text of the label
        
        self.label_choose_profile_analysis.config(text = 'Change Dating Profile Data Source')
        
        # Create profile plot
        
        self.initialize_profile_plot(self.frame_analysis,
                                     self.df_analysis)
        
        # Start the analysis of the dating profile
        
        self.initialize_model_fit_analysis()

        
            
    def initialize_model_fit_analysis(self):
        
        """
        Creates the Dating Sample class and calls the age calculation
        function
        """
        
        # We create the One Stage Class using the profile for the 
        # dating sample > We create the Dating Sample object
        
        self.DATING_SAMPLE = InversionModel(self.df_analysis) 
        
        # We 'calibrate' it
             
        self.DATING_SAMPLE.calibrate_no_plots(self.n_model,
                                              'None',
                                              self.n_iterations,
                                              verbose = True)
        
        # We proceed to calculate the age
        
        self.calculate_age()
        
        
   
    def calculate_age(self):
        
        """
        This function performs the age calculation given the Dating
        Sample Class
        
        It plots two figures showing the model fitting and the resulting
        distribution of age likelihood
        """
        
        # We define the figures and their canvas:
        # One figure for showing the model Fitting and a 
        # second one for the distribution of age distribution
        
        self.figure_fit_age = Figure(figsize = self.figsize,
                                     dpi = self.dpi)
        
        self.figure_age_histo = Figure(figsize = self.figsize,
                                     dpi = self.dpi)
        
        self.figure_canvas_age_fit = FigureCanvasTkAgg(self.figure_fit_age,
                                                       self.frame_analysis)
        
        self.figure_canvas_age_histo = FigureCanvasTkAgg(self.figure_age_histo,
                                                         self.frame_analysis)
        
        # We run the age calculation function
        
        CALC_T, model_of_dating_sample = age_calculation(self.df_analysis,
                        self.selected_model,
                        self.n_model,
                        self.CALIBRATION_SAMPLE,
                        self.figure_fit_age,
                        self.figure_age_histo,
                        mu_forced = self.mu, 
                        mu_error_forced = self.mu_error, 
                        age_tt = self.n_iterations)
        
        # Place the figure of the fitted profile
        
        self.figure_canvas_age_fit.get_tk_widget().grid(row = 2, column = 1)
        self.figure_canvas_age_fit.draw()
        
        # Create its toolbar: define, place and configure it
        
        toolbarFrame = tk.Frame(master = self.frame_analysis)
        toolbarFrame.grid(row = 3, column = 1)
        fit_anal_toolbar = NavigationToolbar2Tk(self.figure_canvas_age_fit, toolbarFrame)
        fit_anal_toolbar.config(background='white')
        
        # Set the backgroung of each button within the toolbar to white
        
        for button in fit_anal_toolbar.winfo_children():
            button.config(background='white')
        
        # Place the figure of the fitted profile
        
        self.figure_canvas_age_histo.get_tk_widget().grid(row = 2, column = 2)
        self.figure_canvas_age_histo.draw()
        
        # Create its toolbar: define, place and configure it
        
        toolbarFrame = tk.Frame(master = self.frame_analysis)
        toolbarFrame.grid(row = 3, column = 2)
        age_hist_toolbar = NavigationToolbar2Tk(self.figure_canvas_age_histo, toolbarFrame)
        age_hist_toolbar.config(background='white')
        
        # Set the backgroung of each button within the toolbar to white
        
        for button in age_hist_toolbar.winfo_children():
            button.config(background='white')
            
            
            
    #-----------------------------------------------#
    #               Multi Event Model               #
    #-----------------------------------------------#  
    
    
    def create_MS_frame(self):
        
        """
        Create the initial frame for the Multiple Event Model
        
        This frame will ask the user to choose a data source for the 
        profile. When a profile data is selectd then this profile
        will be plotted and the window will move on
        """
        
        #------------------------#
        #          Frame         #
        #------------------------# 
        
        ### Frame for Multy-Stage Analysis ###
            
        self.frame_MS_border = tk.Frame(self)
        self.frame_MS_border.grid(sticky="W", 
                                  row=0, column=1,
                                  padx=(10,10), pady=(10, 10))
        self.frame_MS_border['borderwidth'] = 2
       
        self.frame_MS = tk.Frame(self.frame_MS_border)
        self.frame_MS.grid(row=0, column=0)
        self.frame_MS.config(background='white')
        
        ### Data source option ###
       
        self.frame_MS_choose_profile = tk.Frame(self.frame_MS)
        self.frame_MS_choose_profile.grid(row=0, column=0)
        self.frame_MS_choose_profile.config(background='white')  
       
        ### Frame for Profile plotting ###
       
        self.frame_MS_profile = tk.Frame(self.frame_MS)
        self.frame_MS_profile.grid(row=1, column=0)
        self.frame_MS_profile.config(background='white')       
               
        
        #------------------------#
        #         Widgets        #
        #------------------------# 

        
        ### Choose profile source calibration ###
        
        # Label definition and placing
        
        self.label_choose_profile = tk.Label(self.frame_MS_choose_profile,
                                       text="Select Profile Data Source",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_choose_profile.pack(pady = (10, 5), padx= (10, 5))  
        
        # Definion of the possibilities
        
        self.Source_options = ['From txt File',
                               'From Image Analysis']

        source_method_variable = tk.StringVar()
        source_method_variable.set(self.Source_options[1])
        
        # Define the Opiton menu, configure and place it 
        
        self.Source_Menu = tk.OptionMenu(self.frame_MS_choose_profile,
                                         source_method_variable,
                                         *self.Source_options,
                                         command = self.reset_profile_source_cal)
        
        self.Source_Menu.config(bg="white", font=self.letter_type_widgets)
    
        self.Source_Menu.pack(side = tk.LEFT, padx= (15, 5)) 
        
        # Include the information button        
        
        self.Info_choose_profile = tk.Button(self.frame_MS_choose_profile,
                                     text = '?',
                                     command = self.show_Info_Choose_Profile)
        self.Info_choose_profile.pack(side = tk.LEFT)
        self.Info_choose_profile.configure(background='white')
        
        
        
    def create_canvas_MS_order(self):
        
        """
        Creates the canvas where the user is asked to choose the order of
        the One Event model (First Order/Second Order) and the number of the
        events of (2/3)
        
        This function runs when a profile for the MS model is chosen
        """
        
        #------------------------#
        #          Frame         #
        #------------------------# 
        
        ### Menu for choosing model order and nº of stages, border ###
        
        self.frame_MS_menu_border = tk.Frame(self.frame_MS)
        self.frame_MS_menu_border.grid(row=1, column=1)
        self.frame_MS_menu_border['borderwidth'] = 2
 
        self.frame_MS_menu = tk.Frame(self.frame_MS_menu_border)
        self.frame_MS_menu.grid(row=0, column=0)
        self.frame_MS_menu.config(background='white')
       
        # Select Number of Stages
       
        self.frame_MS_stages = tk.Frame(self.frame_MS_menu)
        self.frame_MS_stages.grid(row=0, column=0)
        self.frame_MS_stages.config(background='white')  
        
        # Model option
       
        self.frame_MS_choose_model = tk.Frame(self.frame_MS_menu)
        self.frame_MS_choose_model.grid(row=1, column=0)
        self.frame_MS_choose_model.config(background='white')
       
        # Setup Update button #
       
        self.frame_MS_menu_update = tk.Frame(self.frame_MS_menu)
        self.frame_MS_menu_update.grid(row=2, column=0)
        self.frame_MS_menu_update.config(background='white')  
       
       
        ### Plot Fitted Model ###
       
        self.frame_MS_fitted_profile = tk.Frame(self.frame_MS)
        self.frame_MS_fitted_profile.grid(row=1, column=2)
        self.frame_MS_fitted_profile.config(background='white')  
        
        #------------------------#
        #         Widgets        #
        #------------------------# 
        
        # Choose number of Stages
        
        # Define and place label
        
        self.label_n_stages = tk.Label(self.frame_MS_stages,
                                       text="Select Number of Events",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_n_stages.pack(pady = (10, 5), padx= (10, 5))  
        
        
        # Define possible options
        
        self.stage_options = ['2',
                              '3']
        
        stages_variable = tk.StringVar()
        stages_variable.set(self.stage_options[0])
        
        # Create option menu, configure and place it
        
        self.Stage_Menu = tk.OptionMenu(self.frame_MS_stages,
                                         stages_variable,
                                         *self.stage_options,
                                         command = self.reset_stage_number)
        
        self.Stage_Menu.config(bg="white", font=self.letter_type_widgets)
        
        self.Stage_Menu.pack(side = tk.LEFT, padx= (15, 5)) 
        
        
        # Info Stages, define place and config
                    
        self.Info_SetUp = tk.Button(self.frame_MS_stages,
                                     text = '?',
                                     command = self.show_Info_Number_Stages)
        self.Info_SetUp.pack(side = tk.LEFT)
        self.Info_SetUp.configure(background='white')
        
        
        ### Choose Exposure Model ###
        
        # Definiton and placing of label
        
        self.label_choose_model = tk.Label(self.frame_MS_choose_model,
                                       text="Select Exposure Model",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_choose_model.pack(pady = (10, 5), padx= (10, 5))  
        
        # Definition of the possibilities
        
        self.model_options = ['First Order',
                              'Second Order']
        
        model_variable = tk.StringVar()
        model_variable.set(self.model_options[1])
        
        # Definition of the OptionMenu, configuration and placing
        
        self.Model_Menu = tk.OptionMenu(self.frame_MS_choose_model,
                                         model_variable,
                                         *self.model_options,
                                         command = self.reset_profile_model_fit_MS)
        
        self.Model_Menu.config(bg="white", font=self.letter_type_widgets)
        
        self.Model_Menu.pack(side = tk.LEFT, padx= (15, 5)) 
        
        
        # Info Order definition, placing and configuration
                    
        self.Info_Order = tk.Button(self.frame_MS_choose_model,
                                     text = '?',
                                     command = self.show_Info_Order)
        self.Info_Order.pack(side = tk.LEFT)
        self.Info_Order.configure(background='white')
        
        
        ### Include Update Button ###
        
        # Definition, placing and configuration
        
        self.Button_update_MS = tk.Button(self.frame_MS_menu_update,
                                    font=self.letter_type_widgets,
                                    text = 'Accept',
                                    command = self.begin_MS_analysis)
        
        self.Button_update_MS.pack(pady=5)
        self.Button_update_MS.configure(background='white')
        
        # We establish that this canvas has already been created
        
        self.canvas_created_MS = True


    def begin_MS_analysis(self):

        """
        Takes the current value of the profile and menu (Nuber of Events
        an order of the model) to continues the program by calling the
        function which will initialize the MS model. 
        If the canvas is not created yet then the corresponding function
        will be called in order to do so
        """
        
        # Change the text of the 'Accept' button to 'Update'
        
        self.Button_update_MS.config(text="Update")
        
        # Create the MS Stage canvas if it's not already created
        
        if self.canvas_created_MS_Stages == False:
        
            self.MS_canvas_After_profile()
            
            # Establish that it's now created
            
            self.canvas_created_MS_Stages = True
            
        # Create the MS Class
        
        self.initialize_multiStage_model()
        
        
    def MS_canvas_After_profile(self):
        
        """
        Creates the canvas for the Multiple Event Model once the profile
        has already been chosen
        It basically includes a slider for the 'Power Factor'
        """
        
        # Frame for the slider
        
        self.frame_slider = tk.Frame(self.frame_MS)
        self.frame_slider.grid(row=0, column=2)
        self.frame_slider.config(background='white')
        
        # Slider for the power factor
        
        self.label_slider = tk.Label(self.frame_slider,
                                       text="Power Factor",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        self.label_slider.pack()         
        
        self.Scale_slider = tk.Scale(self.frame_slider,
                                        from_ = 0.01,
                                        to = 1, 
                                        digits = 3,
                                        resolution = 0.01,
                                        highlightthickness = 0,
                                        orient = 'horizontal',
                                        length = 200)
        
        self.Scale_slider.bind("<ButtonRelease-1>",
                                  self.reset_power_factor)
        
        # self.Scale_slider.set(self.Rotation_angle)
        
        self.Scale_slider.configure(background='white')

        self.Scale_slider.set(1)  # Set the initial value 
        self.Scale_slider.pack(side = tk.LEFT, pady = 5) 
        
        
    def initialize_multiStage_model(self):
        
        """
        This function creates the Multiple Event Class according to the 
        profile and setup that have been selected
        
        It calls the plotting routines to show the intermediate stages
        """
        
        # Create Class
        
        self.MS_Class = Multi_Stage_Model(self.df_MS, 
                                          self.stage_number,
                                          self.selected_model,
                                          self.Power_factor)
        
        # Call plotting routines
        
        self.plot_all_stages()
        
        
    def plot_all_stages(self):
        
        """
        Creates the canvas in order to plot the intermediate profiles
        and plots them
        
        Call the routines which print the values of the different 
        fitting / fitted parameters
        """
        
        # Define the figure
        
        self.figure_all_stages = Figure(figsize = self.figsize,
                                     dpi = self.dpi)
        
        # Define the canvas where the figure will live        

        self.figure_canvas_stages = FigureCanvasTkAgg(self.figure_all_stages, 
                                                      self.frame_MS_fitted_profile)
        
        # Call the function which does the plot of the intermediate stages
        # and writes it into the figure
        
        Multi_Stage_Model.plot_intermediate_stages(self.MS_Class,
                                                   self.figure_all_stages)
        
        # Create the toolbar, place and configure it
        
        toolbarFrame = tk.Frame(master = self.frame_MS_fitted_profile)
        toolbarFrame.grid(row=1, column=0)
        profile_toolbar = NavigationToolbar2Tk(self.figure_canvas_stages, toolbarFrame)
        profile_toolbar.config(background='white')
        
        # Configure the buttons of the toolbar > White background
        
        for button in profile_toolbar.winfo_children():
            button.config(background='white')
            
        # Place canvas and draw the figure on it
        
        self.figure_canvas_stages.get_tk_widget().grid(row = 0, column = 0 )
        self.figure_canvas_stages.draw()
        
        # Call the parameter printing routine
        
        self.print_MS_parametes()
        
        
    def print_MS_parametes(self):
        
        """
        Prints a 'table' with the values of the different fitted parameters:
            mu
            Sigma_phi_t1
            F
            Sigma_phi_t2 (in case of three events)
            
        Calls the function which asks the user to input the value of some
        of the parameters 
        """
        
        self.frame_param_table = tk.Frame(self.frame_MS)
        self.frame_param_table.grid(row=2, column=0)
        self.frame_param_table.config(background='white')
        
        # Define the table
        
        self.param_table = tk.Text(self.frame_param_table,
                              font = self.letter_type_widgets)
        
        # Get variables to print
        
        list_to_print = self.MS_Class.parameter_values
        
        # Clear possible old data from table
                
        self.param_table.delete("1.0", "end")  
        
        # Insert all parameters into the text object
        
        for x in list_to_print:
            
            self.param_table.insert(tk.END, x + '\n \n')
            
        # Place the table
            
        self.param_table.pack(anchor = 'center')
        
        # Continue with the program
        
        self.introduce_MS_parameters()
        
        
        
    def introduce_MS_parameters(self):
        
        """
        Asks the user to manually input the value of some of the
        parameters in order to calculate the Age (duration) of each stage:
            Sigma_Phi
            F
        """
        
        #------------------------#
        #         Frame          #
        #------------------------#  
        
        ### Create entry frame, with border ###
        
        self.frame_known_params_border = tk.Frame(self.frame_MS)
        self.frame_known_params_border.grid(row=2, column=1)
        self.frame_known_params_border['borderwidth'] = 2
        
        self.frame_known_params = tk.Frame(self.frame_known_params_border)
        self.frame_known_params.grid(row=0, column=0)
        self.frame_known_params.config(background='white')
        
        ### Create sub-frames within it ###
        
        # Sigma_Phi label
        
        self.frame_known_params_sigma_phi_text = tk.Frame(self.frame_known_params)
        self.frame_known_params_sigma_phi_text.grid(row=0, column=0)
        self.frame_known_params_sigma_phi_text.config(background='white')
        
        # Sigma_Phi text
        
        self.frame_known_params_sigma_phi_entry = tk.Frame(self.frame_known_params)
        self.frame_known_params_sigma_phi_entry.grid(row=1, column=0)
        self.frame_known_params_sigma_phi_entry.config(background='white')
        
        # F label
        
        self.frame_known_params_F_text = tk.Frame(self.frame_known_params)
        self.frame_known_params_F_text.grid(row=2, column=0)
        self.frame_known_params_F_text.config(background='white')
        
        # F entry
        
        self.frame_known_params_F_entry = tk.Frame(self.frame_known_params)
        self.frame_known_params_F_entry.grid(row=3, column=0)
        self.frame_known_params_F_entry.config(background='white')
        
        # Calculate button
        
        self.frame_known_params_calculate = tk.Frame(self.frame_known_params)
        self.frame_known_params_calculate.grid(row=4, column=0)
        self.frame_known_params_calculate.config(background='white')
        
        
        #------------------------#
        #         Widgets        #
        #------------------------#  
        
        # Label Sigma Phi
        
        self.label_Sigma_Phi = tk.Label(self.frame_known_params_sigma_phi_text,
                                       text="Introduce Value of Sigma Phi",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        
        self.label_Sigma_Phi.pack(pady = (10, 5), padx= (10, 5), side = tk.LEFT)  
        
        # Info Sigma Phi
        
        self.Info_Sigma_Phi = tk.Button(self.frame_known_params_sigma_phi_text,
                                     text = '?',
                                     command = self.show_Info_Sigma_Phi)
        
        self.Info_Sigma_Phi.pack(side = tk.LEFT)
        self.Info_Sigma_Phi.configure(background='white')
        
        # Entry Sigma Phi
        
        self.Entry_Sigma_Phi = tk.Entry(self.frame_known_params_sigma_phi_entry,
                                  width=10,
                                  textvariable = tk.DoubleVar())
        
        self.Entry_Sigma_Phi.delete(0, tk.END)
        self.Entry_Sigma_Phi.insert(1, self.Initial_guess_Sigma_Phi)
        
        self.Entry_Sigma_Phi.pack(pady = 5, anchor='w')
        
        
        # Label F (Burial Parameter)
        
        self.label_F = tk.Label(self.frame_known_params_F_text,
                                       text="Introduce Value of F",
                                       borderwidth = 0,
                                       background='white',
                                       font = self.letter_type)
        
        self.label_F.pack(pady = (10, 5), padx= (10, 5), side = tk.LEFT)  
        
        # Info Sigma Phi
        
        self.Info_F = tk.Button(self.frame_known_params_F_text,
                                     text = '?',
                                     command = self.show_Info_F)
        
        self.Info_F.pack(side = tk.LEFT)
        self.Info_F.configure(background='white')
        
        # Entry Sigma Phi
        
        self.Entry_F = tk.Entry(self.frame_known_params_F_entry,
                                  width=10,
                                  textvariable = tk.DoubleVar())
        
        self.Entry_F.delete(0, tk.END)
        self.Entry_F.insert(1, self.Initial_guess_F)
        
        self.Entry_F.pack(pady = 5, anchor='w')
        
        
        # Update Button 

        self.Button_Calculate_MS_Age = tk.Button(self.frame_known_params_calculate,
                                    font=self.letter_type_widgets,
                                    text = 'Calculate Individual Event Durations',
                                    command = self.update_MS_age)
        
        self.Button_Calculate_MS_Age.pack(pady=5)
        self.Button_Calculate_MS_Age.configure(background='white')
        
        # If the duration of each stage has been previously calculated
        # we proceed to just update those values with the current
        # parameter values in the entry
        
        if self.Age_calculated == True:
            
            self.update_MS_age()
        

    def update_MS_age(self):
        
        """
        Calculates the duration of each stage based on the values of the 
        fitted parameters and the parameters that are manually introduced
        by the user in the entry
        """
        
        # We get the specified values of Sigma_Phi and F (from the entry)
        
        self.Initial_guess_Sigma_Phi = float( self.Entry_Sigma_Phi.get())
        
        self.Initial_guess_F = float( self.Entry_F.get())
        
        # We get the specified values from the fitted params and their error
        
        Sigma_Phi_te1 = self.MS_Class.params[1]
        Sigma_Phi_te1_err = self.MS_Class.perr[1]
        
        F_Tb1 = self.MS_Class.params[2]
        F_Tb1_err = self.MS_Class.perr[2]
        
        # The duration of each stage is calculated as the fraction:
        
        te1 = Sigma_Phi_te1 / self.Initial_guess_Sigma_Phi

        tb1 = F_Tb1 / self.Initial_guess_F
        
        # We do the same with the error
        
        te1_err = Sigma_Phi_te1_err / self.Initial_guess_Sigma_Phi
        
        tb1_err = F_Tb1_err / self.Initial_guess_F
        
        # We convert everything to years
        
        # te1 = te1 / (3600*24*365.25)
        
        # tb1 = tb1 / (3600*24*365.25)
        
        # te1_err = te1_err / (3600*24*365.25)
        
        # tb1_err = tb1_err / (3600*24*365.25)
        
        # Create the list of params to be printed out later on
        
        self.Ages_to_print = ['1st Exposure Event = {0:.2E} ± {1:.2E} [years]'.format(te1,
                                                                                te1_err),
                              '1st Burial Event = {0:.2E} ± {1:.2E} [years]'.format(tb1,
                                                                                    tb1_err)]
        
        # If three stages, then an additional param has to be calculated

        if self.stage_number == '3':
            
            # Get value of fitted parameter
            
            Sigma_Phi_te2 = self.MS_Class.params[3]
            
            # Get value of the error of the fitted parameter
            
            Sigma_Phi_te2_err = self.MS_Class.perr[3]
            
            # Calculate second exposure event duration and its error
            
            te2 = Sigma_Phi_te2 / self.Initial_guess_Sigma_Phi
            
            te2_err = Sigma_Phi_te2_err / self.Initial_guess_Sigma_Phi
            
            # Convert units to years
            
            # te2 = te2 / (3600*24*365.25)
            
            # te2_err = te2_err / (3600*24*365.25) 
            
            # Include it in the -to print out- list
            
            self.Ages_to_print.append('2nd Exposure Event = {0:.2E} ± {1:.2E} [years]'.format(te2,
                                                                                        te2_err))
            
        # Print the duration (age) of each event
        
        self.print_MS_ages()
        
        
        
    def print_MS_ages(self):
        
        """
        Prints a 'table' with the duration of each event:
            First Exposure Event 
            First Burial Event
            Second Burial Event (in case of three events)
        """
        
        ### Create the frame ###
        
        self.frame_MS_Age = tk.Frame(self.frame_MS)
        self.frame_MS_Age.grid(row=2, column=2)
        self.frame_MS_Age.config(background='white')
        
        
        ### Create the text widget ###
        
        self.Age_table = tk.Text(self.frame_MS_Age,
                              font = self.letter_type_widgets)
        
        # Clean table from potentially the old data
        
        self.Age_table.delete("1.0", "end") 
        
        # Write the -to print- list into the text object
        
        for x in self.Ages_to_print:
            
            self.Age_table.insert(tk.END, x + '\n \n')
            
        # Place the table
            
        self.Age_table.pack()
        
        # Establish that the duration of each event has been calculated
        
        self.Age_calculated = True
        
        
        
    #-----------------------------------------------#
    #           Create and Plot the Profile         #
    #-----------------------------------------------#
        
    def get_new_profile(self, var_to_abbrev):
        
        """
        Establish where to get the profile data from:
            Txt file
            From Image Analysis
            
        Call the corresponding function to read the profile data according
        to the selected option
        """
        
        if self.profile_source == 0:
            
            self.get_profile_from_txt()
            
        elif self.profile_source == 1:
            
            self.get_profile_from_image(var_to_abbrev)               
            
            
    def get_profile_from_txt(self):
        
        """
        Get the right path to the txt data file and load the data to a 
        pandas dataframe
        """
        
        # Check if the Data_Path defined in Main.py exists
        
        if exists(self.Data_path) == False:
            
            # If it doesn't exist, we show a warning and we stablish
            # the home directory as the reference one
            
            self.show_Error_Wrong_Path()
            
            folder_path = expanduser("~")
            
        # If the Data_Path is a file path instead of folder we split it into
        # folder and file
            
        elif isfile(self.Data_path):
            
            head_tail = os.path.split(self.Data_path)
            
            folder_path = head_tail[0]
            
        # Otherwise the path is well defined and we use it
            
        else:
            
            folder_path = self.Data_path
            
        # Open a dialog box to ask the user to choose a file 
        # within the selected directory
        
        filename = filedialog.askopenfilename( title='Select file',
                                              initialdir = folder_path,
                                              filetypes= (("text files","*.txt"),
                                                         ("all files","*.*")))
        
        # Read data from the selected file        

        self.df = pd.read_csv(filename, sep=" ", header=None)
        
        # Check if the Standard Error is in the file (this variable is optional
        # and we show a warning if only two columns exist, meaning that the
        # luminescence signal and depth are contained in the dataset but not
        # the standard error)
        
        if len(self.df.columns) == 2:
            
            self.show_Warning_Missing_SE()
        
        
    def get_profile_from_image(self, var_to_abbrev):
        
        """
        Run the Image Analysis Interface in order to create the luminescence 
        profile from the images and write it to a pandas dataframe
        """
    
        ### Run the ImageAnalysis GUI ### 
            
        Interface = ImageAnalysis_GUI(self.Data_path, var_to_abbrev)
        Interface.mainloop()
        
        self.Data_path = Interface.Data_path
        
        ### Get the profile data ###
        
        # Convert depth array to pandas
        df = pd.DataFrame(Interface.ImageProcess.x * Interface.ImageProcess.layer_thickness * Interface.pixinmm,
                          columns = ['Depth [mm]'])  
        
        # Add luminiscence signal
        df['Normalized Signal'] = pd.DataFrame(Interface.ImageProcess.profile_data)   
        
        # Add standard error             
        df['Standard Error'] = pd.DataFrame(Interface.ImageProcess.standard_error)
        
        # Rename the header for consistency
        
        df.columns = range(df.shape[1])
        
        # Remove rows with NaNs
        
        df.dropna(inplace=True)
        
        self.df = df
        
      
    def initialize_profile_plot(self, frame, df):
        
        """
        Create the plot of the luminescence profile given the dataframe 
        containing its information and the Tk.frame to plot it in
        """
        
        # Split the data into different arrays
        x = df[0].values          # Depth 
        Signal = df[1].values    # Luminiscence signal 
        
        # Check if the Standard error of the signal is in the dataframe
        
        if len(df.columns) == 3:
            SE = df[2].values            
        else:
            SE = 'None'
            
        # Define the figure and its canvas
        
        self.figure_profile = Figure(figsize = self.figsize,
                                     dpi = self.dpi)
        
        self.figure_canvas_profile = FigureCanvasTkAgg(self.figure_profile, frame)
        
        # Create the ProfileAnalysis object (this function is imported)
        
        self.ProfileAnalysis = ProfileAnalysis(Signal,
                                               SE, 
                                               x,
                                               self.figure_profile,
                                               'Luminescence Profile')
               
        # Create the toolbar
        toolbarFrame = tk.Frame(master = frame)
        toolbarFrame.grid(row = 3, column = 0)
        profile_toolbar = NavigationToolbar2Tk(self.figure_canvas_profile, toolbarFrame)
        profile_toolbar.config(background='white')
        
        # Configure its buttons 
        
        for button in profile_toolbar.winfo_children():
            button.config(background='white')
            
        # Place the canvas of the figure within the frame
        
        self.figure_canvas_profile.get_tk_widget().grid(row = 2, column = 0 )
        self.figure_canvas_profile.draw()
        
        
    #-----------------------------------------------#
    #               Reset Setup Values              #
    #-----------------------------------------------#  
  
        
    def reset_Model(self, value):

        """
        Establish the model to be used:
            1 Event Model
            2/3 Event Model
            
        This function runs when the user chooses any of the two possibilities
        in the initial menu
        """
        
        if value == 0:
            
            self.stage_number = '1'
            
        elif value == 1:
            
            # Note: we assign the variable the value of '2' but it actually
            # represent the MS model (a bit missleading)
            
            self.stage_number = '2'
            
            
        #------------------------#
        #        One Event       #
        #------------------------#  
        
        
    def reset_profile_model_fit_1s(self, event):
        
        """
        Reset the value of the Order for the One Event Model:
            First Order
            Second Order
        """
        
        self.selected_model = event
        
        self.n_model = select_model(self.selected_model) 
        
        
    def reset_iteration(self, event):
        
        """
        Reset the value of the amount of iterations of the fitting for the 
        One Stage Mode
        Update the analysis accordingly
        """
        
        self.n_iterations = event.widget.get()
        
        # Plots to update
        
        self.initialize_model_fit_cal()
        
        
    def reset_mu(self, value):
        
        """
        Reset the mu value that is used for the dating sample of the One
        Event Model. This parameter can take the following values:
            Mu from Calibration Sample
            Mu from Dating Sample
        """
                
        if value == 0:
            
            # Use the Mu from the Calibration Sample
            
            self.mu = 'None'
            self.mu_error = None
            
        elif value == 1:
            
            # Use the Mu from the Dating Sample itself
            
            self.mu = self.DATING_SAMPLE.mu_median
            self.mu_error = self.DATING_SAMPLE.mu_1s_errors[0]
        
        # Plots to update
        
        self.calculate_age()
        
        
    def reset_power_factor(self, event):
        
        """
        Reset the value of the 'Power Factor' used for the function fitting
        in the Multiple Event Model
        Update the Model according to this new value
        """
               
        self.Power_factor = event.widget.get()
        
        self.initialize_multiStage_model()
        
        
    #------------------------#
    #      Multi Events      #
    #------------------------#  
        
        
    def reset_profile_model_fit_MS(self, event):
        
        """
        Reset the value of the Order for the Multiple Event Model:
            First Order
            Second Order
        """
        
        
        self.selected_model = event
        
        self.n_model = select_model(self.selected_model) 
          
    
    def reset_stage_number(self, event):
        
        """
        Reset the number of stages for the Multiple Event Model:
            Two Events
            Three Events
        """
        
        self.stage_number = event
        
        
        
    #-----------------------------------------------#
    #             Define the Info Boxes             #
    #-----------------------------------------------#  
    
    def show_Error_Wrong_Path(self):        
    
        tk.messagebox.showwarning(title = 'Missing path!', 
                               message = 'Be aware that the introduced data path'
                               ' does not exist! \n \n'
                               '{} \n \n The home directory will be used instead.'.format(self.Data_path))
    
    
    def show_Warning_Missing_SE(self):        
    
        tk.messagebox.showwarning(title = 'Warning!', 
                               message = 'Be aware that the Standard Error is'
                               ' missing in this file!!')
    
    def show_Warning_Method(self):        
    
        tk.messagebox.showwarning(title = 'Keep in mind that...', 
                               message = 'Make sure that the method that has'
                               ' been used to obtain the profile is the same'
                               ' for the calibration and dating sample')
    
    def show_Warning_Stages(self):        
    
        tk.messagebox.showwarning(title = 'Keep in mind that', 
                               message = 'Careful, since a multi-stage model has been'
                               ' chosen the algorithm used for model fitting'
                               ' has been accordingly changed!')

    def show_Info_Choose_Profile(self):
        
        tk.messagebox.showinfo(title = 'Choices for the Profile Selection', 
                               message = 'The profile can be chosen via two different'
                               ' methods: \n \n'
                               '1- Through an already existing table stored in a txt file. \n \n'
                               '2- Via Image Analysis')
        
    def show_Info_Number_Stages(self):
        
        tk.messagebox.showinfo(title = 'Stage Number', 
                               message = 'The stage number defines the amount of'
                               ' different stages that the program will assume'
                               ' when fitting the model. \n \n'
                               ' It is always assumed that the profile was initially'
                               ' totally saturated. \n \n'
                               ' 1 stage would correspond to just one exposure event. \n \n'
                               ' 2 stages represents an exposure followed by a burial event \n \n'
                               ' 3 stages includes an additional exposure event after the burial \n \n'
                               ' *Note: Depending on the amount of stages that is chosen'
                               ' a different method is followed by the program for the'
                               ' fitting process!')
        
    def show_Info_Order(self):
        
        tk.messagebox.showinfo(title = 'Model Order', 
                               message = 'The equation that describes the exposure can be derived'
                               ' under different assumptions, leading to a different equation \n \n')
    
    def show_Info_Calibration_Age(self):
        
        tk.messagebox.showinfo(title = 'Age of the Calibration Sample', 
                               message = 'The age of the calibration sample'
                               ' is necessary in order to estimate the value of'
                               ' the detrapping rate constant (sigma phi)')
    

    def show_Info_Iterations(self):
        
        tk.messagebox.showinfo(title = 'Resolution', 
                               message = 'This parameter defines the amount'
                               'points into which the domain is splited \n \n'
                               ' As it increases the resolution increases as well'
                               ' as the computation time.')
    
    def show_Info_Forced_Mu(self):
        
        tk.messagebox.showinfo(title = 'Forced Mu?', 
                               message = 'The value for this parameter can be'
                               ' taken either from the one calculated from the'
                               ' calibration sample or from the dating sample itself.')
        
    def show_Info_Sigma_Phi(self):
        
        tk.messagebox.showinfo(title = 'Forced Mu?', 
                               message = 'The value for this parameter can be'
                               ' taken either from the one calculated from the'
                               ' calibration sample or from the dating sample itself.')
        
    
    def show_Info_F(self):
        
        tk.messagebox.showinfo(title = 'Forced Mu?', 
                               message = 'The value for this parameter can be'
                               ' taken either from the one calculated from the'
                               ' calibration sample or from the dating sample itself.')
        
        
    def show_Info_Model(self):

        tk.messagebox.showinfo(title = 'Model Choices', 
                               message = 'Two different models are available:'
                               '\n \n 1. One Event Model'
                               '\n \n 2. Multiple Event Model')