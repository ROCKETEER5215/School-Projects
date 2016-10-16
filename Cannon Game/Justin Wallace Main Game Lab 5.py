
import pygame
import math
import time
import cannons

def load_frames(name, states, colorkey, frames_per_state):
    dirstr = ('n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw')
    
    frames = []
    for s in states:
        tmpstr0 = name + '/' + s + '/' + s + ' '
        frames.append([])
        for d in dirstr:
            tmpstr1 = tmpstr0 + d
            frames[-1].append([])
            for i in range(0, frames_per_state):
                tmpstr2 = tmpstr1 + '0' * (4 - len(str(i))) + str(i) + '.bmp'
                tmpimg = pygame.image.load(tmpstr2).convert()
                tmpimg.set_colorkey(colorkey)
                frames[-1][-1].append(tmpimg)
    
    return frames

def draw_healthbar(surface, rect, health, max_health, bcolor=(0,0,0),\
				   icolor=(255,0,0), border=3):
    pygame.draw.rect(surface, bcolor, rect)
    
    if health > 0:
        k = health / max_health
        x = rect[0] + border
        w = (rect[2] - 2*border) * k
        h = (rect[3] - 2 * border) 
        y = rect[1] + rect[3] - border + (2 * border - rect[3])
    
        pygame.draw.rect(surface, icolor, (x, y, w, h))

# Main Game
pygame.init()
win_size = (1050,650)
win = pygame.display.set_mode(win_size)
background = (0, 0, 0)
# curLevel
curLevel = 0

# curTrans
curTrans = 1

# Key
key = pygame.image.load('key.png').convert_alpha()
kx = 525
ky = 325
kr = int( key.get_width()/2)
tx= 525
ty= 325
kpx = int(kx -key.get_width()/2)
kpy = int(ky -key.get_height()/2)
Enter = False
# cannon
frate = 1.6
cspeed = 50
bspeed = 170
# font
levfont = pygame.font.Font('This Night.ttf', 40)
gameover = pygame.font.Font('Scream Again.ttf', 20)
Level = 0
# level images
#levelone = pygame.image.load('GameBackground.png').convert_alpha()
levelone = pygame.image.load('Level 1.png').convert_alpha()
leveltwo = pygame.image.load('Level 2.png').convert_alpha()
levelthree = pygame.image.load('Level 3.png').convert_alpha()
levX=0
levY=0
# SWAMPTHING 
N = 0
NE = 1
E = 2
SE = 3
S = 4
SW = 5
W = 6
NW = 7
# 1 / sqrt(2) stored for fixing speed when moving diagonally
recsq2 = 1.0 / (2 ** 0.5)
# swampthing's attributes
# swampthing's states
RUNNING = 1
WALKING = 0
swampthing_pos = [525, 325]
swampthing_speed = (win_size[0] / 5000.0, win_size[0] / 1500.0)
swampthing_frames = load_frames('swampthing', ('running', 'walking'), (106, 76, 48), 8)
swampthing_frame_idx = 0
swampthing_state = RUNNING 
swampthing_dir = W
SWAMPTHING_FRAME_DELAY = (80, 40)
swampthing_curframe_delay = SWAMPTHING_FRAME_DELAY[swampthing_state]
swampthing_max_health = 100
swampthing_health = swampthing_max_health
swampthing_radius = swampthing_frames[0][0][0].get_width() // 13
# use pygame's clock object for keeping track of time
clock = pygame.time.Clock()
totalTime = 0
startTime = time.time()
# list of pressed keys
key_pressed = []
done = False
while not done:
    # Atime
    stopTime = time.time()
    Atime = stopTime - startTime
    startTime = stopTime
    #get frame time
    dtime = clock.tick()
    totalTime += dtime
    #get input
    evt_list = pygame.event.get()
    for evt in evt_list:
        if evt.type == pygame.QUIT:
            done = True
        elif evt.type == pygame.KEYDOWN:
            key_pressed.append(evt.key)
            if evt.key == pygame.K_SPACE:
                Enter = True
        elif evt.type == pygame.KEYUP:
            key_pressed.remove(evt.key)
    
    #--------------
    # UPDATE
    #--------------
    
    # update swampthing
    #--------------
    # get direction based on key pressed
    dx = 0 # change in x
    if pygame.K_LEFT in key_pressed or pygame.K_a in key_pressed:
        dx = -1
    if pygame.K_RIGHT in key_pressed or pygame.K_d in key_pressed:
        dx = 1
    dy = 0 # change in y
    if pygame.K_UP in key_pressed or pygame.K_w in key_pressed:
        dy = -1
    if pygame.K_DOWN in key_pressed or pygame.K_s in key_pressed:
        dy = 1
    
    # update direction animation state based on dx,dy
    if dy > 0:
        if dx > 0:
            swampthing_dir = SE
        elif dx < 0:
            swampthing_dir = SW
        else:
            swampthing_dir = S
    elif dy < 0:
        if dx > 0:
            swampthing_dir = NE
        elif dx < 0:
            swampthing_dir = NW
        else:
            swampthing_dir = N
    else:
        if dx > 0:
            swampthing_dir = E
        elif dx < 0:
            swampthing_dir = W
        else:
            swampthing_curframe_delay = SWAMPTHING_FRAME_DELAY[swampthing_state]
            swampthing_frame_idx = 0
    # update animation if  moving
    if dx != 0 or dy != 0:
        swampthing_curframe_delay -= dtime
        while swampthing_curframe_delay <= 0:
            swampthing_curframe_delay += SWAMPTHING_FRAME_DELAY[swampthing_state]
            swampthing_frame_idx += 1
            if swampthing_frame_idx == len(swampthing_frames[swampthing_state][swampthing_dir]):
                swampthing_frame_idx = 0
    # update dx,dy based on speed
    if dx != 0 and dy != 0:
        dx *= swampthing_speed[swampthing_state] * recsq2
        dy *= swampthing_speed[swampthing_state] * recsq2
    else:
        dx *= swampthing_speed[swampthing_state]
        dy *= swampthing_speed[swampthing_state]
    # apply  speed and direction to position with respect to time
    swampthing_pos[0] += dx * dtime
    swampthing_pos[1] += dy * dtime
