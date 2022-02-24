#!/usr/bin/python

import pygame, sys, random, math
from pygame.locals import *

# Constants
INITIAL_PLAYER_X = 468
INITIAL_Y = 138
INITIAL_BALL_X = 5

clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 300))

MISS_TEXT_X = 200
MISS_TEXT_Y = 10

QUIT_TEXT_X = 200
QUIT_TEXT_Y = 280

class Player():
    """
    Class for the player model

    Attributes
    -----------
    x : int
        x coordinate
    y : int
        y coordinate
    yChange : int 
        change in y (for movement)
    icon : pygame.iamge
        sprite for the player
    """
    def __init__(self):
        self.x = INITIAL_PLAYER_X
        self.y = INITIAL_Y
        self.yChange = 0
        self.icon = pygame.image.load('gun.png')

    def draw(self):
        """ Draws model with bounds checking """
        self.y += self.yChange

        if self.y <= 0: self.y = 0
        elif self.y >= 268: self.y = 268

        screen.blit(self.icon, (self.x, self.y))

    def move_up(self):
        self.yChange = -5
    
    def move_down(self):
        self.yChange = 5

    def stop(self):
        self.yChange = 0
        

class Ball():
    """
    Class for the ball model

    Attributes
    -----------
    x : int
        x coordinate
    y : int
        y coordinate
    yChange : int 
        change in y (for movement)
    icon : pygame.iamge
        sprite for the ball
    rising : bool
        flag for ball direction
    last : int
        time at which rising was last changed
    cooldown : int
        random int from 0.5 sec to 3 sec until rising can be changed
    """

    def __init__(self):
        self.x = INITIAL_BALL_X
        self.y = INITIAL_Y
        self.yChange = 0
        self.rising = 0
        self.last = pygame.time.get_ticks()
        self.cooldown = random.randint(500, 3000)
        self.icon = pygame.image.load('ball.png')

    def draw(self):
        """ Draws model with bounds checking """
        self.y += self.yChange

        if self.y <= 0: self.y = 0
        elif self.y >= 268: self.y = 268

        screen.blit(self.icon, (self.x, self.y))
    
    def move_up(self):
        self.yChange = -5
    
    def move_down(self):
        self.yChange = 5

    def changeDir(self):
        """
        Waits until a time cooldown has passed and toggles the direction of the balloon

        Resets last time and creates new cooldown
        """
        now = pygame.time.get_ticks()
        if now - self.last >= self.cooldown:
            self.last = now
            self.rising = not self.rising
            self.cooldown = random.randint(500, 3000)
    
class Bullet():
    """
    Class for the bullet model

    Attributes
    -----------
    x : int
        x coordinate
    y : int
        y coordinate
    xChange : int 
        change in x (for movement)
    icon : pygame.iamge
        sprite for the bullet
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xChange = -50
        self.icon = pygame.image.load('bullet.png')

    def draw(self):
        """ Draws model with bounds checking """
        self.x += self.xChange
        screen.blit(self.icon, (self.x, self.y))

def collisionDetect(ballX, ballY, bulletX, bulletY):
    """
    Collision detection function

    Returns : bool 
        True when collision is detected
        
        False otherwise
    """
    distance = math.sqrt((math.pow(ballX - bulletX, 2)) + math.pow(ballY - bulletY, 2))
    if distance < 20:
        return True
    else: 
        return False

def show_misses(misses, font):
    missText = font.render("Misses: " + str(misses), True, (0, 0, 0))
    screen.blit(missText, (MISS_TEXT_X, MISS_TEXT_Y))

def show_quit(font):
    quitText = font.render("Press Q to quit", True, (0, 0, 0))
    screen.blit(quitText, (QUIT_TEXT_X, QUIT_TEXT_Y))

def main():
    """ Handles the main loop of the game and initialises pyGame """
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 12)
    random.seed()
    bullets = []
    misses = 0

    pygame.display.set_caption("Balloon Shooter")

    player = Player()
    ball = Ball()

    while 1:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_DOWN:
                    player.move_down()
                if event.key == pygame.K_UP:
                    player.move_up()
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x - 16, player.y + 5))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or pygame.K_UP:
                    player.stop()

        # Toggles direction of ball at random intervals
        ball.changeDir()

        if ball.rising:
            ball.move_up()
        else:
            ball.move_down()

        player.draw()
        ball.draw()
        
        # Manages bullets 
        for bullet in bullets:
            bullet.draw()
            collision = collisionDetect(ball.x, ball.y, bullet.x, bullet.y)
            
            if collision:
                pygame.quit()
                sys.exit()
            if bullet.x <= 0:
                bullets.remove(bullet)
                misses += 1

        show_misses(misses, font)
        show_quit(font)
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__': main()