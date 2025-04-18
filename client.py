import pygame
from network import Network
from player import Player, Goal

import os
import random
import pygame
import math
import sys
import time
import data
from protocol import data_protocol

WINDOW_W = 1050
WINDOW_H = 600

FPS = 30

NUM_OF_MINES = data.NUM_OF_MINES

GOAL_COLOR1 = (255, 255, 0)
GOAL_COLOR2 = (128, 0, 128)

# Player ideally spawns in 50 pixels from horizontal and vertical bounds next to goal

PLAYER_SIZE = 8
SX1 = 50 + PLAYER_SIZE
SY1 = 50 + PLAYER_SIZE
COLOR1 = (0, 255, 0)
SX2 = WINDOW_W-Player.GOAL_SIZE-PLAYER_SIZE
SY2 = WINDOW_H-Player.GOAL_SIZE-PLAYER_SIZE
COLOR2 = (255, 0, 0)

pygame.display.set_caption("Minefield")
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))

pygame.init()
EXPLO_SOUND = pygame.mixer.Sound('sounds/explo.ogg')
WIN_SOUND = pygame.mixer.Sound('sounds/win.ogg')
LOSE_SOUND = pygame.mixer.Sound('sounds/lose.ogg')
LOCATOR_SOUND = pygame.mixer.Sound('sounds/locator.ogg')

SOUND = True
HIDE_OPPONENT = True

BGCOLOR = (0, 0, 0)
if(len(sys.argv) == 2):
    if sys.argv[1] == 'test':
        BGCOLOR = (255, 255, 255)

def play_sound(sound):
    if(SOUND):
        sound.play()

def bounds(player):
    if player.x>WINDOW_W-player.rad:
        player.x = WINDOW_W-player.rad
    if player.x<player.rad:
        player.x = player.rad
    if player.y>WINDOW_H-player.rad:
        player.y = WINDOW_H-player.rad
    if player.y<player.rad:
        player.y = player.rad

def check_player_collisions():
    dist = math.sqrt(math.pow(player.x - opp.x, 2) + math.pow(player.y - opp.y, 2))
    if(dist < (2*PLAYER_SIZE)):
        play_sound(EXPLO_SOUND)
        player.reset()
        player.delay(0.1)
        return True
    return False

def in_sight():
    dist = math.sqrt(math.pow(player.x - opp.x, 2) + math.pow(player.y - opp.y, 2))
    return dist < (Player.OPP_SIGHT_MULTIPLIER*player.sight)


class Mine(object):
    # Hidden, Shown, Peaked
    MINE_COLORS = [(0, 0, 0), (255, 165, 0), (50, 30, 0)]
    MINE_SIZE = 10
    COLLISION_RANGE = 12

    def __init__(self, x, y):
        self.x = x-Mine.MINE_SIZE/2
        self.y = y-Mine.MINE_SIZE/2
        self.id = 0         # 0 for hidden, 1 for found, 2 for peaked

    def draw(self):
        pygame.draw.rect(screen, Mine.MINE_COLORS[self.id], (self.x, self.y, Mine.MINE_SIZE, Mine.MINE_SIZE))

    def collide(self):
        dist = math.sqrt(math.pow((self.x+Mine.MINE_SIZE/2 - player.x), 2) + math.pow((self.y+Mine.MINE_SIZE/2 - player.y), 2))
        dist_loc = math.sqrt(math.pow((self.x+Mine.MINE_SIZE/2 - loc.x), 2) + math.pow((self.y+Mine.MINE_SIZE/2 - loc.y), 2))
        
        if (dist < Mine.COLLISION_RANGE):
            play_sound(EXPLO_SOUND)
            if(self.id == 0):
                player.sight += Player.SIGHT_INCR
            self.id = 1
            player.reset()
            player.delay(0.1)
            return True

        if (dist <= player.sight or dist_loc <= Locator.SIGHT) and self.id == 0:
            self.id = 2
            self.p_name = player.name
        elif (self.id == 2) and (dist > player.sight and dist_loc > Locator.SIGHT):
            self.id = 0


class Mines(object):
    def __init__(self, text):
        self.mines = []
        locs = text.split(',')
        for i in range(0, len(locs)-1, 2):
            self.mines.append(Mine(int(locs[i]), int(locs[i+1])))

    def print(self):
        for mine in self.mines:
            print(str(mine.x)+','+str(mine.y))


def reveal_mines():
    for mine in mines.mines:
        mine.id = 1


