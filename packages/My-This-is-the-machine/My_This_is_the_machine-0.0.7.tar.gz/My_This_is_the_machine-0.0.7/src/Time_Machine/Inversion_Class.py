import numpy as np
import pandas as pd
from scipy.optimize import minimize


class InversionModel():
    
    def __init__(self, df): 
        
        self.df = df
        self.x = None
        self.n = None
        
        # Definition of model parameters
        self.sigma_phi_t_max = 10**(8)   # Dimensionless
        self.sigma_phi_t_min = 10**(0)   # Dimensionless    
        self.mu_max = 5                  # mm-1
        self.mu_min = 0.05                # mm-1 
        
        
    
    def read_data(self):
        '''
        A method for reading the experimental data off an excel file
        Returns the raw data as attributes of the InversionModel class
        '''
        
        df = self.df
        
        # print(df)
        
        # sort the x values by increasing order
        x  = df[0].sort_values()
        self.x = x.values
        
        # sort the signal values by increasing depth
        self.n = df[1][x.index].values
        
        if len(self.df.columns) == 3:
            self.n_err  = df[2][x.index].values
        else:
            self.n_err = 'None'
        
        
        # create a threshold for the plateau
        above_threshold = self.n > 0.95
        
        # return the index of the first value to be above 0.95
        self.index_plateau = df[above_threshold].index.values[0]
    
        # store the standard deviation of the plateau
        self.n_sd = self.n[self.index_plateau :].std()
    
    def run_model(self, model, tt):
        
        # log the number of iterations
        self.tt = tt
        for i in range(2, int(np.sqrt(tt))):
            if tt % i == 0:
                self.chunk = i
 
        # definition of model parameters
        sigma_phi_t_max = self.sigma_phi_t_max
        sigma_phi_t_min = self.sigma_phi_t_min 
        mu_max = self.mu_max
        mu_min = self.mu_min
        
        self.log10_spt_max = int(np.log10(sigma_phi_t_max))
        self.log10_spt_min = int(np.log10(sigma_phi_t_min))
    
        # create a mu and sigma_phi space to explore
        # vector of size TT to sample SP_t
        vec_sigma_phi_t = np.power(10,
                                   np.linspace(
                                       np.log10(sigma_phi_t_min),
                                       np.log10(sigma_phi_t_max),
                                       self.tt
                                    )
                                )
        
        #vector of size TT to sample mu
        vec_mu = np.linspace(mu_min,mu_max,self.tt)  
        
        # create a 2D grid of the space to explore.
        sigma_phi_t_matrix, mu_matrix = np.meshgrid(vec_sigma_phi_t,vec_mu)  
        
        # expand dimensions to allow element wise array operations
        sigma_phi_t_matrix=  np.vsplit(np.expand_dims(sigma_phi_t_matrix,2), self.chunk) 
        mu_matrix = np.vsplit(np.expand_dims(mu_matrix,2), self.chunk)
        
        # add to attributes of the model the modelled signal matrix, mu and sigma_phi_t space
        # cycle over chunks of the matrices..
        
        n_matrix = [ model(self.x,mu_chunk,sigma_phi_t_chunk)
                    for mu_chunk,sigma_phi_t_chunk
                    in zip(mu_matrix,sigma_phi_t_matrix)]
        

        self.n_matrix = np.vstack(n_matrix)
        self.mu_matrix = np.vstack(mu_matrix)
        self.sigma_phi_t_matrix = np.vstack(sigma_phi_t_matrix)
        
    
    def misfit(self):

        # misfit matrix
        
        diff_chunks = [n_chunk - empty_chunk * self.n 
                       for n_chunk,empty_chunk 
                       in zip(np.vsplit(self.n_matrix,self.chunk),
                               np.vsplit(np.expand_dims(np.ones((self.tt,self.tt)),2),self.chunk))] 
        
        misfit_chunks = [np.sum(np.abs(diff_chunk),axis = 2) / self.n_sd for diff_chunk in diff_chunks]
    
        misfit_matrix = np.vstack(misfit_chunks)
        chi = 1./np.exp(0.5*misfit_matrix)
        max_chi = chi.max()
        norm_chi  = chi /max_chi
        
        self.norm_chi = norm_chi
    
    def confidence_intervals(self, known_t):
        
        self.known_t = known_t
        
    
        # define quantiles of interest
        random_vec = np.random.uniform(0.6827,1,size =(self.tt,self.tt))  # uniform sampling between 0.6827 and 1 (1 sigma). 

        quantiles = [0.025,0.175,0.5,0.825,0.975]  # define the quantiles of interest (-2s, -1s, median, +1s, +2s)
    
        # index the parameter matrices, returning possible mu or sigma_phi_t values
        # if the normed chi value is above a randomly chosen threshold.
        self.mu_pdf = self.mu_matrix[self.norm_chi > random_vec].flatten()
        self.sigma_phi_t_pdf = self.sigma_phi_t_matrix[self.norm_chi > random_vec].flatten()
        
        # select the quantiles from flattened arrays (pdfs)
        mu_q = np.quantile(self.mu_pdf, quantiles)
        sigma_phi_t_q =  np.quantile(self.sigma_phi_t_pdf,quantiles)
        
        if known_t != 'None':
            # divide by known time to get sigma_phi
            sigma_phi_q = sigma_phi_t_q/self.known_t
        
            # make dictionary of confidence intervals
            conf_intervals = {'sigma_phi': (sigma_phi_q,'s-1'),
                          'sigma_phi_t': (sigma_phi_t_q,''),
                          'mu': (mu_q, 'mm-1')
                     }
        
            self.conf_intervals = conf_intervals
            self.log10_sp_max = int(self.log10_spt_max - np.log10(self.known_t))
            self.log10_sp_min = int(self.log10_spt_min - np.log10(self.known_t))
            
            
            self.sigma_phi_median = self.conf_intervals["sigma_phi"][0][2]

            # make the median values easy to access
            
            sigma_phi_1s_low = np.log10(sigma_phi_q[2])-np.log10(sigma_phi_q[1])
            sigma_phi_1s_high = np.log10(sigma_phi_q[3])-np.log10(sigma_phi_q[2])
            sigma_phi_2s_low = np.log10(sigma_phi_q[2])-np.log10(sigma_phi_q[0])
            sigma_phi_2s_high = np.log10(sigma_phi_q[4])-np.log10(sigma_phi_q[2])
            
            self.sigma_phi_1s_errors = [[sigma_phi_1s_low], [sigma_phi_1s_high]]
            self.sigma_phi_2s_errors = [[sigma_phi_2s_low], [sigma_phi_2s_high]]
        else:
            # make dictionary of confidence intervals
            self.conf_intervals = {'sigma_phi_t': (sigma_phi_t_q,''),
                          'mu': (mu_q, 'mm-1')
                             }
            
            
        self.mu_median = self.conf_intervals["mu"][0][2]
        self.sigma_phi_t_median = self.conf_intervals["sigma_phi_t"][0][2]



        mu_1s_low = mu_q[2]-mu_q[1] 
        mu_1s_high = mu_q[3]-mu_q[2]
        mu_2s_low = mu_q[2]-mu_q[0]
        mu_2s_high = mu_q[4]-mu_q[2]
        
    
        self.mu_1s_errors = [[mu_1s_low], [mu_1s_high]]
        self.mu_2s_errors = [[mu_2s_low], [mu_2s_high]]
        

        
    def print_run(self):
        
        # print results
        quantile_names = ('2sigma_inf','1sigma_inf','Median','1sigma_sup','2sigma_sup')
        log = []
        for key,value in self.conf_intervals.items():
            variable, unit = value[0],value[1]
        
            for n,quantile in enumerate(quantile_names):
                s = "{} {} =  {:.2e} {}".format(key,quantile,variable[n], unit)
                log.append(s)
        
        # for line in log:
        #     print(line)
            
        self.log = log
        
        
    def plot_figure(self, model):
        
        # # define a figure environment
        # fig, axes = plt.subplots(1,2, figsize = (12,5))
        
        self.axes_0 = self.figure_profile.add_subplot(1,1,1)
    
        if isinstance(self.n_err, str):
            
            # plot the measured signal
            self.axes_0.scatter(self.x, self.n,)
            
        else:
            # plot the measured signal
            self.axes_0.errorbar(self.x,self.n, yerr = self.n_err,ls='', 
                                 marker = 'o', c = 'green',
                                 markerfacecolor  = 'white', zorder = 100,
                                 label = 'Signal')
            
        # plot the modelled signal using median mu and phi, and a model.
        xi = np.linspace(0,self.x[-1],100)
        
        self.axes_0.plot(xi,model(xi, self.mu_median, self.sigma_phi_t_median), 
                         color = 'red',
                         label = 'Model')
        
       
        # label the axes of axes[0]
        self.axes_0.set_xlabel("Depth [mm]")
        # self.axes_0.set_ylabel("Normalised luminescence signal")
        
        self.axes_0.legend()

        
        
        '''#just for saving subfig. 1:
        
        # define a figure environment
        fig, axes = plt.subplots(1,1, figsize = (6,5))
    
        # plot the measured signal
        axes.errorbar(self.x,self.n,yerr = self.n_err,ls='', marker = 'o', c = 'Tab:blue', zorder = 100, label = 'Measured data')
    
        # plot the modelled signal using median mu and phi, and a model.
        xi = np.linspace(0,self.x[-1],100)
        
        axes.plot(xi,model(xi, self.mu_median, self.sigma_phi_t_median), color = 'Tab:orange', label = 'Model')
        
       
        
        # label the axes of axes[0]
        axes.set_xlabel("Depth [mm]")
        axes.set_ylabel("Normalised luminescence signal")
        axes.legend()
        handles, labels = plt.gca().get_legend_handles_labels()

        #specify order of items in legend
        order = [1,0]

        #add legend to plot
        plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order], loc='lower right') 
        
        # plt.savefig('../Python_paper/Images/test.svg', transparent = False, bbox_inches = 'tight', pad_inches = 0.2)
        
        # create a colour map
        '''
        
        self.axes_1 = self.figure_matrix.add_subplot(1,1,1)
        
        if self.known_t != 'None':
            # im = self.axes_1.contourf(np.log10(self.sigma_phi_t_matrix.reshape(self.tt,self.tt)/self.known_t),
            #               self.mu_matrix.reshape(self.tt,self.tt),
            #               self.norm_chi,
            #               np.linspace(0,1,25),
            #               cmap = 'magma')
            
            self.figure_matrix.colorbar(self.axes_1.contourf(np.log10(self.sigma_phi_t_matrix.reshape(self.tt,self.tt)/self.known_t),
                          self.mu_matrix.reshape(self.tt,self.tt),
                          self.norm_chi,
                          np.linspace(0,1,25),
                          cmap = 'magma'))
            
            # set limits
            # find optimal limits.
            
            xlim0 = max(-8, np.log10(self.sigma_phi_median)  - self.sigma_phi_2s_errors[0][0]*5)
            xlim1 = min(10, np.log10(self.sigma_phi_median)  + self.sigma_phi_2s_errors[1][0]*5)
            ylim0 = max(1e-4, self.mu_median  - self.mu_2s_errors[0][0]*5)
            ylim1 = min(5, self.mu_median  + self.mu_2s_errors[1][0]*5)
            
            # print(self.sigma_phi_2s_errors[0][0])
            # print(self.mu_2s_errors[0][0])
            # ! It can be that both tend to zero 
            # > The axes are messed up!
            # Use a different approach
            
            # MODIFICATION
            xlim0 = max(-8, np.log10(self.sigma_phi_median) * 0.9)
            xlim1 = min(10, np.log10(self.sigma_phi_median) * 1.1)
            ylim0 = max(1e-4, self.mu_median * 0.9)
            ylim1 = min(5, self.mu_median * 1.1)
            
            self.axes_1.set_xlim(xlim0,xlim1)
            self.axes_1.set_ylim(ylim0,ylim1)
            

            # set the xtick labels
            ticks = [x for x in range(int(self.axes_1.get_xlim()[0]),int(self.axes_1.get_xlim()[1])+1)]

            xlabels = ["$10^{{{}}}$".format(x) for x in ticks]
            self.axes_1.set_xticks(ticks)
            self.axes_1.set_xticklabels(xlabels)
            #axes[1].set_xlabel("sigma phi s$^{-1}$")
            self.axes_1.set_xlabel("\u03C3\u03C6 [s$^{-1}$]") # sigma phi
            self.axes_1.set_ylabel("$\mu$ [mm$^{-1}$]")

            self.axes_1.errorbar([np.log10(self.sigma_phi_median)],
                         [self.mu_median],
                         yerr = self.mu_1s_errors,
                         xerr = self.sigma_phi_1s_errors,
                         marker = 'o',
                         color = 'red',
                         zorder = 100,
                         markersize = 5,
                         markerfacecolor ='white',
                         ecolor = 'white'
                        )
            self.axes_1.errorbar([np.log10(self.sigma_phi_median)],
                         [self.mu_median],
                         yerr = self.mu_2s_errors,
                         xerr = self.sigma_phi_2s_errors,
                         marker = '.',
                         color = 'red',
                         zorder = 50,
                         markersize = 5,
                         markerfacecolor ='white',
                         ecolor = 'white',
                         linestyle  = '--',
                         linewidth = 0.5
                        )
            
            # fig.show()
            
            # plt.savefig('../Python_paper/Images/test.svg', transparent = False, bbox_inches = 'tight', pad_inches = 0.2)
            # plt.show()
                
    def calibrate(self, model, known_t, tt, figure_profile, fig_matrix, verbose = True):
        
        self.figure_profile = figure_profile
        self.figure_matrix = fig_matrix
        
        self.read_data()
        
        
        # Make sure the medians fall in the middle
        
        self.run_model(model, tt)
        self.misfit()
        self.confidence_intervals(known_t)
        
        
        
        # self.matrix_range_sigma_phi = self.sigma_phi_t_max - self.sigma_phi_t_min
        # self.matrix_range_mu = self.mu_max - self.mu_min
        
        
        # while (self.sigma_phi_median < self.sigma_phi_t_min * 2  or 
        #        self.mu_median < self.mu_min + self.matrix_range_mu * 0.1):
        
        #     if self.sigma_phi_median < self.sigma_phi_t_min * 2:
                
        #         self.sigma_phi_t_min = self.sigma_phi_t_min / 2
        #         # self.sigma_phi_t_max = self.sigma_phi_t_max / 10
                
        #         print(self.sigma_phi_t_min)
        #         print(self.sigma_phi_t_max)
                
        #     if self.mu_median < self.mu_min + self.matrix_range_mu * 0.1:
                
        #         self.mu_min = self.mu_min - self.matrix_range_mu * 0.1
        #         # self.mu_max = self.mu_max - self.matrix_range_mu * 0.2
                
        #         print(self.mu_min)
        #         print(self.mu_max)
            
        #     self.run_model(model, tt)
        #     self.misfit()
        #     self.confidence_intervals(known_t)
        
        
        
        
        # We start a finer 2nd iteration
        
        # self.sigma_phi_t_min = self.sigma_phi_median / 1000
        # self.sigma_phi_t_max = self.sigma_phi_median * 1000
        # self.mu_min = self.mu_median / 1.5
        # self.mu_max = self.mu_median * 1.5
        
        # print(self.mu_min)
        # print(self.mu_max)
        
        # print(self.sigma_phi_t_min)
        # print(self.sigma_phi_t_max)
        
        # self.run_model(model, tt)
        # self.misfit()
        # self.confidence_intervals(known_t)
        
        self.print_run()
        if verbose == True:
            self.plot_figure(model)
        # else:
            # print('verbose = False was passed, and figure plotting was suppressed')
            
            
            
    def calibrate_no_plots(self, model, known_t, tt, verbose = True):
        
        self.read_data()
        self.run_model(model, tt)
        self.misfit()
        self.confidence_intervals(known_t)
        # self.print_run()
        # if verbose == True:
        #     self.plot_figure(model)
        # else:
        #     print('verbose = False was passed, and figure plotting was suppressed')
            
            
    
