# -*- coding: utf-8 -*-
"""
Animated representation of a Rubik's cube using PyOpenGL library.

Description
-----------

Running this program will display a window that is a graphical representation
of a Rubik's cube.

By following the instructions on screen one can change the camera point of 
view, randomly move the cube and of course watch the magic of a mathematical
resolution of the cube.

Usage
-----

Just run this script, when a window with a Rubik's cube pops up you may 
control it by using your keyboard. In particular you can:
    * Change the camera point of view by using the arrow keys
    * Randomly move the cube by pressing the `a` key
    * Solve the cube by pressing the `s` key
    * Move the front face in the clockwise (respectively counterclockwise) 
    direction when pressing the `F` (resp. `f`) key
    * Move the back face in the clockwise (respectively counterclockwise) 
    direction when pressing the `B` (resp. `b`) key
    * Move the right face in the clockwise (respectively counterclockwise) 
    direction when pressing the `R` (resp. `r`) key
    * Move the left face in the clockwise (respectively counterclockwise) 
    direction when pressing the `L` (resp. `l`) key
    * Move the upper face in the clockwise (respectively counterclockwise) 
    direction when pressing the `U` (resp. `u`) key
    * Move the downer face in the clockwise (respectively counterclockwise) 
    direction when pressing the `D` (resp. `d`) key
    * quit and close the window by pressing the `q` or `esc` key

Notes
-----

There is nothing better than having the real cube in hands:

http://eu.rubiks.com/

Created on Thu Dec 11 21:35:39 2014

@author: Gilles Aouizerate 
"""

# the next two lines are here to avoid spurious message being printed
import logging
logging.getLogger('OpenGL').addHandler(logging.NullHandler())

import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

import quaternion as quat
import Kube as kb
import utilities as utl

# Set the width and height of the window
global width
global height

width = 600
height = 600

# Global variables for user information
global mesg1, mesg2, mesg3, mesg4, mesg5

mesg1 = ""
mesg2 = ""
mesg3 = "press 'a' to randomly move the cube"
mesg4 = "press 's' to solve it (it might take several seconds)"
mesg5 = "use arrow keys to change the camera point of view"

# Global variables for movements
global xrot, yrot
global X, Y, Z
global quater
global rotx, roty, rotz
global maxx, maxy, maxz
global A, B, C, D, E, F, Vpos, pos
global Ma, Mb, Mc, Md, Me, Mf
global Speed 
global cur_mov
global actions

cur_mov = 0

actions = []

quater = [quat.quaternion([0.,0.,0.], angl = 0) for i in range(26)]

rotx = 0.*np.ones(26)
roty = 0.*np.ones(26)
rotz = 0.*np.ones(26)
xrot = 45.0
yrot = 45.0
X = np.zeros((26,3))
Y = np.zeros((26,3))
Z = np.zeros((26,3))
X[:,0] = 1.
Y[:,1] = 1.
Z[:,2] = 1. 
maxx = np.copy(rotx)
maxy = np.copy(roty)
maxz = np.copy(rotz)

Speed = 6 

Vpos = np.transpose(np.matrix(np.array(range(26))))

pos = np.asarray(np.transpose(Vpos))[0]

A = range(9)
B = range(17,26)
C = [0, 1, 2, 9, 10, 11, 17, 18, 19]
D = [6, 7, 8, 14, 15, 16, 23, 24, 25]
E = [0, 3, 6, 9, 12, 14, 17, 20, 23]
F = [2, 5, 8, 11, 13, 16, 19, 22, 25]

Ma = Mb = Mc = Md = Me = Mf = np.matrix(np.identity(26))

# Light value and coordonates
global ambientlight
global diffuselight
global specular
global specref

ambientLight = (0.35, 0.35, 0.35, 1.0)
diffuseLight = ( 0.75, 0.75, 0.75, 0.7)
specular = (1.0, 1.0, 1.0, 1.0)
specref = (1.0, 1.0, 1.0, 1.0)

