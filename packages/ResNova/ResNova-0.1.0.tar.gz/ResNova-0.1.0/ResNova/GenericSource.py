#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:31:16 2021

@author: nahuel
"""

class GenericSource:
    def __init__(self, name):
        self.name = name
        pass
    
    def flux(self, Enu: float, t: float = None) -> float:
        '''
        

        Parameters
        ----------
        Enu : float
            Particle energy in GeV.
        t: float
            Time in s
            
        Returns
        -------
        float
            Flux of neutrinos 
            in particles/GeV/m^2/s.

        '''
        pass