def get_bleach_depth(xmax,mu,sigma_phi,t, model):
    '''
    returns the depth at which the normalised luminescence signal equals 0.5
    takes in an InversionModel class
    takes in a model type: n_m or n_i
    '''
    
    # depth values in mm
    xi = np.linspace(0,xmax,1000)

    # calculate the bleaching model
    yi = model(xi,mu,sigma_phi*t*365.25*24*3600)

    # find index of value where yi=0.5
    idx = np.argmin(np.abs(0.5-yi))

    # find out the sample bleach depth
    bleach_depth = xi[idx]
    return bleach_depth


def r_square(calib_mod, model, extent):
    """ model: eitner n_i for the first order model or n_m for second order model
        extent: either "include_plateau or "ignore_plateau"; includes or ignores values of the plateau (>0.95)
    """
    #extracting measured and modelled calibration data: 
    headers = ['x', 'measured_y', 'measured_y_err', 'modelled_y']
    data = [calib_mod.x, calib_mod.n, calib_mod.n_err, model(calib_mod.x, calib_mod.mu_median, calib_mod.sigma_phi_t_median)]

    measured_calib_data = pd.DataFrame.from_dict(dict(zip(headers, data)))
    
    if extent == "include_plateau": 
        pass
    if extent == "ignore_plateau": 
        measured_calib_data = measured_calib_data.loc[(measured_calib_data["modelled_y"] < 0.95)]
   
    df = measured_calib_data

    res = df["measured_y"].sub(df["modelled_y"]).pow(2).sum()
    tot = df["measured_y"].sub(df["measured_y"].mean()).pow(2).sum()
    
    r2 = 1 - res/tot
    
    # print("Convergence between measured values and fitted curve, R² = {:.3f}".format(r2))
    
    return r2





