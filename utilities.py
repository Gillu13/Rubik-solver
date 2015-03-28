# -*- coding: utf-8 -*-
"""
utility files.

Classes
--------

move class: formalizes Rubik's cube moves

functions
---------

T: transposition function (permutation of two elements of the set of the N 
first natural numbers)

Rq: Generates the array 3x3 matrix of the rotation of a given angle about a 
given vector

conjugate: generates the conjugate of two move elements

commutator: generates the commutator of two move elements

Examples
--------

>>> import utilities as utl
>>> M = utl.move()
>>> A = utl.T(8, 0, 1)

Notes
-----

Created on Thu Dec 11 21:35:39 2014

@author: Gilles Aouizerate 
"""

import numpy as np

from scipy import linalg


def Rq(theta, vect):
    """Returns a 3x3 matrix representing a rotation of angle theta about vect 
    axis.
    
    Parameters
    ----------
    
    theta: float, rotation angle in radian
    
    vect: list of float or array, vector about which the rotation happens
    
    """
    I = np.matrix(np.identity(3))
    Q = np.matrix(np.zeros((3,3)))
    Q[0,1] = -vect[2]
    Q[0,2] = vect[1]
    Q[1,2] = -vect[0]
    Q[1,0] = -Q[0,1]
    Q[2,0] = -Q[0,2]
    Q[2,1] = -Q[1,2]
    res = I + np.sin(theta)*Q + (1-np.cos(theta))*Q**2
    return res


def conjugate(A,G):
    """Returns a move object corresponding to the conjugate of move A by move G
    
    Parameters
    ----------
    
    A : a move object
    
    G : a move object
    
    Notes
    -----
    
    http://en.wikipedia.org/wiki/Conjugacy_class
    
    
    """
    return G*A*G**(-1)


def commutator(A, B):
    """Returns a move object corresponding to the commutator of moves A and B
    
    Parameters
    ----------
    
    A : a move object
    
    B : a move object
    
    Notes
    -----
    
    http://en.wikipedia.org/wiki/Commutator
    
    
    """
    return B**(-1)*A**(-1)*B*A
    

def T(N, i, j):
    """Transposition matrix
    
    returns a NxN transposition matrix corresponding to the permutation of 
    the ith and jth elements of a set of N ordered numbers.
    
    Parameters
    ----------
    
    N : strictly positive integer corresponding to the size of the set of 
    elements on which permutations are performed.
    
    i : integer smaller than N corresponding to the position of one of the 
    permuting elements
    
    j : integer smaller than N a d different from i corresponding to the 
    position of one of the permuting elements
    
    Examples
    --------

    >>> import utilities as utl
    >>> A = utl.T(8, 0, 1)
    
    
    """
    res = np.matrix(np.eye(N))
    res[i, i] = 0
    res[j, j] = 0
    res[i, j] = 1
    res[j, i] = 1
    return res