n = 26

B1 = utl.T(n, 0, 6)*utl.T(n, 0, 8)*utl.T(n, 0, 2)
B2 = utl.T(n, 1, 3)*utl.T(n, 1, 7)*utl.T(n, 1, 5)
Ma = B1*B2

B1 = utl.T(n, 0+17, 6+17)*utl.T(n, 0+17, 8+17)*utl.T(n, 0+17, 2+17)
B2 = utl.T(n, 1+17, 3+17)*utl.T(n, 1+17, 7+17)*utl.T(n, 1+17, 5+17)
Mb = B1*B2

B1 = utl.T(n, 0, 2)*utl.T(n, 0, 19)*utl.T(n, 0, 17)
B2 = utl.T(n, 1, 11)*utl.T(n, 1, 18)*utl.T(n, 1, 9)
Mc = B1*B2

B1 = utl.T(n, 6, 8)*utl.T(n, 6, 25)*utl.T(n, 6, 23)
B2 = utl.T(n, 7, 16)*utl.T(n, 7, 24)*utl.T(n, 7, 14)
Md = B1*B2

B1 = utl.T(n, 0, 17)*utl.T(n, 0, 23)*utl.T(n, 0, 6)
B2 = utl.T(n, 3, 9)*utl.T(n, 3, 20)*utl.T(n, 3, 14)
Me = B1*B2

B1 = utl.T(n, 2, 19)*utl.T(n, 2, 25)*utl.T(n, 2, 8)
B2 = utl.T(n, 5, 11)*utl.T(n, 5, 22)*utl.T(n, 5, 16)
Mf = B1*B2


