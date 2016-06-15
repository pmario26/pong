import pygame
from pygame.locals import *
import random,math

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
        

        
        self.direction = [random.randrange(-1,2,2), random.randrange(-1,2,2)]
        self.speedx = 2
        self.speedy = 5
        #CODE TASK: change speed/radius as game progresses to make it harder
        #CODE BONUS: adjust ratio of x and y speeds to make it harder as game progresses

        self.hit_edge_left = False
        self.hit_edge_right = False
        self.hit_edge_top = False
        self.hit_edge_bot = False
    def update(self, player_paddle, ai_paddle_0,ai_paddle_1,ai_paddle_2, corner_BL, corner_BR, corner_UL, corner_UR ):

        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True
        elif self.rect.top <= 0:
            self.hit_edge_top = True
        elif self.rect.bottom >= self.screensize[1]-1:
            self.hit_edge_bot = True

        #CODE TASK: Change the direction of the pong, based on where it hits the paddles (HINT: check the center points of each)

        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] *= -1            
        if self.rect.colliderect(ai_paddle_0.rect):
            self.direction[0] *= -1
        if self.rect.colliderect(ai_paddle_1.rect):
            self.direction[1] *= -1
        if self.rect.colliderect(ai_paddle_2.rect):
            self.direction[1] *= -1        
        #Colisão da bola com os cantos      
        if pygame.sprite.collide_circle(self, corner_BL):
            if self.direction[0] > 0:
                self.direction[0] *= 1.1
                self.direction[1] *= 1
            else:
                self.direction[0] *= -1.1
                self.direction[1] *= -1                
        
        if pygame.sprite.collide_circle(self, corner_BR):
            if self.direction[0] < 0:
                self.direction[0] *= 1.1
                self.direction[1] *= 1.1
            else:
                self.direction[0] *= -1.1
                self.direction[1] *= -1
    
        if pygame.sprite.collide_circle(self, corner_UL):
            if self.direction[0] > 0:
                self.direction[0] *= 1.1
                self.direction[1] *= 1
            else:
                self.direction[0] *= -1.1
                self.direction[1] *= -1
                    
        if pygame.sprite.collide_circle(self, corner_UR):
            if self.direction[0] < 0:
                self.direction[0] *= 1.1
                self.direction[1] *= 1.1
            else:
                self.direction[0] *= -1.1
                self.direction[1] *= -1
            
         
    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)

#Os circulos dos cantos
class Corner(object):
    def __init__(self, screensize, posx, posy):
        
        self.screensize = screensize
        
        self.posx = posx
        self.posy = posy 
        
        
        self.radius = 50
        
        self.rect = pygame.Rect(posx - self.radius, posy - self.radius, 2*self.radius, 2*self.radius)        
        
        self.color = (0,255,0)
            
    def render(self, screen, posx, posy):
        
        #pygame.draw.circle(screen, (0,0,0), (posx, posy),75, 1)        
        pygame.draw.circle(screen, self.color, (posx, posy), self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), (posx, posy), self.radius, 1) 
        #pygame.draw.rect(screen, (0,0,0), self.rect, 0)

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

    def update(self, pong, corner_UL, corner_BL):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)
        #Checar colisão com os cantos
        if self.rect.colliderect(corner_UL):
            self.rect.top = corner_UL.radius 
            self.centery += self.speed
        elif self.rect.colliderect(corner_BL):
            self.rect.bottom = self.screensize[1] - corner_BL.radius    
            self.centery -= self.speed
        
        #ajustar a posição
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

    def update(self, pong, corner_R, corner_L):
        if pong.rect.left < self.rect.left:
            self.centerx -= self.speed
        elif pong.rect.right > self.rect.right:
            self.centerx += self.speed

        self.rect.center = (self.centerx, self.centery)
        #Checar colisão com os cantos
        if self.rect.colliderect(corner_R):
            self.rect.right = corner_R.radius 
            self.centerx += self.speed
        elif self.rect.colliderect(corner_L):
            self.rect.left = self.screensize[0] - corner_L.radius    
            self.centerx -= self.speed
        
        #ajustar a posição
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

    def update(self, corner_UR, corner_BR):
        self.centery += self.direction*self.speed

        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1
            #Checar colisão com os cantos
        if self.rect.colliderect(corner_UR):
            self.rect.top = corner_UR.radius
            self.direction = 0
        elif self.rect.colliderect(corner_BR):
            self.rect.bottom = self.screensize[1] - corner_BR.radius         
            self.direction = 0
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
    myfont = pygame.font.SysFont("comicsansms",50)
    score_ai_0  =  10
    score_player = 10
    score_ai_1  =  10
    score_ai_2  =  10
    label_0 = myfont.render(str(score_ai_0),1,(255,255,255)) 
    label_1 = myfont.render(str(score_ai_1),1,(255,255,255))
    label_2 = myfont.render(str(score_ai_2),1,(255,255,255))
    label_player = myfont.render(str(score_player),1,(255,255,255))
    running = True
    cornerBL = Corner(screensize, 0, 480)
    cornerBR = Corner(screensize, 640, 480)
    cornerUL = Corner(screensize, 0, 0)
    cornerUR = Corner(screensize, 640, 0)    

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
        ai_paddle_0.update(pong,cornerUL, cornerBL)
        ai_paddle_1.update(pong,cornerUL, cornerUR)
        ai_paddle_2.update(pong,cornerBL, cornerBR)
        player_paddle.update(cornerUR, cornerBR)
        pong.update(player_paddle, ai_paddle_0,ai_paddle_1,ai_paddle_2,cornerBL, cornerBR, cornerUL, cornerUR)
       

        #CODE TASK: make some text on the screen over everything else saying you lost/won, and then exit on keypress
        #CODE BONUS: allow restarting of the game (hint: you can recreate the Pong/Paddle objects the same way we made them initially)
        if pong.hit_edge_left:
            print 'You Won'
            score_ai_0 -= 1
            pong = Pong(screensize)
            label_0 = myfont.render(str(score_ai_0),1,(255,255,255))
        elif pong.hit_edge_top :
            print 'You Won'
            score_ai_1 -= 1
            pong = Pong(screensize)
            label_1 = myfont.render(str(score_ai_1),1,(255,255,255))
        elif  pong.hit_edge_bot :
            print 'You Won'
            score_ai_2 -= 1
            pong = Pong(screensize)  
            label_2 = myfont.render(str(score_ai_2),1,(255,255,255))
        elif pong.hit_edge_right:
            print 'You Lose'
            score_player -= 1
            pong = Pong(screensize)
            label_player = myfont.render(str(score_player),1,(255,255,255))

        #rendering phase
        screen.fill((100,200,100))

        ai_paddle_0.render(screen)
        ai_paddle_1.render(screen)
        ai_paddle_2.render(screen)
        player_paddle.render(screen)
        pong.render(screen)
        cornerBL.render(screen, 0, 480)
        cornerBR.render(screen, 640, 480)
        cornerUL.render(screen, 0, 0)
        cornerUR.render(screen, 640, 0)        
        screen.blit(label_player, (585, 415))
        screen.blit(label_0, (0,415))
        screen.blit(label_1, (0,-10))
        screen.blit(label_2, (585,-10))
        pygame.display.flip()

    pygame.quit()


main()
