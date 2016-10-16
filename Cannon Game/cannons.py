
import pygame
import time
from random import randint

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

_cannon_list = []

def add_cannon( position, ball_color, fire_rate=1, move_rate=200, ball_vel=300):
    new_cannon = []
    new_ball = []
    surface = pygame.display.get_surface()
    curFireDelay = fire_rate
    surface_width = surface.get_width()
    surface_height = surface.get_height()
    cannon_img_left = pygame.image.load('cannon.png').convert_alpha()
    new_cannon.append(position)
    # TOP
    if position == TOP:
        cannon_img_top = pygame.transform.rotate(cannon_img_left, -90)
        x=new_cannon.append(randint(0,surface_width-cannon_img_top.get_width()))
        y= new_cannon.append(70)
    # BOTTOM
    elif position == BOTTOM:
        cannon_img_bottom = pygame.transform.rotate(cannon_img_left, 90)                  
        # cx
        new_cannon.append(randint(0,surface_width-cannon_img_bottom.get_width()))
        # cy
        new_cannon.append(surface_height-cannon_img_bottom.get_height())                  
    # LEFT
    elif position == LEFT:
        cannon_img_left                  
        # cx             
        new_cannon.append(0)
        # cy                
        new_cannon.append(randint(0,surface_height - cannon_img_left.get_height()))
    # RIGHT
    elif position == RIGHT:
        cannon_img_right = pygame.transform.flip(cannon_img_left, True, False)                 
        # cx              
        new_cannon.append(surface_width-cannon_img_right.get_width())
        # cy               
        new_cannon.append(randint(0,surface_height-cannon_img_right.get_height()))                  


    new_cannon.append(ball_color)
    new_cannon.append(fire_rate)
    new_cannon.append(fire_rate)

    if randint(0, 1):
        new_cannon.append(-1)
        
    else:
        new_cannon.append(1)
        

    new_cannon.append(move_rate)
    new_cannon.append([])
    new_cannon.append(ball_vel)

    new_cannon.append(cannon_img(new_cannon))
    new_cannon.append([])
    
    
    _cannon_list.append(new_cannon)

def cannon_img(c):
    
    cannon_img_orignal = pygame.image.load('cannon.png').convert_alpha()
    cannon_img_top = pygame.transform.rotate(cannon_img_orignal, -90)
    cannon_img_bottom = pygame.transform.rotate(cannon_img_orignal, 90)
    cannon_img_right = pygame.transform.flip(cannon_img_orignal, True, False)
    cannon_img_left = pygame.image.load('cannon.png').convert_alpha()

    if c[0] == TOP:
        orientation = cannon_img_top
    elif c[0] == BOTTOM:               
        orientation = cannon_img_bottom
    elif c[0] == LEFT:
        orientation = cannon_img_left
    else:
        orientation = cannon_img_right
    return orientation
        
                
def draw_cannons(surface):
    for c in _cannon_list:
        surface.blit(c[10], (c[1], c[2]))

        for ball in c[8]:
            bx = int(ball[1])
            by = int(ball[2])
            pygame.draw.circle(surface, c[3], (bx, by), 8)


def update_cannons(dtime):
    surface_width = pygame.display.get_surface().get_width()
    surface_height = pygame.display.get_surface().get_height()
    # Cannon Movement
    for c in _cannon_list:
        # TOP AND BOTTOM
        if c[0] == TOP or c[0] == BOTTOM :
            c[1] += c[6]*c[7] * dtime
            if c[1] <= 0:
                c[1] = 0
                c[6]*=-1
            elif c[1] >= surface_width - c[10].get_width():
                c[1] = surface_width - c[10].get_width()
                c[6] *= -1
        # LEFT AND RIGHT
        if c[0] == LEFT or c[0] == RIGHT :
            c[2] += c[6]*c[7] * dtime
            if c[2] <= 70:
                c[2] = 70
                c[6] *= -1
            elif c[2] >= surface_height - c[10].get_height():
                c[2] = surface_height - c[10].get_height()
                c[6] *= -1
               
               
    #Ball Movement
        for cball in c[8]:
            if cball[0] == TOP:
                cball[2] += c[9] * dtime
                if cball[2] >= surface_height + c[10].get_height()// 4:
                    c[8].remove(cball)
            elif cball[0] == BOTTOM:
                cball[2] -= c[9] * dtime
                if cball[2] <= -c[10].get_height() // 4:
                    c[8].remove(cball)
            elif cball[0] == LEFT:
                cball[1] += c[9] * dtime
                if cball[1] >= surface_width + c[10].get_width() // 4:
                    c[8].remove(cball)
            elif cball[0] == RIGHT:
                cball[1] -= c[9] * dtime
                if cball[1] <= - c[10].get_width() // 4:
                    c[8].remove(cball)

        c[4] -= dtime
        while c[4] <= 0:
            c[4] += c[5]
            if c[0] == TOP :
                ball = [TOP, c[1] + c[10].get_width() // 2, c[2] + c[10].get_height() + c[10].get_height() // 4]
            elif c[0] == BOTTOM :
                ball = [BOTTOM, c[1] + c[10].get_width() // 2 , c[2] - c[10].get_height() // 4]
            elif c[0] == LEFT  :
                ball = [LEFT, c[1] + c[10].get_width()+ c[10].get_width() // 4 , c[2] + c[10].get_height() // 2]
            elif c[0] == RIGHT  :
                ball = [RIGHT, c[1] +  - c[10].get_width() // 4 , c[2] + c[10].get_height() // 2]
                
            c[8].append(ball)

def get_count():
    return len(_cannon_list)

def get_fire_rate(idx):
    return _cannon_list[idx][4]

def get_move_rate(idx):
    return _cannon_list[idx][7]

def get_fire_rate(idx):
    return _cannon_list[idx][5]

def get_ball_vel(idx):
    return _cannon_list[idx][9]

def set_move_rate(move_rate, idx=-1):
    if idx != -1:
        _cannon_list[idx][7] = move_rate
        return
    
    for c in _cannon_list:
        c[7] = move_rate

def set_fire_rate(fire_rate, idx=-1):
    if fire_rate <= 0.01:
        fire_rate = 0.01
    
    if idx != -1:
        _cannon_list[idx][5] = fire_rate
        return
    
    for c in _cannon_list:
        c[5] = fire_rate

def set_ball_vel(ball_vel, idx=-1):
    if idx != -1:
        _cannon_list[idx][9] = ball_vel
        return
    
    for c in _cannon_list:
        c[9] = ball_vel

def check_collision(pos, radius):
    rv = False
    for c in _cannon_list:
        for cball in c[8]:
            dist = ((pos[0] - cball[1]) ** 2 + (pos[1] - cball[2]) ** 2) ** 0.5
            if dist <= (radius + c[10].get_width() // 2):
                c[8].remove(cball)
                rv = True

    return rv