#MAIN GAME LOOP
    
# swampthiing update pos
    f = swampthing_frames[swampthing_state][swampthing_dir][swampthing_frame_idx]
    tmpx = int(swampthing_pos[0] - f.get_width() / 2)
    tmpy = int(swampthing_pos[1] - f.get_height() / 2)
    tmx = int(swampthing_pos[0])
    tmy = int(swampthing_pos[1])

# COLLISION and game over screen
    if cannons.check_collision((tmx, tmy), swampthing_radius):
        swampthing_health -= 10
        if swampthing_health <= 0:
            curTrans = 0
            curLevel = 0
            Enter = False
    if ( curLevel == 0 and curTrans == 0 and swampthing_health<= 0):
        pygame.draw.rect(win, (0,0,0),(0,0,1050,650))
        fontimg = gameover.render("GAME OVER, Press Space Bar to Quit", True, (0, 255, 0))
        fpx = int(tx - fontimg.get_width() / 2)
        fpy = int(ty - fontimg.get_height() / 2)                           
        win.blit(fontimg, (fpx, fpy))
        gameimg = gameover.render("total time " + str(totalTime) , True, (0, 255, 0))
        gfx = int(tx - gameimg.get_width() / 2)
        gfy = fpy + int(ty - gameimg.get_height() / 2)
        win.blit(gameimg, (gfx, gfy))
    if (curLevel == 0 and curTrans == 0 and Enter == True):
        done = True 
    
# Level One
    # level Transition
    if (curLevel == 0 and curTrans == 1):
        pygame.draw.rect(win, (0,0,0),(0,0,1050,650))
        fontimg = levfont.render("Level 1, Press Space Bar", True, (0, 255, 0))
        fpx = int(tx - fontimg.get_width() / 2)
        fpy = int(ty - fontimg.get_height() / 2)
        win.blit(fontimg, (fpx, fpy))
     # Add level cannons    
    if (curLevel == 0 and curTrans == 1 and Enter == True):
        curLevel += 1
        cannons.add_cannon(cannons.LEFT, (39, 59, 226), frate, cspeed, bspeed)
        cannons.add_cannon(cannons.RIGHT, (255, 8, 0), frate, cspeed, bspeed)
    # level screen    
    if (curLevel == 1 and curTrans == 1):
        swampthing_state = RUNNING
        # level background
        background = levelone
        win.blit(background, (levX, levY))
        # swampthing draw to window
        win.blit(f, (tmpx, tmpy))
        tmppos = (int(swampthing_pos[0]),int(swampthing_pos[1]))
        #pygame.draw.circle(win, (255, 0, 0), tmppos, swampthing_radius, 1)
        # Hud
        pygame.draw.rect(win, (128,128,128),(0,0,1050,70))
        # health bar
        draw_healthbar(win, (470, 10, 100, 50), swampthing_health, swampthing_max_health)
        if (totalTime >= 60000 and totalTime < 120000 ):
            win.blit(key, (kpx, kpy))
            #pygame.draw.circle(win, (255, 0, 0), (kx,ky), kr, 1)
            dist = ((tmx - kx ) ** 2 + (tmy - ky) ** 2) ** 0.5
            if dist <= kr:
                Enter = False
                curTrans += 1 