class move():
    """A move object formalizes a Rubik's cube move. It is seen as:
        * A permutation of the 8 corner cubies regarless of orientation
        * For each corner cubie a permutation of its 3 possible orientations
        * A permutation of the 12 edge cubies regarless of orientation
        * For each edge cubie a permutation of its 2 possible orientations

    Attributes
    ----------
    A8 : array 8x8 matrix representing the permutations of the 8 corner cubies
    
    A12 : array 12x12 matrix representing the permutations of the 12 edge 
    cubies
    
    Notes
    -----
    
    This is greatly inspired by Janet Chen course notes "Group Theory and the 
    Rubik's cube" [1]_
        
    
    .. [1] Janet Chen, "Group Theory and the Rubik's cube", http://www.math.ha\
rvard.edu/~jjchen/docs/Group%20Theory%20and%20the%20Rubik%27s%20Cube.pdf
    
    """
    def __init__(self, **kwargs):
        """Initializes a move object
        
        Parameters
        ----------
        
        kwargs:

        * M8: 8x8 array matrix representing a permutation of the 8 corner 
        cubies
        
        * M3: 24x24 diagonal block array matrix. Each 3x3 diagonal element
        represents a permutation of the orientation of a corner cuby
        
        * M12: 12x12 array matrix representing a permutation of the 12 edge 
        cubies
        
        * M2: 24x24 diagonal block array matrix. Each 2x2 diagonal element
        represents a permutation of the orientation of a edge cuby
        
        * P8 : list of integers representing the cycle notation of a 
        permutation of the 8 corner cubies
        
        * P3 : list of integers representing a permutation of the orientations 
        of the 8 corner cubies as described in [1]
        
        * P12 : list of integers representing the cycle notation of a 
        permutation of the 12 edge cubies
        
        * P2 : list of integers representing a permutation of the orientations 
        of the 12 edge cubies as described in [1]
        
        * seq : list of characters, corresponding to the decomposition of the 
        move in fundamental moves
        
        Examples
        --------

        >>> import utilities as utl
        >>> A = utl.move(P8 = [0,2,6,4], P12 = [4,1,6,9], P3 = [1,2,1,2], 
                         P2 = [1,1,1,1], seq = ["F"])
        
        """        
        if 'M8' in kwargs and 'M3' in kwargs:   
            self.A8 = np.matrix(np.copy(kwargs['M8']))
            #self.S3 = [np.matrix(np.copy(i)) for i in kwargs['M3']]
            self.S3 = np.matrix(np.copy(kwargs['M3']))
        elif 'P8' in kwargs and 'P3' in kwargs:
            p8 = kwargs['P8']
            p3 = kwargs['P3']
            self.A8 = T(8, p8[0], p8[3])*T(8, p8[0], p8[2])*T(8, p8[0], p8[1])
            s3 = [np.matrix(np.eye(3)) for i in range(8)]
            for i in range(len(p3)):
                s3[p8[i]]= (T(3,0,2)*T(3,0,1))**p3[i]
            y=self.A8*np.transpose(np.matrix(np.array(range(8))))
            self.S3=np.matrix(np.zeros([3*8,3*8]))
            for i in range(8):
                self.S3[(3*i):(3*i+3),(3*int(y[i])):(3*int(y[i])+3)] = s3[i]
        else:
            self.A8 = np.matrix(np.eye(8))
            self.S3 = np.matrix(np.eye(3*8))
        
        
        if 'M12' in kwargs and 'M2' in kwargs:   
            self.A12 = np.matrix(np.copy(kwargs['M12']))
            #self.S2 = [np.matrix(np.copy(i)) for i in kwargs['M2']]
            self.S2 = np.matrix(np.copy(kwargs['M2']))
        elif 'P12' in kwargs and 'P2' in kwargs:
            p12 = kwargs['P12']
            p2 = kwargs['P2']
            self.A12 = T(12, p12[0], p12[3])*T(12, p12[0], p12[2])*T(12, 
                p12[0], p12[1])
            s2 = [np.matrix(np.eye(2)) for i in range(12)]
            for i in range(len(p2)):
                s2[p12[i]]= T(2,0,1)**p2[i]
            y=self.A12*np.transpose(np.matrix(np.array(range(12))))
            self.S2=np.matrix(np.zeros([2*12,2*12]))
            for i in range(12):
                self.S2[(2*i):(2*i+2),(2*int(y[i])):(2*int(y[i])+2)] = s2[i]
        else:
            self.A12 = np.matrix(np.eye(12))
            self.S2 = np.matrix(np.eye(2*12)) 

        
        try:
            self.decompo = kwargs['seq']
        except NameError:
            print "to build a move object a list of characters, corresponding \
            to the decomposition of the move in fundamental moves, must be \
            provided."
                        
      
        self.make_M()


    def make_M(self):
        res = linalg.block_diag(self.A8, self.A12)
        res = linalg.block_diag(res, self.S3)
        res = linalg.block_diag(res, self.S2)
        self.M = np.matrix(res)
    
    
    def __pow__(self, expo):
        if (isinstance(expo, int) and (expo > -2)):
            if expo == 0:
                return move(seq = [])
            elif expo == -1:
                s = []
                for i in range(len(self.decompo)):
                    A = self.decompo[-1-i]
                    if A == A.upper():
                        a = A.lower()
                    else:
                        a = A.upper()
                    s = s+[a]
            else:
                s=[]
                for i in range(expo):
                    s=s+self.decompo                
        else:
            raise ValueError("expo has to be an integer greater or equal \
            to -1")
        return move(M8 = self.A8**expo, M12 = self.A12**expo, 
                    M3 = self.S3**expo, 
                    M2 = self.S2**expo,
                    seq = s)
    
    
    def __mul__(self, other):
        return move(M8 = self.A8*other.A8, M12 = self.A12*other.A12, 
                    M3 = self.S3*other.S3, 
                    M2 = self.S2*other.S2,
                    seq = other.decompo + self.decompo)
                    
    
    def __str__(self):
        X = range(8)+range(12)
        for i in range(8):
            X = X + range(3)
        for i in range(12):
            X = X + range(2)  
        X = np.transpose(np.matrix(np.array(X)))
        Y = self.M*X