def select_model(Model_selection):
    
    #-----------------------------------------------#
    #                DEFINE THE MODELS              #
    #-----------------------------------------------#  
    
    # first order model: 
    def n_first_order(x, mu, sigma_phi_t):
        return np.exp(-sigma_phi_t*np.exp(-mu*x))
    
    
    # general order model: 
    ''' At saturation level, the luminescence profiles are normalized to 
        unity and we assume full
        saturation before the onset of bleaching, i.e. n_i = 1.
        
        g is the kinetic order of the model. For the general-order model 
        we use g = 2 as this order is
        generally observed for IRSL (IR50) stimulation curves. 
        Note that when g = 1 the general-order 
        model n_m reduces to the first-order model n_i.
    '''
    def n_general_order(x, mu, sigma_phi_t):
        n_i = 1
        g = 2     
        return ((g-1)*sigma_phi_t*np.exp(-mu*x)+n_i**(1-g))**(1/(1-g))
    
    
    # def n_burial_model(x, mu, sigma_phi_te1, Ftb1, sigma_phi_te2):
    #     x = x / 1e6
    #     L0 = 1
    #     L1 = L0 * np.exp(-sigma_phi_te1 * np.exp(-mu*x))
    #     L2 = (L1 - 1) * np.exp(-Ftb1) + 1
    #     L3 = L2 * np.exp(-sigma_phi_te2 * np.exp(-mu*x))
    #     return L3
    
    if Model_selection == 'First Order':
        
        n_model = n_first_order
        
    if Model_selection == 'Second Order':
        
        n_model = n_general_order 
        
    # if Model_selection == 'Burial':
        
    #     n_model = n_burial_model 
        
    return n_model


