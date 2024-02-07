'''
    File: social_welfare_function.py
    Author: Wes Holliday (wesholliday@berkeley.edu) and Eric Pacuit (epacuit@umd.edu)
    Date: February 6, 2024
    
    The SWF class and helper functions for social welfare functions
'''

import functools
import numpy as np
from numba import jit # Remove until numba supports python 3.11
import random

class SWF(object): 
    """
    A class to add functionality to social welfare functions 

    Args:
        swf (function): An implementation of a voting method. The function should accept a Profile, ProfileWithTies, MajorityGraph, and/or MarginGraph, and a keyword parameter ``curr_cands`` to find the winner after restricting to ``curr_cands``. 
        name (string): The Human-readable name of the social welfare function.

    """
    def __init__(self, swf, name = None): 
        
        self.swf = swf
        self.name = name
        functools.update_wrapper(self, swf)   

    def __call__(self, edata, curr_cands = None, **kwargs):

        if (curr_cands is not None and len(curr_cands) == 0) or len(edata.candidates) == 0: 
            return []
        return self.vm(edata, curr_cands = curr_cands, **kwargs)
        
    def set_name(self, new_name):
        """Set the name of the social welfare function."""

        self.name = new_name

    def __str__(self): 
        return f"{self.name}"

def swf(name = None):
    """
    A decorator used when creating a social welfare function. 
    """
    def wrapper(f):
        return SWF(f, name=name)
    return wrapper

@jit(nopython=True, fastmath=True)
def isin(arr, val):
    """compiled function testing if the value val is in the array arr
    """
    
    for i in range(arr.shape[0]):
        if (arr[i]==val):
            return True
    return False