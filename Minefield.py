#! /usr/bin/env python

import os
import random
import pygame
import math
import sys
import time

# Player 1 -> w, a, s, d, f, g, r
# Player 2 -> up, left, down, right, l, k, o

WINDOW_W = 1050
WINDOW_H = 600

FPS = 30

pygame.display.set_caption("Minefield")
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))

pygame.init()
EXPLO_SOUND = pygame.mixer.Sound('sounds/explo.ogg')
WIN_SOUND = pygame.mixer.Sound('sounds/win.ogg')
LOSE_SOUND = pygame.mixer.Sound('sounds/lose.ogg')

SOUND = True
SHOW_SIGHT = False

BGCOLOR = (0, 0, 0)
if(len(sys.argv) == 2):
    if sys.argv[1] == 'test':
        BGCOLOR = (255, 255, 255)

def play_sound(sound):
    if(SOUND):
        sound.play()


clock = pygame.time.Clock()

class Player(object):
    
    # Key Binds
    LEFT_KEY = pygame.K_a
    RIGHT_KEY = pygame.K_d
    UP_KEY = pygame.K_w
    DOWN_KEY = pygame.K_s

    GOAL_SIZE = 50

    DEFAULT_SPEED = 5
    INIT_SIGHT = 8
    SIGHT_INCR = 0.5

    # Do not change!!!
    SPEED_CONST = 30

    def __init__(self, name, x, y, color, goal):
        self.name = name
        self.init_x = x
        self.init_y = y
        self.x = x
        self.y = y
        self.rad = PLAYER_SIZE
        self.color = color
        self.spd = 5

        self.goal = goal

        self.sight = Player.INIT_SIGHT
        self.delay_time = time.time()
        self.seconds = 0

        self.LEFT_KEY = Player.LEFT_KEY
        self.RIGHT_KEY = Player.RIGHT_KEY
        self.UP_KEY = Player.UP_KEY
        self.DOWN_KEY = Player.DOWN_KEY

    def handle_keys(self):

        # Handles delay
        if(abs(time.time()-self.delay_time) >= self.seconds):
            self.seconds = 0
            self.delay_time = time.time()
        else:
            return

        spd = self.spd * Player.SPEED_CONST/FPS

        key = pygame.key.get_pressed()
        if key[self.LEFT_KEY]:
            self.x-=spd
        elif key[self.RIGHT_KEY]:
            self.x+=spd
        elif key[self.UP_KEY]:
            self.y-=spd
        elif key[self.DOWN_KEY]:
            self.y+=spd

    def set_keybinds(self, left, right, up, down):
        self.LEFT_KEY = left
        self.RIGHT_KEY = right
        self.UP_KEY = up
        self.DOWN_KEY = down

    def bounds(self):
        if self.x>WINDOW_W-self.rad:
            self.x = WINDOW_W-self.rad
        if self.x<self.rad:
            self.x = self.rad
        if self.y>WINDOW_H-self.rad:
            self.y = WINDOW_H-self.rad
        if self.y<self.rad:
            self.y = self.rad

    def delay(self, seconds):
        self.delay_time = time.time()
        self.seconds = seconds

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y

    def check_win(self):
        if self.x>self.goal.goal_x and self.y>self.goal.goal_y and self.x<(self.goal.goal_x+Player.GOAL_SIZE) and self.y<(self.goal.goal_y+Player.GOAL_SIZE):
            return True
        return False

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.rad)
        if(SHOW_SIGHT):
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.sight, 1)

class Goal(object):
    def __init__(self, goal_x, goal_y, goal_x_out, goal_y_out, goal_color):
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_x_out = goal_x_out
        self.goal_y_out = goal_y_out
        self.goal_color = goal_color