# defintion of functions used by the program
def trace(x0 = 0, x1 = 0, x2 = 0):
    """Draw a cube which center is in position [x1, x2, x3]"""
    dc = 0.24    
    
    glBegin(GL_POLYGON)
    glColor3ub(0, 0, 0)
    glNormal3f(0, 0, 1)
    glVertex3f(-dc, -dc, dc)
    glVertex3f(dc, -dc, dc)
    glVertex3f(dc, dc, dc)
    glVertex3f(-dc, dc, dc)
    glEnd()    
    
    glBegin(GL_POLYGON)
    if x2 ==1.*0.5:
        glColor3ub(255, 00, 00)
    else:
        glColor3ub(0, 0, 0)
    glNormal3f(0, 0, 1)
    glVertex3f(-0.9*dc, -0.9*dc, 1.01*dc)
    glVertex3f(0.9*dc, -0.9*dc, 1.01*dc)
    glVertex3f(0.9*dc, 0.9*dc, 1.01*dc)
    glVertex3f(-0.9*dc, 0.9*dc, 1.01*dc)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3ub(0, 0, 0)
    glNormal3f(0, 1, 0)
    glVertex3f(-dc, dc, -dc)
    glVertex3f(-dc, dc, dc)
    glVertex3f(dc, dc, dc)
    glVertex3f(dc, dc, -dc)
    glEnd()

    glBegin(GL_POLYGON)
    if x1 ==1.*0.5:
        glColor3ub(0, 255, 00)
    else:
        glColor3ub(0, 0, 0)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.9*dc, 1.01*dc, -0.9*dc)
    glVertex3f(-0.9*dc, 1.01*dc, 0.9*dc)
    glVertex3f(0.9*dc, 1.01*dc, 0.9*dc)
    glVertex3f(0.9*dc, 1.01*dc, -0.9*dc)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3ub(0, 0, 0)
    glNormal3f(1, 0, 0)
    glVertex3f(dc, -dc, -dc)
    glVertex3f(dc, dc, -dc)
    glVertex3f(dc, dc, dc)
    glVertex3f(dc, -dc, dc)
    glEnd()

    glBegin(GL_POLYGON)
    if x0 ==1.*0.5:
        glColor3ub(255, 255, 255)
    else:
        glColor3ub(0, 0, 0)
    glNormal3f(1, 0, 0)
    glVertex3f(1.01*dc, -0.9*dc, -0.9*dc)
    glVertex3f(1.01*dc, 0.9*dc, -0.9*dc)
    glVertex3f(1.01*dc, 0.9*dc, 0.9*dc)
    glVertex3f(1.01*dc, -0.9*dc, 0.9*dc)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3ub(0, 0, 0)
    glNormal3f(0, 0, -1)
    glVertex3f(-dc, -dc, -dc)
    glVertex3f(dc, -dc, -dc)
    glVertex3f(dc, dc, -dc)
    glVertex3f(-dc, dc, -dc)
    glEnd()

    glBegin(GL_POLYGON)
    if x2 ==-1.*0.5:
        glColor3ub(255, 128, 00)
    else:
        glColor3ub(0, 0, 0)
    glNormal3f(0, 0, -1)
    glVertex3f(-0.9*dc, -0.9*dc, -1.01*dc)
    glVertex3f(0.9*dc, -0.9*dc, -1.01*dc)
    glVertex3f(0.9*dc, 0.9*dc, -1.01*dc)
    glVertex3f(-0.9*dc, 0.9*dc, -1.01*dc)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3ub(0, 0, 0)
    glNormal3f(0, -1, 0)
    glVertex3f(-dc, -dc, -dc)
    glVertex3f(-dc, -dc, dc)
    glVertex3f(dc, -dc, dc)
    glVertex3f(dc, -dc, -dc)
    glEnd()

    glBegin(GL_POLYGON)
    if x1 ==-1.*0.5:
        glColor3ub(00, 00, 255)
    else:
        glColor3ub(0, 0, 0)
    glNormal3f(0, -1, 0)
    glVertex3f(-0.9*dc, -1.01*dc, -0.9*dc)
    glVertex3f(-0.9*dc, -1.01*dc, 0.9*dc)
    glVertex3f(0.9*dc, -1.01*dc, 0.9*dc)
    glVertex3f(0.9*dc, -1.01*dc, -0.9*dc)
    glEnd()

    glBegin(GL_POLYGON)
    glColor3ub(0, 0, 0)
    glNormal3f(-1, 0, 0)
    glVertex3f(-dc, -dc, -dc)
    glVertex3f(-dc, dc, -dc)
    glVertex3f(-dc, dc, dc)
    glVertex3f(-dc, -dc, dc)
    glEnd()

    glBegin(GL_POLYGON)
    if x0 ==-1.*0.5:
        glColor3ub(255, 255, 00)
    else:
        glColor3ub(0, 0, 0)
    glNormal3f(-1, 0, 0)
    glVertex3f(-1.01*dc, -0.9*dc, -0.9*dc)
    glVertex3f(-1.01*dc, 0.9*dc, -0.9*dc)
    glVertex3f(-1.01*dc, 0.9*dc, 0.9*dc)
    glVertex3f(-1.01*dc, -0.9*dc, 0.9*dc)
    glEnd()


def update_cur_mov():
    """Updates the global variable cur_mov, reprsenting the current position in
    the action lists."""
    global rotx, roty, rotz
    global maxx, maxy, maxz
    global cur_mov
    if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
        cur_mov += 1


def find_dir(alpha, beta):
    """Determines the rotating direction and movement speed"""
    global Speed
    poss = [1, 2, 3, 5, 6, 9, 10, 15]
    if beta > alpha:
        res = 1.0
    if beta < alpha:
        res = -1.0
    return res*poss[min(max(0, int(Speed-1)),len(poss)-1)]


