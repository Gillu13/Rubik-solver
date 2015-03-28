# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 22:06:08 2014

@author: Gilles Aouizerate
"""

import numpy as np


class quaternion():
    """A simple quaternion class in order to represent a rotation.
    
    To build a quaternion object, one needs to input either the angle and 
    the unit vector about which the rotation happens or directly the scalar
    and vector parts of the quaternion.
    
    Examples
    --------
    
    >>> import quaternion as quat
    >>> Q1 = quat.quaternion([1.,0.,0.], angl = 90.)
    >>> Q2 = quat.quaternion([(0.5)**0.5,0.,0.], W = (0.5)**0.5)
    
    Notes
    -----
        
    See Eugene Salamin: "Application of Quaternions to Computation with 
    Rotations", Working Paper, Stanford AI Lab, 1979.
        
    """
    
    def __init__(self, vect, **kwargs):
        """Initializes a quaternion object
        
        Parameters
        ----------
        
        vect: list of float, depending on kwargs it is be either the 
        coordonates of the unit vector about which the rotation happens or  
        directly the vector part of the quaternion
        
        \**kwargs:

        * angl: float, the angle of rotation represented by the quaternion.
        * W: float,the scalar part of the quatenion object.         
                
        """
        for name, value in kwargs.items():
            if name=='angl':
                self.w = np.cos(value/2.*np.pi/180.)
                self.x = vect[0]*np.sin(value/2.*np.pi/180.)
                self.y = vect[1]*np.sin(value/2.*np.pi/180.)
                self.z = vect[2]*np.sin(value/2.*np.pi/180.)
            elif name=='W':
                self.w = value
                self.x = vect[0]
                self.y = vect[1]
                self.z = vect[2]
        self.set_matrix()
    
    
    def set_matrix(self):
        self.matrix = np.zeros([4,4])
    
        self.matrix[0,0] = self.w**2+self.x**2-self.y**2-self.z**2
        self.matrix[1,1] = self.w**2-self.x**2+self.y**2-self.z**2
        self.matrix[2,2] = self.w**2-self.x**2-self.y**2+self.z**2
    
        self.matrix[0,1] = 2*self.x*self.y-2*self.w*self.z
        self.matrix[0,2] = 2*self.x*self.z+2*self.w*self.y
    
        self.matrix[1,0] = 2*self.x*self.y+2*self.w*self.z
        self.matrix[1,2] = 2*self.y*self.z-2*self.w*self.x
    
        self.matrix[2,0] = 2*self.x*self.z-2*self.w*self.y
        self.matrix[2,1] = 2*self.y*self.z+2*self.w*self.x   
        self.matrix[3,3] = 1.    
        
        
    def __mul__(self, other):
        w1 = self.w
        x1 = self.x
        y1 = self.y
        z1 = self.z
            
        w2 = other.w
        x2 = other.x
        y2 = other.y
        z2 = other.z
        
        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2
        
        return quaternion(np.array([x, y, z]), W = w)