class Mine(object):
    # Hidden, Shown, Peaked
    MINE_COLORS = [(0, 0, 0), (255, 165, 0), (50, 30, 0)]
    MINE_SIZE = 10
    COLLISION_RANGE = 12

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.id = 0         # 0 for hidden, 1 for found, 2 for peaked
        self.p_name = ''

    def draw(self):
        pygame.draw.rect(screen, Mine.MINE_COLORS[self.id], (self.x, self.y, Mine.MINE_SIZE, Mine.MINE_SIZE))


class Mines(object):
    def __init__(self):
        self.mines = []
        for i in range(0, NUM_OF_MINES):
            xr = random.randint(5, WINDOW_W-5)
            yr = random.randint(5, WINDOW_H-5)

            if not(xr<100 and yr<100 or xr>WINDOW_W-100 and yr>WINDOW_H-100):
                self.mines.append(Mine(xr, yr))
            
    def draw(self):
        for mine in self.mines:
            mine.draw()
    def print(self):
        for mine in self.mines:
            print(str(mine.x)+','+str(mine.y))

    def collide(self, player):

        for mine in self.mines:
            dist = math.sqrt(math.pow((mine.x+Mine.MINE_SIZE/2 - player.x), 2) + math.pow((mine.y+Mine.MINE_SIZE/2 - player.y), 2))
            if (dist < Mine.COLLISION_RANGE):
                play_sound(EXPLO_SOUND)
                if(mine.id == 0):
                    player.sight += Player.SIGHT_INCR
                mine.id = 1
                player.reset()
                player.delay(0.1)

            if (dist <= player.sight) and mine.id == 0:
                mine.id = 2
                mine.p_name = player.name
            elif (mine.id == 2) and dist > player.sight and mine.p_name == player.name:
                mine.id = 0
                mine.p_name = ''

def check_player_collisions():
    for i in range(0, len(players)):
        for j in range(i+1, len(players)):
            dist = math.sqrt(math.pow(players[i].x - players[j].x, 2) + math.pow(players[i].y - players[j].y, 2))
            if(dist < (2*PLAYER_SIZE)):
                play_sound(EXPLO_SOUND)
                players[i].reset()
                players[i].delay(0.1)
                players[j].reset()
                players[j].delay(0.1)

def reveal_mines():
    for mine in mines.mines:
        mine.id = 1


NUM_OF_MINES = int(WINDOW_W/6.5)

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

goal1 = Goal(WINDOW_W-Player.GOAL_SIZE, WINDOW_H-Player.GOAL_SIZE, WINDOW_W-Player.GOAL_SIZE*2, WINDOW_H-Player.GOAL_SIZE*2, GOAL_COLOR1)
goal2 = Goal(0, 0, 0, 0, GOAL_COLOR2)

player1 = Player("Player 1", SX1, SY1, COLOR1, goal1)
player2 = Player("Player 2", SX2, SY2, COLOR2, goal2)

player2.set_keybinds(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)

players = [player1, player2]

mines = Mines()
#mines.print()

pygame.init()
clock = pygame.time.Clock()

running = True

def game():
    
    game_over = False

    while not(game_over):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        screen.fill(BGCOLOR)
        for player in players:
            player.handle_keys()
            player.bounds()
            player.draw()

            pygame.draw.rect(screen, player.goal.goal_color, (player.goal.goal_x, player.goal.goal_y, Player.GOAL_SIZE, Player.GOAL_SIZE))
            pygame.draw.rect(screen, player.goal.goal_color, (player.goal.goal_x_out, player.goal.goal_y_out, Player.GOAL_SIZE*2, Player.GOAL_SIZE*2), 1)
            
            if player.check_win():
                print(player.name + " won!")
                play_sound(WIN_SOUND)
                game_over = True

            mines.collide(player)
            check_player_collisions()
        
        if(game_over):
            reveal_mines()
            for player in players:
                player.delay(3)
                player.reset()

        mines.draw()

        pygame.display.update()
        clock.tick(30)

running = True

mines = Mines()
game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        mines = Mines()
        game()