def renderscene():
    """This function litterally prints the scene."""
    global xrot, yrot
    global X, Y, Z
    global quater
    global rotx, roty, rotz
    global maxx, maxy, maxz
    global mesg1
    global mesg2
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()       
    indic = -1
    for i in range(-1,2,1):
        for j in range(-1,2,1):
            for k in range(-1,2,1):
                if (i==j==k==0)==False:
                    indic = indic + 1       
              
                    if rotx[indic]!=maxx[indic]:
                        speed = find_dir(rotx[indic],maxx[indic])
                        rotx[indic]=rotx[indic]+speed
                        update_cur_mov()
                        quater[indic]=quat.quaternion(X[indic], angl=speed)*quater[indic]
                        Y[indic]=np.transpose(utl.Rq(speed*np.pi/180.,X[indic])*np.transpose(np.matrix(Y[indic])))
                        Z[indic]=np.transpose(utl.Rq(speed*np.pi/180.,X[indic])*np.transpose(np.matrix(Z[indic])))
                  
                    if roty[indic]!=maxy[indic]:
                        speed = find_dir(roty[indic],maxy[indic])
                        roty[indic]=roty[indic]+speed
                        update_cur_mov()
                        quater[indic]=quat.quaternion(Y[indic], angl=speed)*quater[indic]
                        X[indic]=np.transpose(utl.Rq(speed*np.pi/180.,Y[indic])*np.transpose(np.matrix(X[indic])))
                        Z[indic]=np.transpose(utl.Rq(speed*np.pi/180.,Y[indic])*np.transpose(np.matrix(Z[indic])))

                    if rotz[indic]!=maxz[indic]:
                        speed = find_dir(rotz[indic],maxz[indic])
                        rotz[indic]=rotz[indic]+speed
                        update_cur_mov()
                        quater[indic]=quat.quaternion(Z[indic], angl=speed)*quater[indic]
                        Y[indic]=np.transpose(utl.Rq(speed*np.pi/180.,Z[indic])*np.transpose(np.matrix(Y[indic])))
                        X[indic]=np.transpose(utl.Rq(speed*np.pi/180.,Z[indic])*np.transpose(np.matrix(X[indic])))
    
                    glLoadIdentity()
                    
                    rotation_x = quat.quaternion([1.,0.,0.], angl=-xrot)
                    rotation_y = quat.quaternion([0.,1.,0.], angl=-yrot)
                    glMultMatrixf(rotation_x.matrix)
                    glMultMatrixf(rotation_y.matrix)
                    glMultMatrixf((quater[indic]).matrix)
                    glTranslatef(i*0.5,j*0.5,k*0.5)
                    trace(i*0.5, j*0.5, k*0.5)     
    glLoadIdentity()       
    glColor3ub(0, 0, 100)
    glRasterPos2f(-1.15, -1.5)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, mesg1+" "+mesg2) 
    glRasterPos2f(-1., 1.75)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, mesg3) 
    glRasterPos2f(-1.35, 1.5)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, mesg4)
    glRasterPos2f(-1.35, -1.75)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, mesg5) 
    glPopMatrix()
    glutSwapBuffers()
    glutPostRedisplay()


def init():
    """Initiates the display paramters"""
    global width
    global height
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)
    glColor3ub(230,100,100)


def specialkeys(key, x, y):
    """Tells the program what to do when the arrow keys are pressed"""
    global xrot, yrot

    if key == GLUT_KEY_UP:
        xrot = xrot - 2
    if key == GLUT_KEY_DOWN:
        xrot = xrot + 2
    if key == GLUT_KEY_LEFT:
        yrot -= 2.0
    if key == GLUT_KEY_RIGHT:
        yrot += 2.0            
    glutPostRedisplay()


def sequence():
    """This function is meant to be continiously called by OpenGL. It monitors 
    the moves. If the global variable cur_mov equals the length of the actions 
    list, also a global variable, this means that all the planned moves have 
    been executed, thus sequence just passes. If cur_mov does not equal the 
    length of the actions list, then the function manages the next move."""
    global cur_mov
    global actions
    global mesg1
    global mesg2
    if cur_mov>=len(actions):
        mesg1 = ""
        mesg2 = ""
        pass
    else:
        make_a_move(actions[cur_mov])
        mesg2 = "{0} moves remaining".format(len(actions)-cur_mov)
    glutPostRedisplay()        
    

