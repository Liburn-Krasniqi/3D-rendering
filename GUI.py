"""
(x,y,z) -> 3d point behind screen

# points onScreened on screen
x' = x/z
y' = y/z


"""
import time
import pygame
import math
import numpy as np

FPS = 60
dz = 2  # delta z
angle = 0

width = 800
height = 800

screen = pygame.display.set_mode((height, width))

"""
color presets
"""
foreground = (67, 255, 31)

red = (246, 46, 38)

background = (0, 0, 0)


run = True

def clear():
    screen.fill((background))

def point(p):
    s = 10
    pygame.draw.rect(screen, foreground, pygame.Rect(p['x'] - s/2, p['y'] - s/2, s, s))

def pointRed(p):
    s = 10
    pygame.draw.rect(screen, red, pygame.Rect(p['x'] - s/2, p['y'] - s/2, s, s))
    
def onScreen(p):
    # -1..1 => 0..2 => 0..1 => 0..w/h 

    # type('Obj', (object,), { 'x' : (p.x + 1)/2 * width, 'y' : (p.y + 1)/2 * height})()
     return{ 
            'x' : ((p['x'] + 1)/2) * width,
             'y' : (1- (p['y'] + 1)/2) * height
             }

def project(p):
    return { 
            'x' : p['x']/p['z'],
             'y' : p['y']/p['z']
            }

def translate_z(p, dz):
    return {
         'x' : p['x'],
         'y' : p['y'],
         'z' : p['z']+ dz  # the translation is ' ere
         }

def rotate_xz(p, angle):  # rotating around xz plane | y axis
    C = np.cos(angle)
    S = np.sin(angle)

    return { 
        'x' : ((p['x']*C) - (p['z']*S)),
        'y' : p['y'], 
        'z' : ((p['x']*S) +  (p['z']*C))
    }

    # (x_{rotated} = (x-dx)\cos \theta -(y-dy)\sin \theta +dx\)
    # (y_{rotated} = (x-dx)\sin \theta +(y-dy)\cos \theta +dy\) 

def line(p1, p2):
    pygame.draw.line(screen, # on where
                     foreground, # color
                     (p1['x'],p1['y']), # start
                     (p2['x'],p2['y']), # finnish
                     3) # stroke width


VS = [
    {'x':  0.5, 'y':  0.5, 'z': 0.5}, 
    {'x': -0.5, 'y':  0.5, 'z': 0.5},
    {'x': -0.5, 'y': -0.5, 'z': 0.5},
    {'x':  0.5, 'y': -0.5, 'z': 0.5},
    
    {'x':  0.5, 'y':  0.5, 'z': -0.5},
    {'x': -0.5, 'y':  0.5, 'z': -0.5},
    {'x': -0.5, 'y': -0.5, 'z': -0.5},
    {'x':  0.5, 'y': -0.5, 'z': -0.5},
]

FS = [
    [0,1,2,3],
    [4,5,6,7],
    [0,4],
    [1,5],
    [2,6],
    [3,7],
]

VSB = []

def frame():
    # clear()
    DT = 1/FPS  # delta time between frames 

    global dz 
    dz += 1*DT  # move by 0,0166666667 each frame 

    global angle
    angle += math.pi * DT

    # for v in VS:
    #     point(onScreen(project(translate_z(rotate_xz(v, angle), dz))))
    
    for f in FS:
        for i in range(0, len(f)):
            A = VS[f[(i+1)%len(f)]]
            B = VS[f[(i+2)%len(f)]]
            line(
                onScreen(project(translate_z(rotate_xz(A, angle), dz))),
                onScreen(project(translate_z(rotate_xz(B, angle), dz)))
            )

    # for v in VSB:
    #     pointRed(onScreen(project(translate_z(rotate_xz(v, angle), dz))))
    
    # time.sleep(1000/FPS)
    # frame()
    # timer = threading.Timer(1000/FPS, frame)
    # timer.start() 

while run:
    clear()

    # point(onScreen({'x': 0,'y': 1}))
    # point(onScreen(project({'x': 0.5,'y': 0,'z': 2})))
    # point({'x': 100,'y': 100})
    frame()
    # 

    # so i dont do screen.blit for everything i guess in this case?
    pygame.display.flip()
    time.sleep((1000/FPS)/1000) # /1000 to get miliseconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False