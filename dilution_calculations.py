# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 11:58:06 2021

@author: Brandon McNabb
"""

def dilute(C1=None, V1=None, C2=None, V2=None, print_val=False):
    """
    A simple function to automate dilution calculations, solving for the unknown 
    concentration or volume using C1*V1=C2*V2. This funtion will print the final
    value formatted in the appropriate units and rounded to 1 decimal point.

    Parameters
    ----------
    C1 : float, optional
        Initial concentration, in M. The default is None.
    V1 : float, optional
        Initial volume to add, in L. The default is None.
    C2 : float, optional
        Final concentration, in M. The default is None.
    V2 : float, optional
        Final volume to make solution up to, in L. The default is None.

    Returns
    -------
    x : float
        Solved concentration or volume, in either M or L.

    """
    # calculate dilution chemistry
    if C1 is None:
        x = (C2*V2)/V1
    if V1 is None:
        x = (C2*V2)/C1
    if C2 is None:
        x = (C1*V1)/V2
    if V2 is None:
        x = (C1*V1)/C2
    if print_val is True:
        # Print anwser in appropriate units
        if V1 is None or V2 is None:
            if x < 1e-6 and x >= 1e-9:
                print(str(round(x*1e9,1))+' nL')
            if x < 1e-3 and x >= 1e-6:
                print(str(round(x*1e6,1))+' uL')
            if x < 0.1 and x >= 1e-3:
                print(str(round(x*1e3,1))+' mL')
            if x >= 0.1:
                print (str(round(x,1))+' L')
        if C1 is None or C2 is None:
            if x < 1e-6 and x >= 1e-9:
                print(str(round(x*1e9,1))+' nM')
            if x < 1e-3 and x >= 1e-6:
                print(str(round(x*1e6,1))+' uM')
            if x < 0.1 and x >= 1e-3:
                print(str(round(x*1e3,1))+' mM')
            if x >= 0.1:
                print(str(round(x,1))+' M')
    return x

def dilution_series(N_std, total_vol, std_conc):
    """
    Simple function to iteratively generate a dilution series to produce a standard curve, given a starting stock concentration/volume.

    Parameters
    ----------
    N_std : int
        The number of standards in the series.
    total_vol : int
        The total volume of the stock.
    std_conc : int
        The concentration of the stock.

    Returns
    -------
    concs : list
        Standards in the series.
    sample_vols : int
        Corresponding volumes in the series.

    """
    # for the first iteration:
    sample_vol = total_vol
    
    # calculate dilution series
    concs = []
    sample_vols = []
    
    for i in range(N_std):
        sample_vols.append(total_vol-(i*(total_vol/(N_std-1))))
        concs.append(dilute(C1=std_conc, V1=sample_vol, V2=total_vol))
    
    return concs, sample_vols
    
    