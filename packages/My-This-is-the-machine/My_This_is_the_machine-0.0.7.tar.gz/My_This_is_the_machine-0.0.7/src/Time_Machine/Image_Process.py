#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:30:40 2022

@author: gorosti
"""
                                                           
import numpy as np          # Numpy
import imreg                # For image registration
import tifffile             # Read tif files
import cv2                  # For some of the image processing functions
import os                   # For path manipulation
from os.path import exists
import warnings             # Allows to customize warnings


class ImageProcess():      
        
        def get_file_names(self):
            """
            Finds the full name of the files of interest
        
            Arguments:
            Data_path: string containing absolute path to data folder
            var_to_abbrev: dictionary containing the string that should be 
                included within the name of the file for each of the variables
        
            Returns
            var_to_full: dictionary containing the full name of the file for each variable
            """ 
            Data_path = self.Data_path
            var_to_abbrev = self.var_to_abbrev
            
            # We extract the strings we have to look for
            Name_list = list( var_to_abbrev.values())
        
            # We create two empty lists
            files_abbrev = []
            files_full = []
            
            
            for j in Name_list:                     # Iterate over all the strings we have to look for
                        
                if exists( os.path.join( Data_path, j )) == True:
                    
                    files_full.append( os.path.join( Data_path, j ))        # Append file name
                    files_abbrev.append(j)      # Append string name
                    
                else:
                    
                    for i in os.listdir(Data_path):     # Iterate over all the file names within the "Data_path" directory
                        if j in i:                      # If the string is contained in the file name
                            files_full.append(i)        # Append file name
                            files_abbrev.append(j)      # Append string name
                        
            # print(files_full)
            # print(files_abbrev)
            
            # Ideally each string has to be foung be found only 
            # in one file (otherwise each variable would come from two files)
            # We can create a list with the repeated strings
            # (should be empty if everything is fine)
            repeated_names = list(set([x for x in files_abbrev if files_abbrev.count(x) > 1]))
            
            # print(repeated_names)
                        
            if ( len(repeated_names) > 0):                  # If there are repeated strings we raise a warning
                warnings.warn(" There is more than one file containing the string --{0}-- on "
                              "its file name in the {1} folder".format(repeated_names, Data_path) ) 
            else:
                abbrev_to_full = dict( zip( files_abbrev, files_full))      # We create a dictionary relating strings to full names
                
            # We combine two dictinoaries to create a 3rd one (var_to_full) which contains the name of the file of each variables    
            var_to_full = {k:abbrev_to_full[v] for k,v in var_to_abbrev.items() if v in abbrev_to_full}
            
            self.var_to_full = var_to_full
            
            
        def read_file_cv2(self, var, Rotation_angle = 0):
            """
            Reads with opencv a tiff file

            Arguments:
            Data_path: string containing absolute path to data folder
            var_to_abbrev: dictionary containing the string that should be included within the name of the file for each of the variables
            var_to_full: dictionary containing the full name of the file for each variable

            Returns
            image
            """ 
            
            Data_path = self.Data_path
            var_to_full = self.var_to_full
            var_to_abbrev = self.var_to_abbrev
            
            if var in var_to_full:                                                # If the file containing this variable has been found
                path_to_image = os.path.join(Data_path, var_to_full.get(var) )    # Full path of file = "data_path" + "full_name"
                image = cv2.imread(path_to_image)                                 # Read using opencv
            else:
                warnings.warn(" \n \n There is no file containing the string --{0}--on its "
                              "file name in the {1} folder".format( var_to_abbrev.get(var), Data_path ))
                
            if Rotation_angle != False:       # The Rotation angle has already been specified
            
                height, width = image.shape[:2]
                rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), Rotation_angle, 1)
                image = cv2.warpAffine(image, rotation_matrix, (width, height))
            
            return image
            
            
        def read_file_tiff(self, var, Rotation_angle = 0):
            """
            Reads with opencv a tiff file

            Arguments:
            Data_path: string containing absolute path to data folder
            var_to_abbrev: dictionary containing the string that should be included within the name of the file for each of the variables
            var_to_full: dictionary containing the full name of the file for each variable

            Returns
            image
            """ 
            
            Data_path = self.Data_path
            var_to_full = self.var_to_full
            var_to_abbrev = self.var_to_abbrev
            
            
            if var in var_to_full:                                                # If the file containing this variable has been found
                path_to_image = os.path.join(Data_path, var_to_full.get(var) )    # Full path of file = "data_path" + "full_name"
                image = tifffile.imread( path_to_image)                           # Read using opencv
            else:
                warnings.warn(" \n \n There is no file containing the string --{0}--on its "
                              "file name in the {1} folder".format( var_to_abbrev.get(var), Data_path ))
                
            if Rotation_angle != False:       # The Rotation angle has already been specified
            
                height, width = image.shape[:2]
                rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), Rotation_angle, 1)
                image = cv2.warpAffine(image, rotation_matrix, (width, height))
            
            return image
        
        
        
        
        def find_missing_variables(self):
        
            Calculation_Method = self.calculation_method
            
            self.missing_variables = []
            
            if 'Ln_optical' not in self.var_to_full.keys():
                self.missing_variables.append('Ln_optical')
        
            if (Calculation_Method == 0):
                
                if 'Ln_880' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_880')
                
            elif (Calculation_Method == 1):
                
                if 'Ln_955' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_955')
                
            elif (Calculation_Method == 2):
                
                if 'Ln_880' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_880')
                    
                if 'Ln_955' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_955')
                
            elif (Calculation_Method == 3):
                
                if 'Ln_880' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_880')
                    
                if 'Lx_880' not in self.var_to_full.keys():
                    self.missing_variables.append('Lx_880')

            elif (Calculation_Method == 4):
                
                if 'Ln_955' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_955')
                    
                if 'Lx_955' not in self.var_to_full.keys():
                    self.missing_variables.append('Lx_955')
                
            elif (Calculation_Method == 5):
                
                if 'Ln_880' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_880')
                    
                if 'Lx_880' not in self.var_to_full.keys():
                    self.missing_variables.append('Lx_880')

            elif (Calculation_Method == 6):
                
                if 'Ln_955' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_955')
                    
                if 'Lx_955' not in self.var_to_full.keys():
                    self.missing_variables.append('Lx_955')

            elif (Calculation_Method == 7):
                
                if 'Ln_880' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_880')
                    
                if 'Ln_880_after' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_880_after')
                
            elif (Calculation_Method == 8):
                
                if 'Ln_955' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_955')
                    
                if 'Ln_955_after' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_955_after')
                
            elif (Calculation_Method == 9):
                
                if 'Ln_I' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_I')
                
            elif (Calculation_Method == 10):
                
                if 'Ln_I' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_I')
                
            elif (Calculation_Method == 11):
                
                if 'Ln_I' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_I')
                    
                if 'Lx_I' not in self.var_to_full.keys():
                    self.missing_variables.append('Lx_I')

            elif (Calculation_Method == 12):
                
                if 'Ln_I' not in self.var_to_full.keys():
                    self.missing_variables.append('Ln_I')
                    
                if 'Lx_I' not in self.var_to_full.keys():
                    self.missing_variables.append('Lx_I')
          
            
        def choose_calculation(self):
        
            Calculation_Method = self.calculation_method
            Rotation_angle = self.Rotation_angle
            
            Need_to_rotate = False
            
            # Defines the calculation matrix with the method that was set up in the "INPUT PARAMETER SECTION"
        
            if (Calculation_Method == 0):
                
                irpl880 = self.read_file_tiff('Ln_880', Rotation_angle)
                self.calculation_original = irpl880
                self.image_for_mask = irpl880
                
            elif (Calculation_Method == 1):
                
                irpl955 = self.read_file_tiff('Ln_955', Rotation_angle)
                self.calculation_original = irpl955
                self.image_for_mask = irpl955
                
            elif (Calculation_Method == 2):
                
                irpl880 = self.read_file_tiff('Ln_880', Rotation_angle)
                irpl955 = self.read_file_tiff('Ln_955', Rotation_angle)
                with np.errstate(divide='ignore', invalid='ignore'):
                    self.calculation_original = irpl955 / irpl880
                self.image_for_mask = irpl955
                
            elif (Calculation_Method == 3):
                
                irpl880 =  self.read_file_tiff('Ln_880', Rotation_angle)
                irpl880_lx =  self.read_file_tiff('Lx_880', Rotation_angle)
                irpl880_lx_reg, scale, angle, (t0, t1) = imreg.similarity(irpl880, irpl880_lx)    #  Image Registration
                self.calculation_original = irpl880_lx_reg
                self.image_for_mask = irpl880
                
            elif (Calculation_Method == 4):
                
                irpl955 =  self.read_file_tiff('Ln_955', Rotation_angle)
                irpl955_lx =  self.read_file_tiff('Lx_955', Rotation_angle)
                irpl955_lx_reg, scale, angle, (t0, t1) = imreg.similarity(irpl955, irpl955_lx)    #  Image Registration
                self.calculation_original = irpl955_lx_reg
                self.image_for_mask = irpl955_lx_reg
                
            elif (Calculation_Method == 5):

                irpl880 =  self.read_file_tiff('Ln_880', Rotation_angle)
                irpl880_lx =  self.read_file_tiff('Lx_880', Rotation_angle)
                irpl880_lx_reg, scale, angle, (t0, t1) = imreg.similarity(irpl880, irpl880_lx)    #  Image Registration
                
                #irpl880_lx_reg = image_registration(Data_path, var_to_full, var_to_abbrev, 'Lx_8', 'Ln_8', Rotation_angle)
                with np.errstate(divide='ignore', invalid='ignore'):
                    self.calculation_original = irpl880 / irpl880_lx_reg
                self.image_for_mask = irpl880
            
            elif (Calculation_Method == 6):
                
                irpl955 =  self.read_file_tiff('Ln_955', Rotation_angle)
                irpl955_lx =  self.read_file_tiff('Lx_955', Rotation_angle-90)
                irpl955_lx_reg, scale, angle, (t0, t1) = imreg.similarity(irpl955, irpl955_lx)    #  Image Registration        
                with np.errstate(divide='ignore', invalid='ignore'):
                    self.calculation_original = irpl955 / irpl955_lx_reg
                self.image_for_mask = irpl955
                
            elif (Calculation_Method == 7):
                
                irpl880 =  self.read_file_tiff('Ln_880', Rotation_angle)           
                irpl880_af_IRSL = self.read_file_tiff('Ln_880_after', Rotation_angle)    
                
                with np.errstate(divide='ignore', invalid='ignore'):
                    self.calculation_original = (irpl880 - irpl880_af_IRSL) / irpl880
                self.image_for_mask = irpl880 - irpl880_af_IRSL
                
            elif (Calculation_Method == 8):
                
                irpl955 =  self.read_file_tiff('Ln_955', Rotation_angle)
                irpl955_af_IRSL = self.read_file_tiff('Ln_955_after', Rotation_angle) 
                
                with np.errstate(divide='ignore', invalid='ignore'):
                    self.calculation_original = (irpl955 - irpl955_af_IRSL) / irpl955
                self.image_for_mask = irpl955 - irpl955_af_IRSL
            
            elif (Calculation_Method == 9):
                
                irsl =  self.read_file_tiff('Ln_I')
                irsl0 = irsl[0,:,:]
                calculation = irsl0
                height, width = calculation.shape[:2]
                image_for_contour = self.read_file_tiff('Ln_optical', Rotation_angle)
                
                Rotation_vector = np.linspace(0, 0, 1)
                Mirror_vector = [0, 1, 2, 3]
                sse = 0
                for Rotation_angle_loop in Rotation_vector:
                    
                    for Mirror in Mirror_vector:
                        
                        irsl0 = irsl[0,:,:]
                        
                        if Mirror == 1:
                            irsl0 = np.flip(irsl[0,:,:], 1)
                            
                        if Mirror == 2:
                            irsl0 = np.flip(irsl[0,:,:], 0)
                            
                        if Mirror == 3:
                            irsl0 = np.flip(irsl[0,:,:], 0)
                            irsl0 = np.flip(irsl0, 1)
                            
                        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), Rotation_angle_loop, 1)
                        irsl0 = cv2.warpAffine(irsl0, rotation_matrix, (width, height))
                        irsl_reg, scale, angle, (t0, t1) = imreg.similarity(image_for_contour, irsl0)    #  Image Registration
                        #irsl_reg = image_registration_2(image_for_contour, irsl0)
                        sse_new = sum( sum( (image_for_contour - irsl_reg)^2 ))
                        sse_new = sum( sum( (image_for_contour * irsl_reg) ))
                        
                        if sse_new > sse:
                            
                            calculation = irsl_reg
                            sse = sse_new
                            
                self.calculation_original = calculation.copy()
                self.image_for_mask = calculation
                #plt.imshow(calculation)
                Need_to_rotate = False
                
            elif (Calculation_Method == 10):
                
                irsl =  self.read_file_tiff('Ln_I')
                self.calculation_original = irsl[0,:,:] / irsl[4,:,:]
                self.image_for_mask =  irsl[0,:,:] 
                Need_to_rotate = True
                
            elif (Calculation_Method == 11):
                
                irsl = self.read_file_tiff('Ln_I')
                irsl_lx =  self.read_file_tiff('Lx_I', Rotation_angle)
                irsl_lx_reg, scale, angle, (t0, t1) = imreg.similarity(irsl[0,:,:], irsl_lx[0,:,:])
                
                with np.errstate(divide='ignore', invalid='ignore'):
                    self.calculation_original = irsl[0,:,:] / irsl_lx_reg
                self.image_for_mask = irsl[0,:,:] 
                Need_to_rotate = True
                
            elif (Calculation_Method == 12):
                
                irsl =  self.read_file_tiff('Ln_I')
                irsl_lx =  self.read_file_tiff('Lx_I', Rotation_angle)
                irsl_lx_reg, scale, angle, (t0, t1) = imreg.similarity(irsl[0,:,:], irsl_lx[0,:,:])
                self.calculation_original = irsl_lx_reg
                self.image_for_mask = self.calculation_original.copy()
                Need_to_rotate = True
            
            if Rotation_angle != False and Need_to_rotate == True:       # The Rotation angle has already been specified
               
                height, width = self.calculation.shape[:2]
                rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), Rotation_angle, 1)
                self.calculation_original = cv2.warpAffine(self.calculation, rotation_matrix, (width, height))
                self.image_for_mask = cv2.warpAffine(self.image_for_mask, rotation_matrix, (width, height))
                
                
        def create_mask(self, image_for_mask, histogram_cut, layer_mask = False):
            """
            Masks the image
        
            Arguments:
            image_for_mask: image from which the mask has to be created. RGB is expected
            threshold: Parameter that defines the limit for masking
        
            Returns
            mask: binary matrix containing the mask
            """ 
            
            
            if len(image_for_mask.shape) == 3:    # If image is in RGB
                img_gray = cv2.cvtColor(image_for_mask, cv2.COLOR_BGR2GRAY)              # We convert the image to grey
            else:
                img_gray = image_for_mask.copy()
                
            threshold = np.nanpercentile(img_gray, histogram_cut)  # Define the threshold for masking
            
            if type(layer_mask) != bool:
                
                auxiliar = img_gray.astype('float64')
                auxiliar[ np.isnan(layer_mask)] = np.nan
                threshold = np.nanpercentile(auxiliar, histogram_cut)  # Define the threshold for masking
                img_gray[ np.isnan(layer_mask)] = 0
                
                # Binarize (mask) the image with the given threshold
                th, mask = cv2.threshold(img_gray, threshold, 1, cv2.THRESH_BINARY)  
                mask = mask.astype('float64')
                mask = (mask - 1) * (-1)
                mask[np.isnan(layer_mask)] = np.nan
                
            else:
                
                th, mask = cv2.threshold(img_gray, threshold, 1, cv2.THRESH_BINARY)
            
            return mask
                
                
        def create_contour(self):
            """
            Finds the contour containing the rock
        
            Arguments:
            image_for_mask: image from which the contour has to be created. RGB is expected
            threshold: Parameter that defines the limit for the contour
            Smooth_factor: Parameter that defines how much the found contour is smoothened
        
            Returns
            image_with_contour: image with the contour already drawn
            biggest_contour: contour containing the rock
            """ 
        
            image_for_contour = self.image_for_contour
            histogram_cut = self.histogram_cut_contour
            Smooth_factor = self.Smooth_factor
            
            mask_for_contour = self.create_mask(image_for_contour, histogram_cut)       # We create a mask for the image
                        
            # Detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
            contours, hierarchy = cv2.findContours(image=mask_for_contour,
                                                   mode=cv2.RETR_TREE,
                                                   method=cv2.CHAIN_APPROX_SIMPLE)
        
            # Diffent contours can be found, to get the one containing the rock the we choose the one that enclosest the biggest area
            contours_sizes= [(cv2.contourArea(cnt), cnt) for cnt in contours]
            biggest_contour = max(contours_sizes, key=lambda x: x[0])[1]
            
            my_contour = biggest_contour
            
            if Smooth_factor != 0:   # Smoothen the contour
                
                image_length = image_for_contour.shape[0]
                source_image = np.zeros((image_length, image_length))      # create a single channel black image 
        
                cv2.fillPoly(source_image, pts = [biggest_contour], color=(255,255,255))  # Fill th534e image with the area inside the contour
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (Smooth_factor, Smooth_factor))
        
                dilated_image = cv2.dilate( source_image, kernel, cv2.BORDER_REFLECT)
                eroded_image = cv2.erode( dilated_image, kernel, cv2.BORDER_REFLECT) 
                eroded_image = eroded_image.astype('uint8')
                my_contour, hierarchy = cv2.findContours(image=eroded_image,
                                                       mode=cv2.RETR_TREE, 
                                                       method=cv2.CHAIN_APPROX_SIMPLE)
                # Diffent contours can be found, to get the one containing the rock the we choose the one that enclosest the biggest area
                contours_sizes= [(cv2.contourArea(cnt), cnt) for cnt in my_contour]
                biggest_contour = max(contours_sizes, key=lambda x: x[0])[1]
                   
            # Draw contours on the original image
            image_with_contour = image_for_contour.copy()
            cv2.drawContours(image=image_with_contour, contours=my_contour,
                             contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
            
            self.image_with_contour = image_with_contour
            self.biggest_contour = biggest_contour
            
            
        def create_layers(self):
            """
            Creates different depth layers starting from the contour

            Arguments:
            biggest_contour: contour enclosing the rock

            Returns
            layer_mask: matrix containing the layer to which each pixel belongs to
            """ 
            
            biggest_contour = self.biggest_contour
            image_for_contour = self.image_for_contour
            layer_thickness = self.layer_thickness
            layering_Method = self.layering_Method
            
            image_length = image_for_contour.shape[0]

            source_image = np.zeros((image_length, image_length))      # create a single channel black image 
            layer_mask = np.empty((image_length,image_length))         # create a single channel black image
            layer_mask[:] = np.NaN
            source_image.astype('uint8')
            cv2.fillPoly(source_image, pts = [biggest_contour], color=(255,255,255))          # Fill the image with the area inside the contour
            
            # Smoothen it
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
            # dilated_image = cv2.dilate( source_image, kernel, cv2.BORDER_REFLECT)
            # source_image = cv2.erode( source_image, kernel, cv2.BORDER_REFLECT) 
            
            # Create kernel (defines how each layer is calculated) 
            if layering_Method == 1:
                kernel = np.zeros((1, 2*layer_thickness+1) ).astype('uint8')  # Move left to right
                kernel[0, 0:layer_thickness+1] = 1
            elif layering_Method == 2:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                               (2*layer_thickness+1, 2*layer_thickness+1)) # In this case we choose an ellipse
                
            # eroded_image = cv2.erode( source_image, kernel, cv2.BORDER_REFLECT)
            # dilated_image = cv2.dilate( source_image, kernel, cv2.BORDER_REFLECT)
            # new_layer = dilated_image - source_image
            # layer_mask[ new_layer > 0 ] = 0
            
            i = 1
            while sum(sum( source_image )) > 0:    # We iterate while the image is not empty

                # We erode (shrink) the source image that we had 
                eroded_image = cv2.erode( source_image, kernel, cv2.BORDER_REFLECT)    

                # We calculate the new layer as the difference in between the source image and the eroded one
                new_layer = source_image - eroded_image        

                # The eroded image will be the source image for the next iteration step
                source_image = eroded_image

                # We write the layer number on the pixels contained within the layer 
                layer_mask[ new_layer > 0 ] = i     

                i += 1
            
            self.layer_mask = layer_mask
            
            
        def make_calculation(self):
            """
            Creates the calculation taking into account the mask

            Arguments:
            calculation: matrix with the intensity values
            mask: binary mask previously defined

            Returns
            calculation: after some processing and by multiplying with the mask
            """ 
            
            calculation = self.calculation_original.copy()
            mask = self.mask.copy()
            layer_mask = self.layer_mask.copy()
            
            calculation = calculation.astype('float64')      # Just some conversion
            calculation[calculation == np.inf ] = np.nan     # We set the Inf values to Nan
            calculation = calculation * mask                 # Multiply with the mask
            calculation = calculation / np.nanmax(calculation)  # Reescale
            
            calculation[ np.isnan(layer_mask)] = np.nan      # Delete everythin ourside
         
            self.calculation = calculation
            
            
        def select_ROI(self):
            """
            Creates the Region Of Interest (ROI) by dragging with the mouse
        
            Arguments:
            image_ROI: image from which the ROI is selected
        
            Returns
            roi: contains the 2 coordinates of a corner of the rectange plus height and width
            """ 
            
            image_ROI = self.calculation
            biggest_contour = self.biggest_contour
            
            image = image_ROI.copy()
            image /= np.nanmax(image)
            
            cv2.drawContours(image=image, contours=biggest_contour, contourIdx=-1, 
                             color=1, thickness=2, lineType=cv2.LINE_AA)
            
            
            roi = cv2.selectROI('Drag Rectangle with Mouse and press Enter',
                                image, False, False)     # Plots the image on screen so that you can select the RIO
            cv2.destroyWindow('Drag Rectangle with Mouse and press Enter')                            # Destroy the plot that poped out on the previus command

            self.roi = roi
            
            
        def make_profile(self):
            """
            Calculates the profile as function of depth
        
            Arguments:
            calculation: already with the mask applied
            roi: region of interest
            layer_mask: tells to which layer each pixel belongs to
        
            Returns
            profile_data: profile by layer averaging (by using the layer mask)
            """ 
            
            calculation = self.calculation.copy()
            roi = self.roi
            layer_mask = self.layer_mask.copy()
            
            calculation_aux = calculation[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]      # We only care about the ROI section
            layer_mask_aux = layer_mask[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]        # Take only its ROI section
            
            calculation_aux[ np.isnan(calculation_aux)] = 0
            layer_mask_aux[ np.isnan(layer_mask_aux)] = 0
            
            layer_mask_aux = layer_mask_aux.astype(int)                                # Change type
            profile_data = np.zeros(( np.max(layer_mask_aux) ))                        # Initialize array
            standard_error = np.zeros(( np.max(layer_mask_aux) ))                      # Initialize array
            
            
            if len(profile_data) == 0:
                
                self.profile_data = profile_data.copy()
                self.standard_error = standard_error.copy()
                
                self.profile_data[:] = 0
                self.standard_error[:] = 0
                
            else:              
        
                # Iterate over each layer
                for i in range( len(profile_data )):   
                    
                    my_mask = layer_mask_aux == i+1                            # We create a boolan matrix containing the pixels that are within the i layer
                    product = np.nansum(np.nansum(calculation_aux * my_mask )) # Add all the values within this layer
                    standard_error[i] = np.nanstd(calculation_aux * my_mask)
                    non_zero = np.count_nonzero(calculation_aux * my_mask)     # We count how many pixels are not zero within the i layer
                    with np.errstate(divide='ignore', invalid='ignore'):
                        profile_data[i] = product / non_zero                       # Calculate mean for i-th layer
                  
                profile_data = profile_data - np.nanmin(profile_data)  # Set offset to zero
                value_100 = np.nanpercentile(profile_data, 60)          # We consider the plateau is at the 90% of the distribution
                profile_data = profile_data / value_100                 # Normalize it to the 'plateau' as defined in the previous step
                profile_data[0] = profile_data[1]
                standard_error = standard_error / value_100             # Normalize it
                
                self.profile_data = profile_data
                self.standard_error = standard_error
                self.x = np.linspace(0.5 , len(self.profile_data), len(self.profile_data)) * self.pixinmm * self.layer_thickness  # Depth vector 
                    
        
        def __init__(self, Calculation_Method, Data_path, 
                     var_to_abbrev, Rotation_angle, histogram_cut_contour,
                     Smooth_factor, histogram_cut_mask,
                     layer_thickness, layering_Method,
                     pixinmm, roi):
                
            self.calculation_method = Calculation_Method
            self.Data_path = Data_path
            self.var_to_abbrev = var_to_abbrev
            self.Rotation_angle = Rotation_angle
            self.histogram_cut_contour = histogram_cut_contour
            self.Smooth_factor = Smooth_factor
            self.histogram_cut_mask = histogram_cut_mask
            
            self.layer_thickness = layer_thickness
            self.layering_Method = layering_Method
            
            self.pixinmm = pixinmm
            
            self.roi = roi
                        
            
            # Call various methods
            
            self.get_file_names()
            
            self.find_missing_variables()
            
            if len(self.missing_variables) == 0:
                
                self.choose_calculation()
            
                self.image_for_contour = self.read_file_cv2('Ln_optical', Rotation_angle)
                
                self.create_contour()
                
                self.create_layers()
                
                self.mask = self.create_mask(self.image_for_mask, self.histogram_cut_mask,
                                             self.layer_mask )
                
                self.make_calculation()
                
                self.make_profile()
