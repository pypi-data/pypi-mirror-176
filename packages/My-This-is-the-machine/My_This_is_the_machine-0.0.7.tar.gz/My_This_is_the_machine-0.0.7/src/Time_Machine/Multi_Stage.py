#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  9 15:27:54 2022

@author: gorosti
"""

import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt

class Multi_Stage_Model():
    
    def __init__(self, df, stage_number, selected_model, power_factor): 
        
        self.df = df
        self.stage_number = stage_number
        self.selected_model = selected_model
        self.power_constant = power_factor
        
        self.read_data()
        
        self.fit_model()
        
        print(self.params)
        print(self.perr)
        
        # self.print_values()
        
        # self.plot_intermediate_stages()
        
        self.relevant_output()
        
    def read_data(self):
        '''
        A method for reading the experimental data off an excel file
        Returns the raw data as attributes of the InversionModel class
        '''
        
        df = self.df
        
        # sort the x values by increasing order
        x  = df[0].sort_values()
        self.x = x.values
        
        # sort the signal values by increasing depth
        self.Signal = df[1][x.index].values
        
    def fit_model(self):
        
        
        ### We create a Fitting Class ###
        
        class fitClass:
            
            def __init__(self):
                pass
            
            def MS_2s_1order(self, x, mu, sigma_phi_te1, Ftb1):
                x = x / 1e6
                L0 = 1
                L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                L2 = np.sign(L2) * (np.abs(L2)) ** self.c
                return L2
            
            
            def MS_2s_2order(self, x, mu, sigma_phi_te1, Ftb1):
                n_i = 1
                g = 2     
                x = x / 1e6
                L0 = 1
                L1 = L0 * ((g-1)*sigma_phi_te1*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                L2 = np.sign(L2) * (np.abs(L2)) ** self.c
                return L2
            
            
            def MS_3s_1order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                x = x / 1e6
                L0 = 1
                L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                L3 = L2 * np.exp(-sigma_phi_te2 * np.exp(-mu*x)) 
                L3 = np.sign(L3) * (np.abs(L3)) ** self.c
                return L3
            
            
            def MS_3s_2order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                n_i = 1
                g = 2     
                x = x / 1e6
                L0 = 1
                L1 = L0 * ((g-1)*sigma_phi_te1*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                L3 = L2 * ((g-1)*sigma_phi_te2*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                L3 = np.sign(L3) * (np.abs(L3)) ** self.c
                return L3
        
        
        
        MS_Model = fitClass()
                
        MS_Model.c = self.power_constant 
        
        if self.stage_number == '2':
            
            if self.selected_model == 'First Order':
                
                params, cv = scipy.optimize.curve_fit(MS_Model.MS_2s_1order,
                                                  self.x,
                                                  self.Signal ** self.power_constant,
                                                  maxfev=100000) 

                if any(x<0 for x in params) == True:

                    param_bounds = ([0, 0, 0],[np.inf, np.inf, np.inf])
            
                    params, cv = scipy.optimize.curve_fit(MS_Model.MS_2s_1order,
                                                      self.x,
                                                      self.Signal ** self.power_constant,
                                                      bounds = param_bounds)
                
                self.params = params
                
                # one standard deviation errors on the parameters                
                
                self.perr = np.sqrt(np.diag(cv))
                
                
            elif self.selected_model == 'Second Order':

                params, cv = scipy.optimize.curve_fit(MS_Model.MS_2s_2order,
                                                  self.x,
                                                  self.Signal ** self.power_constant,
                                                  maxfev=100000)
                
                if any(x<0 for x in params) == True:
                    
                    param_bounds = ([0, 0, 0],[np.inf, np.inf, np.inf])
            
                    params, cv = scipy.optimize.curve_fit(MS_Model.MS_2s_2order,
                                                      self.x,
                                                      self.Signal ** self.power_constant,
                                                      bounds = param_bounds)
                
                self.params = params
                
                # one standard deviation errors on the parameters                
                
                self.perr = np.sqrt(np.diag(cv))
            
        if self.stage_number == '3':
            
            if self.selected_model == 'First Order':

                params, cv = scipy.optimize.curve_fit(MS_Model.MS_3s_1order,
                                                  self.x,
                                                  self.Signal ** self.power_constant,
                                                  maxfev=100000)
                
                if any(x<0 for x in params) == True:
                    
                    param_bounds = ([0, 0, 0, 0],[np.inf, np.inf, np.inf, np.inf])
            
                    params, cv = scipy.optimize.curve_fit(MS_Model.MS_3s_1order,
                                                      self.x,
                                                      self.Signal ** self.power_constant,
                                                      bounds = param_bounds)
            
                self.params = params
                
                # one standard deviation errors on the parameters                
                
                self.perr = np.sqrt(np.diag(cv))
                
                
            elif self.selected_model == 'Second Order':
                
                params, cv = scipy.optimize.curve_fit(MS_Model.MS_3s_2order,
                                                  self.x,
                                                  self.Signal ** self.power_constant,
                                                  maxfev=100000)
                
                if any(x<0 for x in params) == True:
                    
                    param_bounds = ([100, 0, 0, 0],[np.inf, np.inf, np.inf, np.inf])
            
                    params, cv = scipy.optimize.curve_fit(MS_Model.MS_3s_2order,
                                                      self.x,
                                                      self.Signal ** self.power_constant,
                                                      bounds = param_bounds)
                
                self.params = params
                
                # one standard deviation errors on the parameters                
                
                self.perr = np.sqrt(np.diag(cv))
                
        
    def print_values(self):
              
        print('Mu {0:.2f} ± {1:.2f}'.format(self.params[0] / 1e6, 
                                            self.perr[0] / 1e6))
        print('Sigma_phi_t1 equals {0:.2f} ± {1:.2f}'.format(self.params[1],
                                                             self.perr[1]))
        print('F_tb1 {0:.2f} ± {1:.2f}'.format(self.params[2],
                                               self.perr[2]))
            
        if self.stage_number == '3':
        
            print('Sigma_phi_t2 equals {0:.2f} ± {1:.2f}'.format(self.params[3],
                                                                 self.perr[3]))

    def plot_intermediate_stages(self, figure):
        
        ### We create a Class with the Intermediate stages
        
        class Inter_Stages:
            
            def __init__(self):
                pass
            
            def L1_2s_1order(self, x, mu, sigma_phi_te1, Ftb1):
                x = x / 1e6
                L0 = 1
                L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
                return L1
            
            def L1_3s_1order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                x = x / 1e6
                L0 = 1
                L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
                return L1
            
            def L2_2s_1order(self, x, mu, sigma_phi_te1, Ftb1):
                x = x / 1e6
                L0 = 1
                L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                return L2
            
            def L2_3s_1order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                x = x / 1e6
                L0 = 1
                L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                return L2
            
            def L3_1order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                x = x / 1e6
                L0 = 1
                L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                L3 = L2 * np.exp(-sigma_phi_te2 * np.exp(-mu*x))
                return L3
            
            def L1_2s_2order(self, x, mu, sigma_phi_te1, Ftb1):
                n_i = 1
                g = 2     
                x = x / 1e6
                L0 = 1
                L1 = L0 * ((g-1)*sigma_phi_te1*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                return L1
            
            def L1_3s_2order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                n_i = 1
                g = 2     
                x = x / 1e6
                L0 = 1
                L1 = L0 * ((g-1)*sigma_phi_te1*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                return L1
            
            def L2_2s_2order(self, x, mu, sigma_phi_te1, Ftb1):
                n_i = 1
                g = 2     
                x = x / 1e6
                L0 = 1
                L1 = L0 * ((g-1)*sigma_phi_te1*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                return L2
            
            def L2_3s_2order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                n_i = 1
                g = 2     
                x = x / 1e6
                L0 = 1
                L1 = L0 * ((g-1)*sigma_phi_te1*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                return L2
            
            def L3_2order(self, x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
                n_i = 1
                g = 2     
                x = x / 1e6
                L0 = 1
                L1 = L0 * ((g-1)*sigma_phi_te1*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                L2 = (L1 - 1) * np.exp(-Ftb1) + 1
                L3 = L2 * ((g-1)*sigma_phi_te2*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
                return L3

        IStage = Inter_Stages()

        self.figure_stages = figure
        
        self.axes = self.figure_stages.add_subplot(1,1,1)
        
        x = np.linspace(self.x[0], self.x[-1], 100)
        
        if self.stage_number == '2':

            self.axes.scatter(self.x, self.Signal, label = 'Data')
            # ax.set_yscale('log')
            self.axes.set_ylim(10**(-3), 10**(0.3))
            self.axes.set_ylabel('Signal')
            self.axes.set_xlabel('Depth [mm]')
            
            if self.selected_model == 'First Order':
            
                self.axes.plot(x, IStage.L1_2s_1order( x, *self.params ), '--',
                         label="First Exposure Event")
                self.axes.plot(x, IStage.L2_2s_1order( x, *self.params ), '--', 
                         label="Final State")
            
            elif self.selected_model == 'Second Order':
                
                self.axes.plot(x, IStage.L1_2s_2order( x, *self.params ), '--',
                         label="First Exposure Event")
                self.axes.plot(x, IStage.L2_2s_2order( x, *self.params ), '--', 
                         label="Final State")
            
            self.axes.set_title('Reproduce Intermediate Profiles')
            self.axes.legend()
            
            
        if self.stage_number == '3':
        
            self.axes.scatter(self.x, self.Signal, label = 'Data')
            # ax.set_yscale('log')
            self.axes.set_ylim(10**(-3), 10**(0.3))
            self.axes.set_ylabel('Signal')
            self.axes.set_xlabel('Depth [mm]')
            
            if self.selected_model == 'First Order':
                
                self.axes.plot(x, IStage.L1_3s_1order( x, *self.params ), '--',
                         label="First Exposure Event")
                self.axes.plot(x, IStage.L2_3s_1order( x, *self.params ), '--', 
                         label="First Burial Event")
                self.axes.plot(x, IStage.L3_1order( x, *self.params ), '--', 
                         label="Final State")
                
            elif self.selected_model == 'Second Order':
                
                self.axes.plot(x, IStage.L1_3s_2order( x, *self.params ), '--',
                         label="First Exposure Event")
                self.axes.plot(x, IStage.L2_3s_2order( x, *self.params ), '--', 
                         label="First Burial Event")
                self.axes.plot(x, IStage.L3_2order( x, *self.params ), '--', 
                         label="Final State")
            
            
            self.axes.set_title('Reproduce Intermediate Profiles')
            self.axes.legend()
            
            
    def relevant_output(self):
        
        self.parameter_values = []
        
        self.parameter_values = ['\u03BC = {0:.2f} ± {1:.2f}'.format(self.params[0] / 1e6,
                                                                     self.perr[0] / 1e6),
                         '\u03C3\u03C6 t1 = {0:.2E} ± {1:.2E}'.format(self.params[1],
                                                                      self.perr[1]),
                         'Ftb1 = {0:.2f} ± {1:.2f}'.format(self.params[2],
                                                           self.perr[2])]
            
        if self.stage_number == '3':
            
            self.parameter_values.append('\u03C3\u03C6 t2 = {0:.2E} ± {1:.2E}'.format(self.params[3],
                                                                                      self.perr[3]))


            
            
            
        
        
        
        
        
        
        