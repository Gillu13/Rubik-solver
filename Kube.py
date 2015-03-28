# -*- coding: utf-8 -*-
"""
This files contains some useful definitions to solve the Rubik's cube.

functions
---------

rand_move: randomly generates a list of chars representing a list of 
fundamental Rubik's cube moves

move_list_to_state: returns the state of the Rubik's cube from a list a chars
corresponding to a list consecutive fundamental moves

solve: solves the Rubk's cube from a given state

Notes
-----

Created on Thu Dec 11 22:22:17 2014

@author: Gilles Aouizerate
"""

import numpy as np
import random as rd

import utilities as utl

# define the fundamental moves and store them 

F = utl.move(P8 = [0,2,6,4], P12 = [4,1,6,9], P3 = [1,2,1,2], P2 = [1,1,1,1],
             seq = ["F"])
f = F**(-1)
R = utl.move(P8 = [4,6,7,5], P12 = [8,9,11,10], P3 = [1,2,1,2], P2 = [0,0,0,0],
             seq = ["R"])
r = R**(-1)
U = utl.move(P8 = [6,2,3,7], P12 = [6,3,7,11], P3 = [0,0,0,0], P2 = [0,0,0,0],
             seq = ["U"])
u = U**(-1)
B = utl.move(P8 = [1,5,7,3], P12 = [7,2,5,10], P3 = [2,1,2,1], P2 = [1,1,1,1],
             seq = ["B"])
b = B**(-1)
L = utl.move(P8 = [0,1,3,2], P12 = [0,2,3,1], P3 = [2,1,2,1], P2 = [0,0,0,0],
             seq = ["L"])
l = L**(-1)
D = utl.move(P8 = [0,4,5,1], P12 = [0,4,8,5], P3 = [0,0,0,0], P2 = [0,0,0,0],
             seq = ["D"])
d = D**(-1)

fund = {}
fund['F'] = F
fund['f'] = f
fund['R'] = R
fund['r'] = r
fund['U'] = U
fund['u'] = u
fund['B'] = B
fund['b'] = b
fund['L'] = L
fund['l'] = l
fund['D'] = D 
fund['d'] = d


# enlarged list of fundamental moves
fund_l = [F, F**2, f, R, R**2, r, U, U**2, u, B, B**2, b, L, L**2, l, D,
          D**2, d]

# moves that have special useful behaviors    
    
M0 = (F*utl.commutator(U,L))**3
M1 = (f*L)**3*(F*l)**3
M20 = U**2*F*b*L**2*f*B 
M21 = B**2*R*l*U**2*r*L 
M22 = U**2*R*l*F**2*r*L 
M23 = B**2*D*u*R**2*d*U 
M30 = l*R*F*l*R*D*l*R*B*B*r*L*D*r*L*F*r*L*U*U 
M31 = b*F*D*b*F*R*b*F*U*U*f*B*R*f*B*D*f*B*L*L 

# useful functions


def move_list_to_state(actions):
    """Returns the state of the Rubik's cube from a list a chars corresponding
    to a list consecutive fundamental moves.
    
    Paramters
    ---------
    
    actions: char list, corresponding to a list of names of consecutive 
    fundamental moves
    
    """
    M = utl.move(seq = [])

    for a in actions:
        M = fund[a]*M
    
    X = range(8)+range(12)
    for i in range(8):
        X = X + range(3)
    for i in range(12):
        X = X + range(2)  
    X = np.transpose(np.matrix(np.array(X)))
    res = M.M*X    
    
    return res


def solve(state):
    """Solves the Rubk's cube from a given state.
    
    Parameters
    ----------
    
    state: array 68x1 matrix representing the state of the Rubik's cube to 
    solve
    
    """

    Y = np.matrix(np.copy(state))

    Y1 = Y[:8]

    res1 = utl.solve_corner_pos(Y1, M0, 1, 3, fund_l)
    Y = res1.M*Y
    Y2 = Y[(8+12):(4*8+12)]
    res2 = utl.pivot_corner_cubies(Y2, M1, 2, fund_l)
    Y = res2.M*Y
    Y3 = Y[8:(8+12)]
    res3 = utl.solve_edge_pos(Y3, [M20, M21, M22, M23], [[0, 3, 11], [5, 6, 7], 
                          [4, 6, 7], [2, 9, 10]], fund_l)
    Y = res3.M*Y
    Y4 = Y[(4*8+12):]
    res4 = utl.pivot_edge_cubies(Y4, M31, 3, fund_l)
    
    res = res4*res3*res2*res1    
    
    print "I solved the Rubik's cube in {0} moves!".format(len(res.decompo))
    
    return res.decompo


def rand_move(num_move = 200):
    """Generates a list of chars randomly picked among the names of fundamental
    moves.
    
    Parameters
    ----------
    
    num_move: (optional) int, length of the desired list
    
    """
    return [rd.choice(["F", "f", "B", "b", "R", "r", "U", "u", "L", "l", "D",
                       "d" ]) for i in range(num_move)]