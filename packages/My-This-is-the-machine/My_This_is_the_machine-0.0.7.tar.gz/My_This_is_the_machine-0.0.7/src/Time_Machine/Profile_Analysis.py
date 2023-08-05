#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 13:35:34 2022

@author: gorosti
"""
                                                           
import numpy as np                                         # Numpy
import warnings                                            # Allows to customize warnings
from scipy.signal import savgol_filter
import scipy.optimize



class ProfileAnalysis():   
    
    def __init__(self, profile_data, standard_error, x, figure_profile, tt):
        
        self.profile_data = profile_data
        self.standard_error = standard_error
        self.x = x 
        self.plot_title = tt
        
        self.figure_profile = figure_profile
        self.axes_profile = self.figure_profile.add_subplot()
        
        
        self.get_half_life_depth()
        
        # self.fit_model()
        
        self.plot_profile()
        

        
    def get_half_life_depth(self, life_threshold = 0.5):
        """
        Calculates the depth at which a given amount of luminiscense (default to 0) is reached

        Arguments:
        x: vector containig the depth [mm]
        profile_data: vector containing the luminiscence signal for each depth
        life_threshold: amount of signal we want to look for (0.5 by default)

        Returns
        Half_lum_depth: depth at which the "life_threshold" amount of signal is reached
        """ 
        x = self.x.copy()
        
        self.smoothen_profile()
        
        profile_without_nan = self.Smooth_signal.copy()                               # We make a copy
        
        profile_without_nan[np.isnan(profile_without_nan)] = 0                  # We convert NaNs to zeros

        position_of_half_lifetime = np.argmax(profile_without_nan > life_threshold)   # Get position we the signal exceeds "life_threshold"

        # Linear regresion  
        fraction = ((0.5 - profile_without_nan[position_of_half_lifetime - 1] )  /
            ( profile_without_nan[position_of_half_lifetime] - profile_without_nan[position_of_half_lifetime - 1]))

        Half_lum_depth = ( x[position_of_half_lifetime - 1] + fraction * 
                      (x[position_of_half_lifetime] - x[position_of_half_lifetime - 1]))
        
        self.Half_lum_depth = Half_lum_depth
        
    
    def smoothen_profile(self):
        """
        Smoothen the luminiscence profile by using a filter

        Arguments:
        x: vector containig the depth [mm]

        Returns
        Smooth_signal: Luminiscence profile after the filter is applied
        """
        profile_data = self.profile_data.copy()

        
        averaging_window = len(profile_data) / 10                    # Amount of points per window
        averaging_window = np.ceil(averaging_window) // 2 * 2 + 1    # Convert it to an odd number
        averaging_window = int(averaging_window)                     # Convert it to an integer

        filter_order = np.minimum(3, averaging_window - 1)          # We use a cubic polynomial to fit it
        
        # Remove the Nan values
        profile_data[np.isnan(profile_data)] = 0
        # profile_data_no_Nan = profile_data[np.logical_not(np.isnan(profile_data))]
        
        
        Smooth_signal = savgol_filter(profile_data,
                                      averaging_window,
                                      filter_order)                  # Apply the filter (3 is for the order)
        
        self.Smooth_signal = Smooth_signal
        
            
        # High order model
    def n_m(self, x, mu, sigma_phi_t):
        
        n_i = 1
        g = 2   
        my_function = ((g-1) * sigma_phi_t * np.exp(-mu*x) + n_i**(1-g)) ** (1 / (1-g))
        
        return my_function
        
        
    def fit_model(self):
        """
        Fits the model to the profile using the function defined in n_m

        Arguments:
        x: vector containig the depth [mm]
        profile_data: vector containing the luminiscence signal for each depth
        n_m: function which we want to fit to the data
        
        Returns
        mu: 
        sigma_phi_t: 
        rSquared: R-squared from the fit
        """
        
        x = self.x.copy()
        Signal = self.profile_data.copy()
                
        Signal[np.isnan(Signal)] = 0
        
        p0 = (1, 10e-4)                                    # Initial guess for the values (mu and sigma_phi respectively)
        
        # x = np.array(x, dtype=np.float128)
        # Signal = np.array(Signal, dtype=np.float128)
        
        warnings.filterwarnings('ignore')
        
        params, cv = scipy.optimize.curve_fit(self.n_m, 
                                              x, 
                                              Signal,
                                              p0,
                                              maxfev=2000)          # Fit the curve
        
        warnings.filterwarnings('default')
        mu, sigma_phi_t = params                           # Extract the parameters

        # Determine quality of the fit using R-squared
        
        squaredDiffs = np.square(Signal - self.n_m(x, mu, sigma_phi_t))
        squaredDiffsFromMean = np.square(Signal - np.mean(Signal))
        rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
        
        self.mu = mu
        self.sigma_phi_t = sigma_phi_t
        self.rSquared = rSquared
        
        
    def plot_profile(self, my_title = 'Profile'):
        """
        Plots the luminiscence profile

        Arguments:
        x: vector containig the depth [mm]
        profile_data: vector containing the luminiscence signal for each depth
        standard_error: standard error of the profile_data
        """ 
        
        x = self.x.copy()
        profile_data = self.profile_data.copy()
          
        Half_lum_depth = self.Half_lum_depth
        
        self.axes_profile.plot(x, profile_data, label="Signal")
        # self.axes_profile.plot(x, self.n_m(x, self.mu, self.sigma_phi_t), '--', label="Fitted Curve")
        
        if isinstance(self.standard_error, str) == False:
            
            standard_error = self.standard_error
        
            self.axes_profile.fill_between(x, profile_data-standard_error, profile_data+standard_error,
                              facecolor="orange", # The fill color
                              color='blue',       # The outline color
                              alpha=0.2,          # Transparency of the fill
                              label="Standard Error")          
        
        self.axes_profile.plot([0, Half_lum_depth, Half_lum_depth],[0.5, 0.5, 0], "r--", linewidth=1)
        
        self.axes_profile.set_xlabel('Depth [mm]')
        self.axes_profile.set_ylabel('Normalized Intensity')
        self.axes_profile.set_ylim(bottom=0)
        self.axes_profile.set_ylim(top=1.5)
        self.axes_profile.set_xlim(left=0)
        self.axes_profile.legend()
        self.axes_profile.set_title(self.plot_title )
