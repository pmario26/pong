import pygame
from pygame.locals import *
import random

class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize

        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)

        self.radius = 8

        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)

        self.color = (100,100,255)
        

        vector = [ 1,-1]
        self.direction = [vector[random.randint(0,1)],vector[random.randint(0,1)]]

        self.speedx = 2
        self.speedy = 5
        #CODE TASK: change speed/radius as game progresses to make it harder
        #CODE BONUS: adjust ratio of x and y speeds to make it harder as game progresses

        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle, ai_paddle_0,ai_paddle_1,ai_paddle_2):

        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        '''if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1'''

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        #CODE TASK: Change the direction of the pong, based on where it hits the paddles (HINT: check the center points of each)

        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] *= -1            
        if self.rect.colliderect(ai_paddle_0.rect):
            self.direction[0] *= -1
        if self.rect.colliderect(ai_paddle_1.rect):
            self.direction[1] *= -1
        if self.rect.colliderect(ai_paddle_2.rect):
            self.direction[1] *= -1        

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)


class AIPaddle_vert(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = 5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (255,100,100)

        #CODE TASK: Adjust size of AI paddle as match progresses to make it more difficult

        self.speed = 3

    def update(self, pong):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)
    
class AIPaddle_hor(object):
    def __init__(self, screensize,top):
        self.screensize = screensize

        self.centerx = int(screensize[0]*0.5)
        if (top):
            self.centery = 5
        else :
            self.centery = 475
        self.height = 10
        self.width = 100

        self.rect = pygame.Rect(self.centerx-int(self.width*0.5),0, self.width, self.height)

        self.color = (255,100,100)

        #CODE TASK: Adjust size of AI paddle as match progresses to make it more difficult

        self.speed = 3

    def update(self, pong):
        if pong.rect.left < self.rect.left:
            self.centerx -= self.speed
        elif pong.rect.right > self.rect.right:
            self.centerx += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)



class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (100,255,100)

        #CODE TASK: Adjust size of Player paddle as match progresses to make it more difficult

        self.speed = 3
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed

        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


def main():
    pygame.init()

    screensize = (640,480)

    screen = pygame.display.set_mode(screensize)

    clock = pygame.time.Clock()

    pong = Pong(screensize)
    ai_paddle_0 = AIPaddle_vert(screensize)
    ai_paddle_1 = AIPaddle_hor(screensize,1)
    ai_paddle_2 = AIPaddle_hor(screensize,0)
    player_paddle = PlayerPaddle(screensize)

    running = True

    while running:
        #fps limiting/reporting phase
        clock.tick(64)

        #event handling phase
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    player_paddle.direction = -1
                elif event.key == K_DOWN:
                    player_paddle.direction = 1
            if event.type == KEYUP:
                if event.key == K_UP and player_paddle.direction == -1:
                    player_paddle.direction = 0
                elif event.key == K_DOWN and player_paddle.direction == 1:
                    player_paddle.direction = 0

        #object updating phase
        ai_paddle_0.update(pong)
        ai_paddle_1.update(pong)
        ai_paddle_2.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle_0,ai_paddle_1,ai_paddle_2)
       

        #CODE TASK: make some text on the screen over everything else saying you lost/won, and then exit on keypress
        #CODE BONUS: allow restarting of the game (hint: you can recreate the Pong/Paddle objects the same way we made them initially)
        if pong.hit_edge_left:
            print 'You Won'
            #running = False
        elif pong.hit_edge_right:
            print 'You Lose'
            #running = False

        #rendering phase
        screen.fill((100,200,100))

        ai_paddle_0.render(screen)
        ai_paddle_1.render(screen)
        ai_paddle_2.render(screen)
        player_paddle.render(screen)
        pong.render(screen)

        pygame.display.flip()

    pygame.quit()


main()