# Level Two
    # level Transition
    if (curLevel == 1 and curTrans == 2):
        pygame.draw.rect(win, (0,0,0),(0,0,1050,650))
        fontimg = levfont.render("Level 2, Press Space Bar", True, (0, 255, 0))
        fpx = int(tx - fontimg.get_width() / 2)
        fpy = int(ty - fontimg.get_height() / 2)
        win.blit(fontimg, (fpx, fpy))
    # Add level cannons    
    if (curLevel == 1 and curTrans == 2 and Enter == True):
        curLevel +=1
        swampthing_health = 100
        cannons.add_cannon(cannons.BOTTOM, (191, 0, 255), frate, cspeed, bspeed)
        cannons.add_cannon(cannons.TOP, (57, 255, 20), frate, cspeed, bspeed)
    # level screen  
    if (curLevel == 2 and curTrans == 2):
        swampthing_state = RUNNING 
        background = leveltwo
        win.blit(background, (levX, levY))
        # swampthing drawn to window
        win.blit(f, (tmpx, tmpy))
        pygame.draw.rect(win, (128,128,128),(0,0,1050,70))
        draw_healthbar(win, (470, 10, 100, 50), swampthing_health, swampthing_max_health)
        if (totalTime >= 120000 and totalTime < 180000):
            win.blit(key, (kpx, kpy))
            dist = ((tmx - kx) ** 2 + (tmy - ky) ** 2) ** 0.5
            if dist <= kr:
                Enter = False
                curTrans += 1 
# Level Three
    # level Transition
    if (curLevel == 2 and curTrans == 3):
        pygame.draw.rect(win, (0,0,0),(0,0,1050,650))
        fontimg = levfont.render("Level 3, Press Space Bar", True, (0, 255, 0))
        fpx = int(tx - fontimg.get_width() / 2)
        fpy = int(ty - fontimg.get_height() / 2)
        win.blit(fontimg, (fpx, fpy))
    # Add level cannons
    if (curLevel == 2 and curTrans == 3 and Enter == True):
        swampthing_health = 100
        curLevel += 1
        cannons.add_cannon(cannons.LEFT, (0, 0, 255), frate, cspeed, bspeed)
        cannons.add_cannon(cannons.RIGHT, (255, 0, 0), frate, cspeed, bspeed)
    # level screen
    if (curLevel == 3 and curTrans == 3):
        swampthing_state = RUNNING
        # level background
        background = levelthree
        win.blit(background, (levX, levY))
        # swampthing drawn to window
        win.blit(f, (tmpx, tmpy))
        # Hud
        pygame.draw.rect(win, (128,128,128),(0,0,1050,70))
        # health bar
        draw_healthbar(win, (470, 10, 100, 50), swampthing_health, swampthing_max_health)
        if (totalTime >= 180000 and totalTime < 240000):
            win.blit(key, (kpx, kpy))
            dist = ((tmx - kx) ** 2 + (tmy - ky) ** 2) ** 0.5
            if dist <= kr:
                Enter = False
                curLevel +=1
                curTrans +=1 
    # Ending
    if (curLevel == 4 and curTrans == 4):
        pygame.draw.rect(win, (0,0,0),(0,0,1050,650))
        fontimg = levfont.render("Wozer!!! You Won,Press Space Bar to Quit", True, (0, 255, 0))
        fpx = int(tx - fontimg.get_width() / 2)
        fpy = int(ty - fontimg.get_height() / 2)
        win.blit(fontimg, (fpx, fpy))
        gameimg = gameover.render("total time" +str(totalTime), True, (0, 255, 0))
        gfx = int(tx - gameimg.get_width() / 2)
        gfy = fpy + int(ty - gameimg.get_height() / 2)
        win.blit(gameimg, (gfx, gfy))
        if(curLevel == 4 and curTrans == 4 and Enter == True):
            done = True
# update screen and cannons
    cannons.update_cannons(Atime)
    cannons.draw_cannons(win)
    pygame.display.flip()
pygame.quit()