class Locator(object):
    SIGHT = 100
    ptime = time.time()
    DELAY = 10
    RAD = 6
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def hide(self):
        self.x = -2*Locator.SIGHT
        self.y = -2*Locator.SIGHT
    def move(self, x, y):
        self.x = x
        self.y = y
    def collide(self, p):
        dist = math.sqrt(math.pow((self.x - p.x), 2) + math.pow((self.y - p.y), 2))
        return dist < (Locator.RAD+data.PLAYER_SIZE)
    def can_see(self, p):
        dist = math.sqrt(math.pow((self.x - p.x), 2) + math.pow((self.y - p.y), 2))
        return dist < Locator.SIGHT
    def draw(self, color):
        if not(self.x <= 2*data.GOAL_SIZE and self.x >= data.WINDOW_W-2*data.GOAL_SIZE) and not(self.y <= 2*data.GOAL_SIZE and self.y >= data.WINDOW_H-2*data.GOAL_SIZE):
            pygame.draw.polygon(screen, color, ((self.x-math.sin(math.pi/3)*Locator.RAD, self.y+math.cos(math.pi/3)*Locator.RAD),
                                (self.x+math.sin(math.pi/3)*Locator.RAD, self.y+math.cos(math.pi/3)*Locator.RAD),
                                (self.x, self.y-Locator.RAD)))


pygame.init()
clock = pygame.time.Clock()

running = True

ipaddr = open("ipconfig").read().strip()

n = Network(ipaddr)
init_data = n.getInitData()
player = init_data[0]
opp = init_data[1]

loc = Locator(-2*Locator.SIGHT, -2*Locator.SIGHT)
oppLoc = Locator(-2*Locator.SIGHT, -2*Locator.SIGHT)

minestr = n.getMineString()
mines = Mines(minestr)

def game():
    run = True
    clock = pygame.time.Clock()
    
    print("hi")

    while run:

        clock.tick(60)

        screen.fill(BGCOLOR)
        
        player.handle_keys(FPS)
        bounds(player)
        player.draw(screen)
        player.draw_goal(screen)

        # -1 for no explosion, index of mine that was hit
        mi = -1
        # 0 for nothing, 1 for player collision, 2 for locator, 3 for win
        uid = 0

        extra = [0, 0]

        # Spawn locator
        key = pygame.key.get_pressed()
        if key[pygame.K_f]:
            if (time.time()-Locator.ptime) >= Locator.DELAY:
                play_sound(LOCATOR_SOUND)
                loc.move(player.x, player.y)
                Locator.ptime = time.time()
                uid = 2
                extra = [player.x, player.y]

        if(loc.collide(opp)):
            uid = 1

        if(check_player_collisions()):
            uid = 1

        for i in range(0, len(mines.mines)):
            mines.mines[i].draw()
            if(mines.mines[i].collide()):
                mi = i
                uid = 0

        if player.check_win():
            print(player.name + " won!")
            play_sound(WIN_SOUND)
            player.reset()
            player.delay(3)
            reveal_mines()
            uid = 3
            run = False

        # Send Data
        data_packed = data_protocol(player.x, player.y, mi, uid, extra=extra)
        n.send(data_packed)

        # Collect Data
        pos_data = n.getPosData()
        if(pos_data != None):
            if(int(pos_data[3])==0):
                opp.x, opp.y = float(pos_data[0]), float(pos_data[1])
            elif(int(pos_data[3])==1):
                play_sound(EXPLO_SOUND)
                player.reset()
                player.delay(0.1)
            elif(int(pos_data[3])==2):
                play_sound(LOCATOR_SOUND)
                oppLoc.move(int(float(pos_data[4])), int(float(pos_data[5])))
                opp.x, opp.y = float(pos_data[0]), float(pos_data[1])
                pass
            elif(int(pos_data[3])==3):
                play_sound(LOSE_SOUND)
                player.reset()
                reveal_mines()
                player.delay(3)
                print(opp.name + " won!")
                run = False
            
            # Check which mine exploded
            if(int(pos_data[2])>-1):
                opp.sight += Player.SIGHT_INCR
                play_sound(EXPLO_SOUND)
                mines.mines[int(pos_data[2])].id = 1


        if not(HIDE_OPPONENT) or in_sight() or loc.can_see(opp):
            opp.draw(screen)
        opp.draw_goal(screen)

        loc.draw(player.color)
        oppLoc.draw(opp.color)


        pygame.display.update()
        clock.tick(30)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


game()
game()

n.close()