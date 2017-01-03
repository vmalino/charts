# Six charts to visualize single variable

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import *
from random import randint


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
def line_chart(var, x0, y0):
    glLineWidth(3)
    glBegin(GL_LINE_STRIP)  # Linked dots sequence
    x = x0
    for n in var:
        glVertex2f(x, n / 10 + y0)
        x = x + 1
    glEnd()


# Bar chart - single variable by rangs
def bar_chart(var, x0, y0):
    y = y0 + 10
    for n in sorted(var, reverse = True):
        glBegin(GL_QUADS)  # To display value bars
        glVertex2f(x0, y)
        glVertex2f(x0 + n / 10, y)
        glVertex2f(x0 + n / 10, y - 0.9)
        glVertex2f(x0, y - 0.9)
        glEnd()
        y = y - 1


# Histogram - single variable by intervals (bins)
def histogram(var, x0, y0):
    bins = [0, 0, 0, 0, 0]  # Bins
    for n in var:
        i = (n - 1) // 20  # Put value into bin
        bins[i] = bins[i] + 1
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


# Candlestick chart - limits of the single variable
def candlestick_chart(var, x0, y0):
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


# Pie chart - parts of the whole (sum)
def pie_chart(var, x0, y0):
    glLineWidth(2)
    c = 0  # Accumulated value
    for n in sorted(var, reverse = True):
        t0 = c
        c =  c + n / sum(var)  # Add value's share
        glBegin(GL_LINE_LOOP)  # Value sector
        glVertex2f(x0 + 5, y0 + 5)
        for t in arange(2 * pi * t0, 2 * pi * c, 0.01):
            x = sin(t)
            y = cos(t)
            glVertex2f(x0 + 5 + x * 3, y0 + 5 + y * 3)
        glEnd()
    

# Box plot
def box_plot(var, x0, y0):
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)  # Box for quartiles
    glVertex2f(x0 + percentile(var, 25) / 10, y0 + 4)
    glVertex2f(x0 + percentile(var, 25) / 10, y0 + 6)
    glVertex2f(x0 + percentile(var, 75) / 10, y0 + 6)
    glVertex2f(x0 + percentile(var, 75) / 10, y0 + 4)
    glEnd()
    glBegin(GL_LINES)  # min line
    glVertex2f(x0 + min(var) / 10, y0 + 5)
    glVertex2f(x0 + percentile(var, 25) / 10, y0 + 5)
    glEnd()
    glBegin(GL_LINES)  # median line
    glVertex2f(x0 + percentile(var, 50) / 10, y0 + 4)
    glVertex2f(x0 + percentile(var, 50) / 10, y0 + 6)
    glEnd()
    glBegin(GL_LINES)  # max line
    glVertex2f(x0 + percentile(var, 75) / 10, y0 + 5)
    glVertex2f(x0 + max(var) / 10, y0 + 5)
    glEnd()


def init():
    glClearColor(255, 255, 255, 1.0)
    gluOrtho2D(0, 33, 0, 22)  # x-left, x-right, y-bottom, y-top


def plot_diagrams():
    glClear(GL_COLOR_BUFFER_BIT)

    # Separators
    glColor3f(0.0, 0.0, 1.0)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    glVertex2f(0, 11)
    glVertex2f(33, 11)
    glVertex2f(11, 0)
    glVertex2f(11, 22)
    glVertex2f(22, 0)
    glVertex2f(22, 22)
    glEnd()

    # Charts
    row = simulation(50, 10)
    glColor3f(0.0, 0.0, 0.0)
    line_chart(row, 0.5, 11.5)
    bar_chart(row, 11.5, 11.5)
    histogram(row, 22.5, 11.5)
    candlestick_chart(row, 0.5, 0.5)
    pie_chart(row, 11.5, 0.5)
    box_plot(row, 22.5, 0.5)

    glFlush()


def keyboard(key, x, y):
    if key == b'\x1B' or key == b'q' or key == b'Q':
        sys.exit()
    elif key == b'r' or key == b'R':
        glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(900, 600)
glutInitWindowPosition(450, 100)
glutCreateWindow('6 Charts for 1 Variable')
glutDisplayFunc(plot_diagrams)
glutKeyboardFunc(keyboard)
init()
glutMainLoop()
