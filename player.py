import pygame
import time

class Player(object):
    
    # Key Binds
    LEFT_KEY = pygame.K_a
    RIGHT_KEY = pygame.K_d
    UP_KEY = pygame.K_w
    DOWN_KEY = pygame.K_s

    GOAL_SIZE = 50

    PLAYER_SIZE = 8
    SHOW_SIGHT = False
    SHOW_OPP_SIGHT = False

    DEFAULT_SPEED = 5
    INIT_SIGHT = 8
    SIGHT_INCR = 1
    OPP_SIGHT_MULTIPLIER = 4

    # Do not change!!!
    SPEED_CONST = 30

    def __init__(self, name, x, y, color, goal):
        self.name = name
        self.init_x = x
        self.init_y = y
        self.x = x
        self.y = y
        self.rad = Player.PLAYER_SIZE
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

    def handle_keys(self, fps):

        # Handles delay
        if(abs(time.time()-self.delay_time) >= self.seconds):
            self.seconds = 0
            self.delay_time = time.time()
        else:
            return

        spd = self.spd * Player.SPEED_CONST/fps

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

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.rad)
        if(Player.SHOW_SIGHT):
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.sight, 1)
        if(Player.SHOW_OPP_SIGHT):
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.OPP_SIGHT_MULTIPLIER*self.sight, 1)

    def draw_goal(self, surface):
        pygame.draw.rect(surface, self.goal.goal_color, (self.goal.goal_x, self.goal.goal_y, Player.GOAL_SIZE, Player.GOAL_SIZE))
        pygame.draw.rect(surface, self.goal.goal_color, (self.goal.goal_x_out, self.goal.goal_y_out, Player.GOAL_SIZE*2, Player.GOAL_SIZE*2), 1)

class Goal(object):
    def __init__(self, goal_x, goal_y, goal_x_out, goal_y_out, goal_color):
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_x_out = goal_x_out
        self.goal_y_out = goal_y_out
        self.goal_color = goal_color