def plot_age_histogram(xi,yi,calib_mod,model_name,ax, mu_random, sigma_phi_random, total = 10000):
          
    ages = []

    for rand_mu, rand_sigma_phi in zip(mu_random,sigma_phi_random):
        ages.append(get_age(xi, yi, rand_mu, rand_sigma_phi,7, model_name)/(3600*24*365.25))

    ax.hist(ages, bins = 98, density=True)
    ax.set_xlabel('Age [years]')
    ax.set_ylabel('Age probability density')
    
    if (np.percentile(ages, 99) - np.percentile(ages, 1)) < np.percentile(ages, 50)*0.1 :
        
        ax.set_xlim([np.percentile(ages, 50)*0.9, np.percentile(ages, 50)*1.1])
        
    else:
    
        ax.set_xlim([np.percentile(ages, 1), np.percentile(ages, 99)])

    return ages, ax


def diff_n_m_t(x, n, mu, sigma_phi, model_name):
    """ create function which compute the sum of squared differences,
        x is the position along sample in mm
        n is the standardised measured signal
        mu and sigma phi are computed above
    """

    n_i = 1
    g = 2
    
    measured = np.expand_dims(n,1)
    if model_name == 'Second Order':
        # compute second order model
        modelled =  lambda t : ((g-1)*sigma_phi*np.power(10,t)*np.exp(-mu*np.expand_dims(x,1))+n_i**(1-g))**(1/(1-g))
    else:
        # compute first order model
        modelled = lambda t : np.exp(-sigma_phi*np.power(10,t)*np.exp(-mu*np.expand_dims(x,1)))
    
    # define the custom summed square difference function, only taking time t as variable
    model = lambda t : np.sum(( measured - modelled(t))**2)
    
    # returns a function which computes the sum of squared differences
    return np.vectorize(model)

