# Transformation of line chart to candlestick chart

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
from random import randint

global row, step
step = 0

# Single variable - modified random walk (4 weighted scenarios)
def simulation(v0, l):
    val = v0
    lst = [val]
    for i in range(l - 1):
        s = randint(1, 100)
        if s > 90:
            val = val + 20  # Up a lot
        elif s > 50:
            val = val + 5  # Up a little
        elif s > 10:
            val = val - 5  # Down a little
        else:
            val = val - 20  # Down a lot
        if val > 100:
            lst.append(90)
        elif val > 0:
            lst.append(val)
        else:
            lst.append(10)
    return lst


# Line chart - single variable by timeline
def line_chart(var, x0, y0, scale = 1):
    global step
    glLineWidth(3)
    glBegin(GL_LINE_STRIP)  # Linked dots sequence
    x = x0
    for n in var:
        glVertex2f(x, n / 10 * scale + y0)
        x = x + scale - 0.1 * step
    glEnd()


# Candlestick chart - limits of the single variable
def candlestick_chart(var, x0, y0, scale = 1):
    glLineWidth(3)
    glBegin(GL_LINES)  # Min-Max line
    glVertex2f(x0 + 5, max(var) / 10 + y0)
    glVertex2f(x0 + 5, min(var) / 10 + y0)
    glEnd()
    if var[len(var) - 1] > var[0]:
        glColor3f(1.0, 1.0, 1.0)  # Last > First color
    elif var[len(var) - 1] < var[0]:
        glColor3f(0.0, 0.0, 0.0)  # Last < First color
    glBegin(GL_QUADS)
    glVertex2f(x0 + 4.5, var[len(var) - 1] / 10 + y0)
    glVertex2f(x0 + 4.5, var[0] / 10 + y0)
    glVertex2f(x0 + 5.5, var[0] / 10 + y0)
    glVertex2f(x0 + 5.5, var[len(var) - 1] / 10 + y0)
    glEnd()
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x0 + 4.5, var[len(var) - 1] / 10 + y0)
    glVertex2f(x0 + 4.5, var[0] / 10 + y0)
    glVertex2f(x0 + 5.5, var[0] / 10 + y0)
    glVertex2f(x0 + 5.5, var[len(var) - 1] / 10 + y0)
    glEnd()


def init():
    glClearColor(255, 255, 255, 1.0)
    gluOrtho2D(0, 33, 0, 22)  # x-left, x-right, y-bottom, y-top


def plot_diagrams():
    glClear(GL_COLOR_BUFFER_BIT)
    x_start = 5
    y_start = 5
    # Illustration
    glColor3f(0.0, 0.5, 0.5)
    glBegin(GL_LINES)
    glVertex2f(x_start, y_start + max(row) / 10)
    glVertex2f(x_start + 20, y_start + max(row) / 10)
    glEnd()
    # Charts
    glColor3f(0.0, 0.0, 0.0)
    line_chart(row, x_start, y_start, 1)
    candlestick_chart(row, x_start + 15, y_start)
    glFlush()


def keyboard(key, x, y):
    global row, step
    if key == b'\x1B' or key == b'q' or key == b'Q':
        sys.exit()
    elif key == b'r' or key == b'R':
        row = simulation(50, 10)
        step = 0
        glutPostRedisplay()
    elif key == b'\x20' or key == b'n' or key == b'N':
        step = step + 1
        glutPostRedisplay()


row = simulation(50, 10)
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(900, 600)
glutInitWindowPosition(450, 100)
glutCreateWindow('Line to Candlestick')
glutDisplayFunc(plot_diagrams)
glutKeyboardFunc(keyboard)
init()
glutMainLoop()
