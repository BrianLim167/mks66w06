from display import *
from matrix import *
import math

screen = PPMGrid()

red     = [255,0,0]
green   = [0,255,0]
yellow  = [255,255,0]
magenta = [255,0,255]
cyan    = [0,255,255]
##draw_line(250,250, 250+150,250+50, screen, green)

##length = 40
##for i in range(360):
##    h = i / 60
##    c = int(i % 60 * 255 / 60)
##    if (0 <= h < 1):
##        color = [255,c,0]
##    if (1 <= h < 2):
##        color = [255-c,255,0]
##    if (2 <= h < 3):
##        color = [0,255,c]
##    if (3 <= h < 4):
##        color = [0,255-c,255]
##    if (4 <= h < 5):
##        color = [c,0,255]
##    if (5 <= h < 6):
##        color = [255,0,255-c]
##    dx = int(length*math.cos(math.radians(i)))
##    dy = int(length*math.sin(math.radians(i)))
##    screen.draw_line(250,250, 250+dx,250+dy, color)

##m = Matrix(4,0)
##m.add_edge(10,10,0, 30,40,0)
##m.add_edge(30,40,0, 0, 20,0)
##m.add_edge(0, 20,0, 10,10,0)
##print(m)
##print("###########\n")
##screen.draw_lines(m, green)
##
##Matrix.ident().print()
##print("###########\n")
##m *= Matrix.ident()
##print(m)
##print("###########\n")

##for i in range(10):
##    for j in range(20):
##        t = Matrix.ident(3)
##        t.add_point(40*i+30,25*j+30)
##        n = t * m
##        print(n)
##        print("###########\n")
##        screen.draw_lines(n, red)
##for i in range(10):
##    for j in range(20):
##        t = Matrix.ident(3)
##        t.add_point(45*i+60,15*j-30)
##        n = t * m
##        print(n)
##        print("###########\n")
##        screen.draw_lines(n, yellow)
##    for c in range(t.cols):
##        t[c][c] = 5
##    t[3][3] = 1
##    n = t * m
##    print(n)
##    print("###########\n")
##    screen.draw_lines(n, cyan)
##m = Matrix.mover(5,6,7)
##print(m)
##print("###########\n")
##m = Matrix.rotx(30)
##print(m)
##print("###########\n")

##screen.display()
##screen.save_extension('img.png')

##print(Matrix.hermite())

screen.parse_file( "script", green )
