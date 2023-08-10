# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 10:19:53 2021

@author: Brandon McNabb
"""
class std_curve():
    def __init__(self, std_concs, std_vals):
        """
        Functions to analyze a standard curve.

        Parameters
        ----------
        std_concs : list, numpy array, Series, or DataFrame
            standard concentrations used.
        std_vals : list, numpy array, Series, or DataFrame
            Corresponding response variable for each concentration (e.g. a val area).

        Returns
        -------
        None.

        """
        
        import numpy as np
        import pandas as pd
        
        # Convert list to column vectors
        if isinstance(std_concs, (list, pd.Series)):
            std_concs = np.array(std_concs).reshape(-1,1)
        if isinstance(std_vals, (list, pd.Series)):
            std_vals = np.array(std_vals).reshape(-1,1)
            
        # if numpy arrays, check that they are column vectors
        if isinstance(std_concs, np.ndarray):
            if std_concs.ndim<2:
                std_concs = std_concs.reshape(-1,1)
        if isinstance(std_vals, np.ndarray):
            if std_vals.ndim<2:
                std_vals = std_vals.reshape(-1,1)
        
            
        self.std_concs = std_concs
        self.std_vals = std_vals
        
    def regress(self, print_results=True, plot_results=True):
        """
        Generate summary stats (R2, slope/intercept, best-fit equation) for the standard curve.
    
        Returns
        -------
        coef : float64 array
            Coefficient derived from linear regression.
        intercept : float64 array
            Intercept derived from linear regression.
    
        """
        import matplotlib.pyplot as plt
        from sklearn import linear_model
        
        # Compute linear regression
        lm = linear_model.LinearRegression()
        lm.fit(self.std_concs,
               self.std_vals)
        self.intercept = lm.intercept_
        self.coef = lm.coef_[0]
        self.R2 = lm.score(self.std_concs,
                      self.std_vals)
        best_fit_eq_text ='y = '+str(self.coef[0])[:5]+'x + '+str(self.intercept[0])[:5]
        R2_text = r'$R^{2}$ = '+str(self.R2)[:5]
        
        # Conditionally print output stats
        if print_results is True:
            print(best_fit_eq_text)
            print('R2 = '+str(self.R2)[:5])
        
        # Plot the standard curve
        if plot_results is True:
            fig = plt.figure(figsize=(18,18))
            font={'family':'DejaVu Sans',
                  'weight':'normal',
                  'size':'24'} 
            plt.rc('font', **font) # sets the specified font formatting globally
            ax = fig.add_subplot(111)
            ax.plot(self.std_concs,
                    self.std_vals,
                    'k.',
                    ms=24)
            ax.plot(self.std_concs,
                    lm.predict(self.std_concs), 'r-', ms=24)
            ax.set_ylabel('val Areas')
            ax.set_xlabel('Concentrations')
            ax.text(0.7,
                    0.1,
                    best_fit_eq_text+'\n'+R2_text,
                    transform=ax.transAxes)
        
        
        return self.coef, self.intercept, self.R2
    
    def calc(self, val):
        """
        Calculate concentration(s). Requires running regress() first.
    
        Parameters
        ----------
        val : Int, list, float64 array, Series or DataFrame
            val area(s) measured. Function accepts single or multiple values.
    
        Returns
        -------
        conc : list, float64 array, Series or DataFrame
            Corresponding concentration(s) to inputted val area(s).
    
        """
        conc = (val-self.intercept)/self.coef
        return conc

if __name__ == '__main__':
    
    # Example: given a list of concentrations and the measured responses (in this case, peak areas),
    # compute a regression and calculate the concentration of a new sample.
    import numpy as np
    import pandas as pd
    
    std_concs = [0,
                 2,
                 10,
                 25,
                 50,
                 75,
                 100,
                 ] # in nM
    
    std_vals = [
                627.07, 
                940.99, 
                1032.87, 
                1442.51, 
                2384.65, 
                3643.81, 
                4417.69,
                ]

    # set up our curve
    curve = std_curve(std_concs, std_vals)
    
    # get the regression parameters, and plot the best fit
    coef, intercept, R2 = curve.regress(print_results=True, plot_results=True)
    
    # Given a new measurement, calculate its concentration
    val = 1600
    conc = curve.calc(val)[0]
    print(f'concentration = {conc:.2f} nM')