def get_age(x, n, mu, sigma_phi, t0, model_name):
    
    # minimize the time exponent to allow variation in times using logspace.
    results = minimize(diff_n_m_t(x, n, mu, sigma_phi, model_name), t0)
    
    return((np.power(10,results.x))[0])

def age_calculation(ds, model_name, model, calib_mod, figure_fit_age,
                    figure_age_histo, mu_forced='None', 
                    mu_error_forced=None, age_tt = 10000):
       
    ax_model = figure_fit_age.add_subplot(1,1,1)
    ax_histogram = figure_age_histo.add_subplot(1,1,1)

    
    # read the column data
    xi    = np.array(ds[0])
    yi    = np.array(ds[1])
    if len(ds.columns) == 3:
        errors = ds[2].values            # Standard error of the signal
    else:
        errors = 'None'
    
    
    # using the computed mu and sigma_phi values
    mu = calib_mod.mu_median # A.mu_median  # A.mu_median is the calculated µ of the calibration sample; alternatively use another value
    sigma_phi = calib_mod.sigma_phi_median # this is the calculated sig_phi of the calibration sample; 
    
    
    # mu follows normal distribution
    
    # if mu is hard coded, give some estimate of the standard dev too!
    if mu_forced != 'None':
        # print('You specified a forced mu value. Using mu = {}'.format(mu_forced))
        # print('Still sigma_phi from the calibration sample. sigma_phi = {}'.format(sigma_phi))

        mu_random = np.random.normal(mu_forced,mu_error_forced,age_tt)
        mu = mu_forced
            
    # if mu is not hardcoded, we just use the median and conf. intervals of the calib. model
    else:
        # print('You did not specify a forced mu value. Using mu = {}'.format(mu))
        # print('Still sigma_phi from the calibration sample. sigma_phi = {}'.format(sigma_phi))
        mu_random = np.random.normal(mu,calib_mod.mu_1s_errors[1],age_tt)
    
    # sigma phi 
    sigma_phi_random = np.power(10,np.random.normal(np.log10(calib_mod.sigma_phi_median),calib_mod.sigma_phi_1s_errors[1],age_tt))

    core_age,age_histogram = plot_age_histogram(xi,yi,calib_mod,model_name,ax_histogram, mu_random, sigma_phi_random, total = age_tt)
    
    
    
    t = np.median(core_age)
    t_2sigma_inf = np.quantile(core_age,[0.125])
    t_2sigma_sup = np.quantile(core_age,[0.975])
    
    
    
    age_histogram.text(0.88, 0.70, "Age: {:.2f} years".format(t),fontweight='bold', ha='right', transform=figure_age_histo.transFigure) 
    age_histogram.text(0.88, 0.67, "Age-2s: {:.2f} years".format(t_2sigma_inf[0]),ha='right', transform=figure_age_histo.transFigure)
    age_histogram.text(0.88, 0.64, "Age+2s: {:.2f} years".format(t_2sigma_sup[0]),ha='right',  transform=figure_age_histo.transFigure) 

    if len(ds.columns) == 3:
        ax_model.errorbar(xi,yi,yerr = errors,marker = 'o', lw = 0,elinewidth = 1, label = "Measured data")
        
    elif len(ds.columns) == 2:
        ax_model.plot(xi, yi, label = "Measured data")
   
    # plot the calculated sample age model curve...
    xii = np.linspace(0,xi[-1],100)
    
   
    
    ax_model.plot(xii, model(xii,mu,sigma_phi*t*3600*24*365.25), label = 'Model')
    ax_model.set_xlabel('Depth [mm]')
    # ax_model.set_ylabel('Normalized luminescence signal')
    
    # true age of the generated sample: 10e4 years, model curve
    #ax.plot(xi,n_m(xi,mu,sigma_phi*10e4*(365.25*24*3600)), label = 'generated sample')
    ax_model.legend()
    model_of_dating_sample = lambda x : model(x,mu,sigma_phi*t*3600*24*365.25) # this is the modelled curve for the dating sample
    
    return t,model_of_dating_sample