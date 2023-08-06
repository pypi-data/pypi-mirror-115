#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 00:43:13 2021

@author: nahuel
"""

import numpy as np
#fermi constant [GeV^-2];
GF = 1.1663787e-5 

def WeakCharge(A: float, Z: float) -> float:
    '''
    

    Parameters
    ----------
    A : float
        Atomic mass number.
    Z : int
        Atomic number.

    Returns
    -------
    float
        Absolute value of the nuclear weak charge.

    '''
    N = float(A) - float(Z)
    return np.abs(float(N)-0.0599*float(Z))

class TargetElement:
    def __init__(self, A: float, Z: float, name: str, s = 0.9):
        '''
        

        Parameters
        ----------
        A : float
            Atomic mass number of the target element (amu).
        Z : int
            Atomic number of the target element.
        name: str
            Name of the species
        s : float
            Nuclear skin thickness [fm].

        Returns
        -------
        None.

        '''
        self.A = A
        self.Z = Z
        self.Qw = WeakCharge(A, Z)
        self.s = s
        self.Mn = 0.9315*float(A)#931.5*1e3*float(A)
        self.name = name
    
    def Helm_Form_Factor2(self, Er: float):
        '''
        

        Parameters
        ----------
        Er : float
            Recoil energy [GeV].

        Returns
        -------
        TYPE
            Helm form factor squared at energy Er.

        '''
        amu = 931.5*1e+9
        A = self.A
        #Convert recoil energy to momentum transfer q in keV
        q1 = np.sqrt(2*A*amu*Er)
    
        #Convert q into fm^-1
        q2 = q1*(1e-12/1.97e-7)
    
        #Calculate nuclear parameters
        s = self.s
        a = 0.52
        c = 1.23*(A**(1.0/3.0)) - 0.60
        R1 = np.sqrt(c*c + 7*np.pi*np.pi*a*a/3.0 - 5*s*s)

        #Calculate form factor
        x = q2*R1
        J1 = np.sin(x)/(x*x) - np.cos(x)/x
        F = 3*J1/x
     
        return (F*F)*(np.exp(-(q2*q2*s*s)))
    

    def Ermax(self, Enu: float):
        '''
        

        Parameters
        ----------
        Enu : float
            Energy of the incoming neutrino [GeV].

        Returns
        -------
        float
            Maximum recoil energy given Enu [GeV].

        '''
        return 2*Enu**2/(self.Mn)

    def Enumin(self, Er: float):
        '''
        

        Parameters
        ----------
        Er : float
            Recoil energy [GeV].

        Returns
        -------
        float
            Minimum incoming neutrino energy needed to induce a recoil
            of energy Enumin [GeV].

        '''
        return np.sqrt(self.Mn*Er/2)
    
    def dSigmaCNNSdEr(self, Er: float, Enu: float) -> float:
        '''
        

        Parameters
        ----------
        Er : float
            Recoiling energy [GeV].
        Enu : float
            Incident neutrini energy [GeV].

        Returns
        -------
        float
            cross-section [cm^2/GeV].

        '''
        #GeV^-2 -> cm^2, Fermi, weakcharge, mass number, kinematics, nuclear form
        return 389.4*1e-30*GF**2/(4.*np.pi)*self.Qw**2*self.Mn*\
        (1.-np.divide(
            self.Mn*Er,(2*Enu**2), 
            out = np.zeros_like(Er), where=Er!=0))*\
            self.Helm_Form_Factor2(Er)*(Er <= self.Ermax(Enu))
class CompositeTarget:
    def __init__(self, elements, subscripts):
        '''
        

        Parameters
        ----------
        elements : list of TargetElement
            List containing TargetElements to be considered in the composite
            material.
        subscript : list of ints
            List of molecular subscripts fo each element, indicating the
            number of each species present in one molecule.


        Returns
        -------
        None.

        '''
        if any(type(i) != type(TargetElement(0, 0, '')) for i in elements):
            raise TypeError('elements must be a list of TargetElements')
        if any(type(i) != int 
               for i in subscripts):
            raise TypeError('subscripts must be a list of\
                            ints')
        if len(elements) != len(subscripts):
            raise ValueError('lengths of elements and subscripts \
                             must be equal')                  
        self.elements = elements
        self.subscripts = subscripts
        self.relative_mass = {}
        tot = 0.
        for i in range(len(elements)):
            tot += elements[i].A*subscripts[i]
        #molar mass in kg
        self.molar_mass = 1e-3*tot
        for idx, i in enumerate(elements):
            self.relative_mass[i.name] = i.A*subscripts[idx]/tot 
        
TargetPb = TargetElement(A = 208, Z = 82, name = 'Pb')
TargetCa = TargetElement(A = 40, Z = 20, name = 'Ca')
TargetW = TargetElement(A = 183.8, Z = 74, name = 'W')
TargetO = TargetElement(A = 16, Z = 8, name = 'O')
TargetXe = TargetElement(A = 131.3, Z = 54, name = 'Xe')

PbWO4 = CompositeTarget([TargetPb, TargetW, TargetO], [1, 1, 4])
CaWO4 = CompositeTarget([TargetCa, TargetW, TargetO], [1, 1, 4])
MetallicPb = CompositeTarget([TargetPb], [1])
Xe = CompositeTarget([TargetXe], [1])