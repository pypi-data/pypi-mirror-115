#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 14:23:57 2021

@author: nahuel
"""

import scipy.integrate
import numpy as np

from ResNova.GenericSource import GenericSource
from ResNova.Target import CompositeTarget

class Detector:
    def __init__(self, name: str, 
                 model, 
                 target: CompositeTarget, 
                 mass = 1000.,
                 energy_resolution = 0.2,
                 energy_threshold = 1.,
                 time_resolution = 200e-3):
        '''
        

        Parameters
        ----------
        name : str
            Name of the detector
        model : list of GenericSource
            List of models.
        target : CompositeTarget
            Target material.
        mass : mass, optional
            detectors mass in kg. The default is 1000..
        energy_resolution : float, optional
            nuclear recoil energy resolution in keV. The default is 0.2.
        energy_threshold : float, optional
            nuclear recoil energy threshold in keV. The default is 1.

        Returns
        -------
        None.

        '''
        self.name = name
        self.model = model
        self.mass = mass
        self.target = target
        self.energy_resolution = energy_resolution
        self.energy_threshold = energy_threshold
        self.time_resolution = time_resolution
    
    def recoil_spectrum(self, Er: float, t: float = None) -> float:
        '''
        

        Parameters
        ----------
        Er : float
            Recoil energy in GeV.
        t: float
            Time at which the flux is evaluated
        Returns
        -------
        dictionary
            counts/GeV/s for the given detector mass per model and the sum
            with key name 'sum'.

        '''

        allrates = {}

        for mod in self.model:
            rate_per_element = np.zeros_like(self.target.elements)
            for idx, El in enumerate(self.target.elements):
                rate_per_element[idx] = self.mass*self.target.relative_mass[El.name]*1000/El.A*\
                    6.02214076e+23*\
                np.vectorize(
                    lambda y: scipy.integrate.quad(
                        lambda x: mod.flux(x, t=t)*1e-4*\
                            El.dSigmaCNNSdEr(Er = y, Enu = x),
                        El.Enumin(y), 0.05)[0]
                    )(Er)
            allrates[mod.name] = np.sum(rate_per_element)
        allrates['sum'] = 0
        for mod in self.model:
            allrates['sum'] += allrates[mod.name]
        return allrates
    
    def recoil_rate(self, t: float = None) -> float:
        '''
        

        Parameters
        ----------
        t : float
            time in s.
        Returns
        -------
        dictionary
            counts/s for the given detector mass.

        '''

        allrates = {}

        for mod in self.model:
            cr = np.zeros_like(self.target.elements)
            for idx, El in enumerate(self.target.elements):
                cr[idx] = self.mass*self.target.relative_mass[El.name]*1000/El.A*\
                    6.02214076e+23*\
                np.vectorize(
                    lambda z: scipy.integrate.nquad(
                        lambda x, y: mod.flux(Enu = x, t = z)*1e-4*\
                            El.dSigmaCNNSdEr(Er = y, Enu = x),
                        [ [0,0.10], [self.energy_threshold*1e-6, 20e-6]])[0]
                    )(t)
            allrates[mod.name] = np.sum(cr) 
        allrates['sum'] = 0
        for mod in self.model:
            allrates['sum'] += allrates[mod.name]
        return allrates
    