# compressibility_drag_wing.py
# 
# Created:  Your Name, Dec 2013
# Modified:         

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
from SUAVE.Attributes.Results.Result import Result
from SUAVE.Structure import (
    Data, Container, Data_Exception, Data_Warning,
)

# python imports
import os, sys, shutil
from copy import deepcopy
from warnings import warn

# package imports
import numpy as np
import scipy as sp


# ----------------------------------------------------------------------
#  The Function
# ----------------------------------------------------------------------

def compressibility_drag_wing(conditions,configuration,geometry):
    """ SUAVE.Methods.compressibility_drag_wing(conditions,configuration,geometry)
        computes the induced drag associated with a wing 
        
        Inputs:
        
        Outputs:
        
        Assumptions:
            based on a set of fits
            
    """

    # unpack
    wings      = geometry.Wings
    #wing_lifts = conditions.lift_breakdown.clean_wing
    wing_lifts = conditions.clean_wing_lift
    mach       = conditions.mach_number
    
    # start result
    total_compressibility_drag = 0.0
    count=0  #counter
    #conditions.drag_breakdown.compressibility = Result(total = 0)

    # go go go
<<<<<<< HEAD
    for surf, lift in zip(wings, wing_lifts):
        wing = geometry.Wings[surf]
=======
    #for wing, lift in zip( wings.values(), wing_lifts.values() ):
    for wing, in zip( wings.values()):
        
>>>>>>> c422cfc93480e326c5a4ef5e7d955b38d4a85e9c
        # unpack wing
        t_c_w   = wing.t_c
        sweep_w = wing.sweep
        cl_w    = wing_lifts[count]
    
        # get effective Cl and sweep
        tc = t_c_w /(np.cos(sweep_w))
        cl = cl_w / (np.cos(sweep_w))**2
    
        # compressibility drag based on regressed fits from AA241
        mcc_cos_ws = 0.922321524499352       \
                   - 1.153885166170620*tc    \
                   - 0.304541067183461*cl    \
                   + 0.332881324404729*tc**2 \
                   + 0.467317361111105*tc*cl \
                   + 0.087490431201549*cl**2
            
        # crest-critical mach number, corrected for wing sweep
        mcc = mcc_cos_ws / np.cos(sweep_w)
        
        # divergence mach number
        MDiv = mcc * ( 1.02 + 0.08*(1 - np.cos(sweep_w)) )
        
        # divergence ratio
        mo_mc = mach/mcc
        
        # compressibility correlation, Shevell
        dcdc_cos3g = 0.0019*mo_mc**14.641
        
        # compressibility drag
        cd_c = dcdc_cos3g * (np.cos(sweep_w))**3
        
        # increment
        #total_compressibility_drag += cd_c
        
        if count==0:
        
            total_compressibility_drag = cd_c        
            
        count=count+1
        
        # dump data to conditions
<<<<<<< HEAD
        wing_results = Result(
            compressibility_drag      = cd_c    ,
            thickness_to_chord        = tc      , 
            wing_sweep                = sweep_w , 
            crest_critical            = mcc     ,
            divergence_mach           = MDiv    ,
        )
        conditions.drag_breakdown.compressible[wing.tag] = wing_results
=======
        #wing_results = Result(
            #compressibility_drag      = cd_c    ,
            #thickness_to_chord        = tc      , 
            #wing_sweep                = sweep_w , 
            #crest_critical            = mcc     ,
            #divergence_mach           = Mdiv    ,
        #)
        #conditions.drag_breakdown.compressible[wing.tag] = wing_results
>>>>>>> c422cfc93480e326c5a4ef5e7d955b38d4a85e9c

    #: for each wing
    
    # dump total comp drag
    #conditions.drag_breakdown.compressible.total = total_compressibility_drag
    

    return total_compressibility_drag