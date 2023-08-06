#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 23:29:05 2021
@author: nahuel
"""

"""
Abstract class defining a model:
    it must offer access to the relevant physical variables:
        luminosity [foe/s], fluence [MeV/s], Eavg [MeV], E2avg [MeV^2], alpha
"""

import numpy as np
import scipy.integrate
from scipy.special import gamma
from ResNova.GenericSource import GenericSource

class SNModel(GenericSource):
    def __init__(self, name, distance = 10.):
        '''
        

        Parameters
        ----------
        name : str
            Name of the model.
        distance : float, optional
            SN distance in kpc. The default is 10..

        Returns
        -------
        None.

        '''
        self.name = name
        #distance from kpc to m
        self.distance = distance*3.08567758e+19

    def luminosity(self, time: float) -> float:
        '''
        

        Parameters
        ----------
        time : float
            Time in seconds at which the luminosity is returned.

        Returns
        -------
        float
            Luminosity in foe/s.

        '''
        pass
    
    def fluence(self, time: float) -> float:
        '''
        

        Parameters
        ----------
        time : float
            Time in seconds at which the fluence is returned.

        Returns
        -------
        float
            fluence in GeV/s.

        '''
        pass
    
    def Eavg(self, time: float) -> float:
        '''
        

        Parameters
        ----------
        time : float
            Time in seconds at which the average neutrino energy is returned.

        Returns
        -------
        float
            average neutrino energy in MeV.

        '''
        pass
    
    def E2avg(self, time: float) -> float:
        '''
        

        Parameters
        ----------
        time : float
            Time in seconds at which the quadratic average 
            neutrino energy is returned.

        Returns
        -------
        float
            quadratic average neutrino energy in MeV^2.

        '''
        pass
    
    def alpha(self, time: float) -> float:
        '''
        

        Parameters
        ----------
        time : float
            Time in seconds at which the pinching parameter is returned.

        Returns
        -------
        float
            pinching parameter.

        '''
        pass
    
    def SetTimeInterval(self, t = (float, float)):
        '''
        

        Parameters
        ----------
        t : (float, float)
            time interval to consider the SN as a static source
            (astrophysical quantities are averaged over the interval)

        Returns
        -------
        None.

        '''
        self.alpham = scipy.integrate.quad(
                self.alpha, t[0], t[1]
                )[0]/(t[1] - t[0])
        self.Eavgm = scipy.integrate.quad(
                self.Eavg, t[0], t[1]
                )[0]/(t[1] - t[0])    
        self.Lm = scipy.integrate.quad(
                self.fluence, t[0], t[1]
                )[0]/(t[1] - t[0]) 
        
    def phi(self, Enu: float, t: float) -> float:
        '''
        

        Parameters
        ----------
        Enu : float
            Neutrino energy in GeV.
        t: float
            Time is seconds at which the distribution is computed. If t is None, static
            values will be used

        Returns
        -------
        float
            Distribution function of emitted neutrinos, unit normalized.

        '''
        if t == None:
            alpha = self.alpham
            Em = self.Eavgm
        else:
            alpha = self.alpha(t)
            Em = self.Eavg(t)
            
        norm = gamma(alpha + 1)/((alpha+1)/Em)**(alpha+1)/Em**alpha
        return 1/norm*(Enu/Em)**alpha*np.exp(-(alpha+1)*Enu/Em)
    
    def flux(self, Enu: float, t: float = None):
        '''
        

        Parameters
        ----------
        Enu : float
            Neutrino energy in GeV.
        t : float 
            Time is seconds at which the flux is computed.
            
        Returns
        -------
        float
            Flux of neutrinos of given energy at distance d, at time t
            in neutrinos/GeV/m^2/s.

        '''
        
        if t == None:
            L = self.Lm
            Eavg = self.Eavgm
        else:
            L = self.fluence(t)
            Eavg = self.Eavg(t)
        
            
        return L/4/np.pi/(self.distance)**2/Eavg*\
            self.phi(Enu, t)
    