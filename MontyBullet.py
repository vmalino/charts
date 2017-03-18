# PyOpenGL demo of Monty Hall game enhanced with strategies vizualization
# For "stay" and "switch" strategies bullty graphs depicting expected and sample
# wins probabitlity is shown (above doors). This helps player to choose doors more
# reasonably.
# Commands: 1, 2, and 3 to choose door, a/A to choose "stay" strategy,
# s/S to choose "switch" strategy, r/R for next game
# By Vladimir Malinovskiy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # glut32.dll to download separately and to copy to C:\Windows\System
from numpy import *
from random import randint


global game  # Game number
global prize  # Door with prize
global choosen1  # Door selected by player
global opened  # Door opened by Monty
global choosen2  # Door selected by player after one door is opened
global strats  # Strategies successes
global strats_counts  # Strategies counts


# Door drawing, closed or opened, with prize or not
def door(d, is_open):
    glColor3f(0, 0, 0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)  # Door casing
    glVertex2f(14 * d - 9, 5)
    glVertex2f(14 * d - 9, 15)
    glVertex2f(14 * d - 3, 15)
    glVertex2f(14 * d - 3, 5)
    glEnd()
    if is_open:
        glBegin(GL_LINE_LOOP)  # Opened door fold
        glVertex2f(14 * d - 3, 15)
        glVertex2f(14 * d - 1, 13)
        glVertex2f(14 * d - 1, 3)
        glVertex2f(14 * d - 3, 5)
        glEnd()
        if d == prize:
            glColor3f(0, 0.6, 0)
            glBegin(GL_QUADS)  # Prize box if it is behind this door
            glVertex2f(14 * d - 8, 6)
            glVertex2f(14 * d - 8, 9)
            glVertex2f(14 * d - 4, 9)
            glVertex2f(14 * d - 4, 6)
            glEnd()            
    else:
        glBegin(GL_LINES)  # Closed door knob
        glVertex2f(14 * d - 8, 10)
        glVertex2f(14 * d - 8, 11)
        glEnd()
        if d == choosen1:
            glColor3f(0, 0, 0.8)
            glLineWidth(1)
            glBegin(GL_LINE_LOOP)  # Choosen door highlighting
            glVertex2f(14 * d - 9.5, 4.5)
            glVertex2f(14 * d - 9.5, 15.5)
            glVertex2f(14 * d - 2.5, 15.5)
            glVertex2f(14 * d - 2.5, 4.5)
            glEnd()        


def bullet_graph(d, s):
    global game, strats
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_QUADS)  # Theoretical (expected) percentage of successes
    glVertex2f(14 * d - 6.5, 9.5)
    glVertex2f(14 * d - 6.5, 9.5 + 5 * (1 + s) / 3)
    glVertex2f(14 * d - 3.5, 9.5 + 5 * (1 + s) / 3)
    glVertex2f(14 * d - 3.5, 9.5)
    glEnd()
    if strats_counts[s] > 0:
        glColor3f(0, 0, 0)
        glBegin(GL_QUADS)  # Sample percentage of successes for a strategy
        glVertex2f(14 * d - 5.5, 9.5)
        glVertex2f(14 * d - 5.5, 9.5 + 5 * strats[s] / strats_counts[s])
        glVertex2f(14 * d - 4.5, 9.5 + 5 * strats[s] / strats_counts[s])
        glVertex2f(14 * d - 4.5, 9.5)
        glEnd()
    glLineWidth(1)
    glColor3f(0, 0, 0)
    glBegin(GL_LINE_LOOP)  # Graph frame (full range = 1)
    glVertex2f(14 * d - 6.5, 9.5)
    glVertex2f(14 * d - 6.5, 14.5)
    glVertex2f(14 * d - 3.5, 14.5)
    glVertex2f(14 * d - 3.5, 9.5)
    glEnd()


# GLUT initialization
def init():
    global game, prize, choosen1, opened, choosen2, strats, strats_counts

    glClearColor(255, 255, 255, 1)  # White background
    gluOrtho2D(0, 45, 0, 20)  # x-left, x-right, y-bottom, y-top

    # Initial state at the first game
    game = 1
    prize = randint(1, 3)  # Randomly put prize behind one of the doors
    choosen1 = 0
    opened = 0
    choosen2 = 0
    strats = [0, 0]
    strats_counts = [0, 0]

# Drawing function called in glutDisplayFunc()
def plot():
    global choosen1, opened, choosen2
    glClear(GL_COLOR_BUFFER_BIT)
    if choosen1 == 0:  # All doors closed in the beginning
        for i in range(3):
            door(i + 1, False)
    else:
        if choosen2 == 0:
            for i in range(3):
                d = i + 1
                if d == choosen1:
                    door(d, False)
                    bullet_graph(d, 0)  # Show bullet graph for "stay" strategy
                elif d == opened:
                    door(d, True)  # Door selected by Monty to be opened
                else:
                    door(d, False)
                    bullet_graph(d, 1)  # Show bullet grapth for "switch" strategy
        else:
            for i in range(3):
                d = i + 1
                if d == opened:
                    door(d, True)  # Door selected by Monty to be opened
                else:
                    door(d, d == choosen2)  # Door finally selected by player
                    if d == choosen1:
                        bullet_graph(d, 0)  # Show bullet graph for "stay" strategy
                    else:
                        bullet_graph(d, 1)  # Show bullet grapth for "switch" strategy
    glFlush()


# Keyboard commands function called in glutKeyboardFunc()
def keyboard(key, x, y):
    global game, prize, choosen1, opened, choosen2, strats
    if key == b'\x1B' or key == b'q' or key == b'Q':
        sys.exit()  # Exit upon q, Q, or ESC
    elif key == b'1' or key == b'2' or key == b'3':
        if choosen1 == 0 and opened == 0:  # If nothing choosen, set selected door
            choosen1 = int(key)
            while opened == 0:  # Monty is selecting door without prize to open
                d = randint(1, 3)
                if d != prize and d != choosen1:
                    opened = d
            glutPostRedisplay()
    elif key == b'a' or key == b'A':  # Player selects "stay" strategy
        if choosen1 > 0 and opened > 0 and choosen2 == 0:
            choosen2 = choosen1
            glutPostRedisplay()
            strats_counts[0] = strats_counts[0] + 1  # Strategies usage statistics
            if choosen2 == prize:
                strats[0] = strats[0] + 1
    elif key == b's' or key == b'S':  # Player selects "switch" strategy
        if choosen1 > 0 and opened > 0 and choosen2 == 0:
            while choosen2 == 0:
                d = randint(1, 3)
                if d != opened and d != choosen1:
                    choosen2 = d
            glutPostRedisplay()
            strats_counts[1] = strats_counts[1] + 1  # Strategies usage statistics
            if choosen2 == prize:
                strats[1] = strats[1] + 1
    elif key == b'r' or key == b'R':  # Next game
        if choosen1 > 0 and opened > 0 and choosen2 > 0:
            game = game + 1
            prize = randint(1, 3)  # Randomly put prize behind one of the doors
            choosen1 = 0
            opened = 0
            choosen2 = 0
            glutPostRedisplay()


glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(900, 400)
glutInitWindowPosition(100, 100)
glutCreateWindow('Monty Hall simulation with bullet graph')
glutDisplayFunc(plot)
glutKeyboardFunc(keyboard)
init()
glutMainLoop()
