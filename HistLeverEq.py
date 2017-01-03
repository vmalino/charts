# PyOpenGL demo of a histogram and its mean (normal and sample)
# The green frame shows normal (expected) histogram range and average position
# The red fulcrum calculated as mean shows physical (mechanical) sense of histogram (balanced lever)

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # glut32.dll to download separately and to copy to C:\Windows\System
from numpy import *
from random import randint


global row  # Single variable values from simulation


# Single variable simulation - random walk modified with 4 scenarios
def simulation(v0, l):
    val = v0
    lst = [val]
    for i in range(l - 1):
        s = randint(1, 100)  # Random integer values from 1 to 100 to model probability
        if s > 90:
            val = val + 20  # "Up a lot" unlikely scenario
        elif s > 50:
            val = val + 5  # "Up a little" likely scenario
        elif s > 10:
            val = val - 5  # "Down a little" likely scenario
        else:
            val = val - 20  # Down a lot unlikely scenario
        if val > 100:
            lst.append(90)  # Upper limit of simulation range
        elif val > 0:
            lst.append(val)
        else:
            lst.append(10)  # Lower limit of simulation range
    return lst


# Histogram - single variable by intervals (bins)
def histogram(var, x0, y0):
    glColor3f(0, 0, 1)  # To show historgram bins in blue
    bins = [0, 0, 0, 0, 0]  # Histogram bins
    for n in var:
        i = (n - 1) // 20  # Define bin for a value
        bins[i] = bins[i] + 1  # Put a value into a bin
    x = x0
    for b in bins:
        if b == 0:
            b = 0.1
        glBegin(GL_QUADS)  # To display bin bars
        glVertex2f(x, y0)
        glVertex2f(x, y0 + b)
        glVertex2f(x + 1.9, y0 + b)
        glVertex2f(x + 1.9, y0)
        glEnd()
        x = x + 2


# Normal (expected) distribution range and center
def frame(var, x0, y0):
    glColor3f(0, 1, 0)  # To show normal frame in green
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)  # To draw frame square (bins x probability)
    glVertex2f(x0, y0)
    glVertex2f(x0 + 10, y0)
    glVertex2f(x0 + 10, y0 + 10)
    glVertex2f(x0, y0 + 10)
    glEnd()
    glBegin(GL_LINES)  # To draw center line
    glVertex2f(x0 + 5, y0 + 11)
    glVertex2f(x0 + 5, y0 - 1)
    glEnd()


# Histogram lever pivot point
def fulcrum(var, x0, y0):
    glColor3f(1, 0, 0)  # 
    m = x0 + sum(var) / len(var) / 10
    glBegin(GL_QUADS)  # To draw fulcrum's triangle
    glVertex2f(m, y0)
    glVertex2f(m + 0.5, y0 - 0.5)
    glVertex2f(m - 0.5, y0 - 0.5)
    glVertex2f(m, y0)
    glEnd()


# GLUT initialization
def init():
    glClearColor(255, 255, 255, 1)
    gluOrtho2D(0, 20, 0, 15)  # x-left, x-right, y-bottom, y-top


# Drawing function called in glutDisplayFunc()
def plot():
    glClear(GL_COLOR_BUFFER_BIT)
    x_start = 5
    y_start = 2.5
    histogram(row, x_start, y_start)
    frame(row, x_start, y_start)
    fulcrum(row, x_start, y_start)
    glFlush()


# Keyboard commands function called in glutKeyboardFunc()
def keyboard(key, x, y):
    global row
    if key == b'\x1B' or key == b'q' or key == b'Q':
        sys.exit()  # Exit by q, Q, or ESC
    elif key == b'r' or key == b'R':
        row = simulation(50, 10)  # Re-draw histogram with new simulation by r or R
        glutPostRedisplay()


row = simulation(50, 10)  # Initial simulation
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(900, 600)
glutInitWindowPosition(450, 100)
glutCreateWindow('Histogram with Normal frame and Lever fulcrum (\'r\' to refresh)')
glutDisplayFunc(plot)
glutKeyboardFunc(keyboard)
init()
glutMainLoop()