def make_a_move(key):
    """Updates the global parameters. This will start the moving process."""
    global xrot, yrot
    global rotx, roty, rotz
    global maxx, maxy, maxz
    global Ma, Mb, Mc, Md, Me, Mf
    global A, B, C, D, E, F, Vpos, pos    
    
    if key == "F":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = (Ma)**(-1)*Vpos
            maxx[pos[A]] = (maxx[pos[A]] - 90)
    if key == "f":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = Ma*Vpos
            maxx[pos[A]] = (maxx[pos[A]] + 90)
    if key == "D":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0] 
            pos = np.array([int(l) for l in pos])
            Vpos = (Mc)**(-1)*Vpos
            maxy[pos[C]] = (maxy[pos[C]] - 90)
    if key == "d":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0] 
            pos = np.array([int(l) for l in pos])
            Vpos = Mc*Vpos
            maxy[pos[C]] = (maxy[pos[C]] + 90)
    if key == "l":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = Me*Vpos
            maxz[pos[E]] = (maxz[pos[E]] + 90)
    if key == "L":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = (Me)**(-1)*Vpos
            maxz[pos[E]] = (maxz[pos[E]] - 90)
    if key == "B":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = Mb*Vpos
            maxx[pos[B]] = (maxx[pos[B]] + 90)
    if key == "b":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = (Mb)**(-1)*Vpos
            maxx[pos[B]] = (maxx[pos[B]] - 90)
    if key == "U":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = Md*Vpos
            maxy[pos[D]] = (maxy[pos[D]] + 90)
    if key == "u":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = (Md)**(-1)*Vpos
            maxy[pos[D]] = (maxy[pos[D]] - 90)
    if key == "R":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = Mf*Vpos
            maxz[pos[F]] = (maxz[pos[F]] + 90)
    if key == "r":
        if (rotx==maxx).all()&(roty==maxy).all()&(rotz==maxz).all():
            pos = np.asarray(np.transpose(Vpos))[0]
            pos = np.array([int(l) for l in pos])
            Vpos = (Mf)**(-1)*Vpos
            maxz[pos[F]] = (maxz[pos[F]] - 90) 

            

def keyboard(key, x, y):
    """When the user press keyboard keys (except arrrow keys), this function 
    updates accordingly the actions global list"""
    global actions
    global mesg1
    
    if key == chr(27) or key == "q":
        sys.exit()
    if key in ["F", "f", "B", "b", "R", "r", "U", "u", "L", "l", "D", "d" ]:
        actions = actions + [key]
    if key == "a":
        actions = actions + kb.rand_move(20)
        mesg1 = "randomly moving...."
    if key == "s":
        state = kb.move_list_to_state(actions)
        seq = kb.solve(state)
        actions = actions + seq
        mesg1 = "I found the solution!..."


def reshape( w, h):
    """Reshapes the scene when the window is resized."""
    lightPos = (-50.0, 50.0, 100.0, 1.0)
    nRange = 2.0

    if h==0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    
    glLoadIdentity()
    
    if w <= h:
        glOrtho(-nRange, nRange, -nRange*h/w, nRange*h/w, -nRange, nRange)
    else:
        glOrtho(-nRange*w/h, nRange*w/h, -nRange, nRange, -nRange, nRange)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)


if __name__ == '__main__':   
    glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE|GLUT_DEPTH)
    glutInitWindowPosition(100,100)
    glutInitWindowSize(width,height)
    glutInit(sys.argv)
    glutCreateWindow("Cube")

    init()
    
    glutReshapeFunc(reshape)
    glutDisplayFunc(renderscene)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(specialkeys)
    glutIdleFunc(sequence)
    glutMainLoop()