#        corner_index = [Y[i] for i in range(8)]
#        edge_index = [Y[i+8] for i in range(12)]
        corner_pos = [int(Y[i]) for i in range(8)]
        edge_pos = [int(Y[i+8]) for i in range(12)]
        corner_value = [int(Y[3*int(i)+8+12]) for i in range(8)]
        edge_value = [int(Y[2*int(i)+4*8+12]) for i in range(12)]
        return format(corner_pos)+'\n'+format(edge_pos)+'\n'+\
        format(corner_value)+'\n'+format(edge_value)

        
def send_8(cb1, cb2, cl1, cl2, auth, maxMove = 5, n_combi = 1, 
           prev = [move(seq = [])]):
    """Returns a move that sends corner cubies cb1 and cb2 to corner cubicles
    cl1 and cl2 or to cubicles cl2 and cl1
    
    """
    if n_combi > maxMove:
        print "Oops!.. The maximum number of allowed moves is reached ({0}). \
        If you want to go further, you have to set MaxMove to some greater \
        value".format(maxMove)
        return None
    Y = np.transpose(np.matrix(np.array(range(8))))
    if n_combi == 1:
        fact = [move(seq = [])] + auth
    else:
        fact = auth
    cur = []
    for m in fact:
        for g in prev:
            if n_combi == 1:
                cur.append(m*g)
            else:
                if not((m.decompo[0].upper()==m.decompo[0] and 
                g.decompo[-1]==m.decompo[0].lower()) or (m.decompo[0].lower()
                ==m.decompo[0] and g.decompo[-1]==m.decompo[0].upper()) 
                or m.decompo[0]==g.decompo[-1]):
                    cur.append(m*g)
    
    for m in cur:
        y = m.A8*Y
        if (((y[cl1]==cb1) and (y[cl2]==cb2)) or ((y[cl1]==cb2) and 
        (y[cl2]==cb1))):
            return m
    return send_8(cb1, cb2, cl1, cl2, auth, maxMove, n_combi+1, 
           [m for m in cur if m.decompo!=[]])


def send_8_slow(cb1, cb2, cl1, cl2, auth, maxMove = 5, n_combi = 1, 
           prev = [move(seq = [])]):
    """Returns a move that sends corner cubies cb1 and cb2 respectively to 
    corner cubicles cl1 and cl2
    
    """
    if n_combi > maxMove:
        print "Oops!.. The maximum number of allowed moves is reached ({0}). \
        If you want to go further, you have to set MaxMove to some greater \
        value".format(maxMove)
        return None
    Y = np.transpose(np.matrix(np.array(range(8))))
    if n_combi == 1:
        fact = [move(seq = [])] + auth
    else:
        fact = auth
    cur = []
    for m in fact:
        for g in prev:
            if n_combi == 1:
                cur.append(m*g)
            else:
                if not((m.decompo[0].upper()==m.decompo[0] and 
                g.decompo[-1]==m.decompo[0].lower()) or (m.decompo[0].lower()
                ==m.decompo[0] and g.decompo[-1]==m.decompo[0].upper()) 
                or m.decompo[0]==g.decompo[-1]):
                    cur.append(m*g)
    
    for m in cur:
        y = m.A8*Y
        if ((y[cl1]==cb1) and (y[cl2]==cb2)):
            return m
    return send_8_slow(cb1, cb2, cl1, cl2, auth, maxMove, n_combi+1, 
           [m for m in cur if m.decompo!=[]])


def send_12(cb1, cb2, cb3, cl1, cl2, auth, maxMove = 3, n_combi = 1, 
           prev = [move(seq = [])]):
    """Returns a move that sends edge cubies cb1, cb2 and cb3 respectively
    to edge cubicles cl1, cl2 and cl3
    
    """
    if n_combi > maxMove:
#        print "Oops!.. The maximum number of allowed moves is reached ({0}). \
#If you want to go further, you have to set MaxMove to some greater \
#value".format(maxMove)
        return None
    Y = np.transpose(np.matrix(np.array(range(12))))
    if n_combi == 1:
        fact = [move(seq = [])] + auth
    else:
        fact = auth
    cur = []
    for m in fact:
        for g in prev:
            if n_combi == 1:
                cur.append(m*g)
            else:
                if not((m.decompo[0].upper()==m.decompo[0] and 
                g.decompo[-1]==m.decompo[0].lower()) or (m.decompo[0].lower()
                ==m.decompo[0] and g.decompo[-1]==m.decompo[0].upper()) 
                or m.decompo[0]==g.decompo[-1]):
                    cur.append(m*g)
    for m in cur:
        y = m.A12*Y
        if ((y[cl1]==cb1) and (y[cl2]==cb2) and (float(cb3) in y[(cl1+1):])):
            return m
    return send_12(cb1, cb2, cb3, cl1, cl2, auth, maxMove, n_combi+1, 
           [m for m in cur if m.decompo!=[]])    


def send_12_slow(cb1, cb2, cl1, cl2, auth, maxMove = 3, n_combi = 1, 
           prev = [move(seq = [])]):
    """Returns a move that sends edge cubies cb1 and cb2 respectively
    to edge cubicles cl1 and cl2
    
    """
    if n_combi > maxMove:
        print "Oops!.. The maximum number of allowed moves is reached ({0}). \
If you want to go further, you have to set MaxMove to some greater \
value".format(maxMove)
        return None
    Y = np.transpose(np.matrix(np.array(range(12))))
    if n_combi == 1:
        fact = [move(seq = [])] + auth
    else:
        fact = auth
    cur = []
    for m in fact:
        for g in prev:
            if n_combi == 1:
                cur.append(m*g)
            else:
                if not((m.decompo[0].upper()==m.decompo[0] and 
                g.decompo[-1]==m.decompo[0].lower()) or (m.decompo[0].lower()
                ==m.decompo[0] and g.decompo[-1]==m.decompo[0].upper()) 
                or m.decompo[0]==g.decompo[-1]):
                    cur.append(m*g)
    for m in cur:
        y = m.A12*Y
        if ((y[cl1]==cb1) and (y[cl2]==cb2)):
            return m
    return send_12_slow(cb1, cb2, cl1, cl2, auth, maxMove, n_combi+1, 
           [m for m in cur if m.decompo!=[]])    


def solve_corner_pos(Y, switcher, c1, c2, auth):
    """Returns a move that brings back the corner cubies from the position Y
    to their unoriented starting position.
    
    """
    y = np.matrix(np.copy(Y))
    res = move(seq =[])
    for i in range(8):
        if y[i]!=i:
            j = [k for k in range(i+1,len(y)) if int(y[k])==i][0]
            G = send_8(c1, c2, i, j, auth)
            next_move = conjugate(switcher, G)
            res = next_move*res
            y = next_move.A8*y

    return res


def pivot_corner_cubies(Y, flipper, c2, auth):
    """Returns a move that brings back the corner cubies from the orientation Y
    to their starting orientation without changing their position.
    
    """
    y = np.matrix(np.copy(Y))
    res = move(seq =[])
    for i in range(1,8):
        if y[3*i]==2:
            G = send_8_slow(0, c2, 0, i, auth)
            next_move = conjugate(flipper, G)
            res = next_move*res
            y = next_move.S3*y
        elif y[3*i]==1:
            G = send_8_slow(0, c2, 0, i, auth)
            next_move = conjugate(flipper, G)**2
            res = next_move*res
            y = next_move.S3*y
    return res        

    
def solve_edge_pos(Y, switcher_l, c_l, auth):
    """Returns a move that brings back the corner cubies from the position Y
    to their unoriented starting position.
    
    """
    y = np.matrix(np.copy(Y))
    res = move(seq =[])
    for i in range(10):
        if y[i]!=i:
            j = [k for k in range(i+1,len(y)) if int(y[k])==i][0]
            for k in range(len(c_l)):
                G = send_12(c_l[k][0], c_l[k][1], c_l[k][2], i, j, auth)
                if G!=None:
                    next_move = conjugate(switcher_l[k], G)
                    break
#                else:
#                    print "I was not able to use the edge switcher number {0},\
# I am trying the next one".format(k)
            res = next_move*res
            y = next_move.A12*y

    return res


def pivot_edge_cubies(Y, flipper, c2, auth):
    """Returns a move that brings back the edge cubies from the orientation Y
    to their starting orientation without changing neither their position nor 
    any other cubie.
    
    """
    y = np.matrix(np.copy(Y))
    res = move(seq =[])
    for i in range(1,12):
        if y[2*i]!=0:
            G = send_12_slow(0, c2, 0, i, auth)
            next_move = conjugate(flipper, G)
            res = next_move*res
            y = next_move.S2*y
    return res 