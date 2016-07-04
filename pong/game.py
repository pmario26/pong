import pygame
from pygame.locals import *
import random,math
import time
#import menu

Balls = [] # Lista de Bolas no jogo
class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize

        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)

        self.radius = 8

        self.colidiu = False

        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)

        #self.color = (100,100,255)
        self.color = (random.randrange(0,255,5),random.randrange(0,255,5),random.randrange(0,255,5))

        #Define Randomicamente qual direcao a bola vai sair
        self.direction = [random.randrange(-1,2,2), random.randrange(-1,2,2)]
        self.speedx = 2 
        self.speedy = 2 
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

        
        #Checar se colidiu com a parede
        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True
        elif self.rect.top <= 0:
            self.hit_edge_top = True
        elif self.rect.bottom >= self.screensize[1]-1:
            self.hit_edge_bot = True

        #CODE TASK: Change the direction of the pong, based on where it hits the paddles (HINT: check the center points of each)
        #Colisao da bola com os paddles
        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1            
            self.speedx *= 1.05
            self.speedy *= 1.05
        if self.rect.colliderect(ai_paddle_0.rect):
            self.direction[0] = 1
            self.speedx *= 1.05
            self.speedy *= 1.05
        if self.rect.colliderect(ai_paddle_1.rect):
            self.direction[1] = 1
            self.speedx *= 1.05
            self.speedy *= 1.05
        if self.rect.colliderect(ai_paddle_2.rect):
            self.direction[1] = -1
            self.speedx *= 1.05
            self.speedy *= 1.05
            
        #Colisao da bola com os cantos      
        if pygame.sprite.collide_circle(self, corner_BL):
            if self.direction[0] > 0:
                self.direction[0] *= 1.2
                self.direction[1] *= 1
            else:
                self.direction[0] *= -1.25
                self.direction[1] *= -1               
        
        if pygame.sprite.collide_circle(self, corner_BR):
            if self.direction[0] < 0:
                self.direction[0] *= 1.25
                self.direction[1] *= 1.25
            else:
                self.direction[0] *= -1.25
                self.direction[1] *= -1
    
        if pygame.sprite.collide_circle(self, corner_UL):
            if self.direction[0] > 0:
                self.direction[0] *= 1.25
                self.direction[1] *= 1
            else:
                self.direction[0] *= -1.2
                self.direction[1] *= -1
                    
        if pygame.sprite.collide_circle(self, corner_UR):
            if self.direction[0] < 0:
                self.direction[0] *= 1.25
                self.direction[1] *= 1.25
            else:
                self.direction[0] *= -1.25
                self.direction[1] *= -1    
               
                
    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)

#Funcao pra verificar o sinal de um numero
def sign(x): return 1 if x >= 0 else -1

def ColisionBalls(B1, B2):
    
    if sign(B1.direction[0]) == sign(B2.direction[0]) and sign(B1.direction[1]) != sign(B2.direction[1]):
        B1.direction[1] *= -1
        B2.direction[1] *= -1
    elif sign(B1.direction[1]) == sign(B2.direction[1]) and sign(B1.direction[0]) != sign(B2.direction[0]):
        B1.direction[0] *= -1
        B2.direction[0] *= -1
    elif sign(B1.direction[1]) != sign(B2.direction[1]) and sign(B1.direction[0]) != sign(B2.direction[0]):
        B1.direction[0] *= -1
        B1.direction[1] *= -1
        B2.direction[0] *= -1
        B2.direction[1] *= -1
    elif sign(B1.direction[1]) == sign(B2.direction[1]) and sign(B1.direction[0]) == sign(B2.direction[0]):
        auxSX = B1.speedx
        auxSY = B1.speedy
        B1.speedx = B2.speedx
        B1.speedy = B2.speedy
        B2.speedx = auxSX
        B2.speedy = auxSY

#Detectar Colisao dos Pongs    
def ColisionDetect():
    for B1 in Balls:
        for B2 in Balls:
            if B1 != B2:
                if B1.colidiu == False and B2.colidiu == False:
                    if pygame.sprite.collide_circle(B1, B2):
                        #print("Colidiu!")
                        B1.colidiu = True
                        B2.colidiu = True                        
                        ColisionBalls(B1, B2)
    
    for Ball in Balls:
        Ball.colidiu = False
                    
    

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

        self.speed = 5

    def update(self, Balls, corner_UL, corner_BL):
        for Ball in Balls:
            if Ball.rect.x < 150:
                
                if Ball.rect.top < self.rect.top:
                    self.centery -= self.speed
                elif Ball.rect.bottom > self.rect.bottom:
                    self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)
        #Checar colisao com os cantos
        if self.rect.colliderect(corner_UL):
            self.rect.top = corner_UL.radius 
            self.centery += self.speed
        elif self.rect.colliderect(corner_BL):
            self.rect.bottom = self.screensize[1] - corner_BL.radius    
            self.centery -= self.speed
        
        #ajustar a posicao
        self.rect.center = (self.centerx, self.centery)              

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)
    
    def lose(self, screen, i):
        pygame.draw.rect(screen, (0,0,0), (0, self.centery-int(self.height*0.5), self.width, i), 0)
    
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

        self.speed = 5

    def update(self, Balls, corner_R, corner_L):
        #TESTE
        #Checar se e o paddle de cima ou de baixo
        if self.rect.y < 100:
            for Ball in Balls:
                if Ball.rect.y < 150:        
                    if Ball.rect.left < self.rect.left:
                        self.centerx -= self.speed
                    elif Ball.rect.right > self.rect.right:
                        self.centerx += self.speed

        if self.rect.y > 100:
            for Ball in Balls:
                if Ball.rect.y > 350:        
                    if Ball.rect.left < self.rect.left:
                        self.centerx -= self.speed
                    elif Ball.rect.right > self.rect.right:
                        self.centerx += self.speed        
        #------------------------------------
        self.rect.center = (self.centerx, self.centery)
        #Checar colisao com os cantos
        if self.rect.colliderect(corner_R):
            self.rect.right = corner_R.radius 
            self.centerx += self.speed
        elif self.rect.colliderect(corner_L):
            self.rect.left = self.screensize[0] - corner_L.radius    
            self.centerx -= self.speed
        
        #ajustar a posicao
        self.rect.center = (self.centerx, self.centery)              
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)
    
    def lose(self, screen, i):
        pygame.draw.rect(screen, (0,0,0), (self.centerx-int(self.width*0.5), self.centery-5, i, self.height), 0)
        

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
        
        #Checar colisao com os corners
        if self.rect.colliderect(corner_UR):
            self.rect.top = corner_UR.radius
            self.direction = 0
        elif self.rect.colliderect(corner_BR):
            self.rect.bottom = self.screensize[1] - corner_BR.radius         
            self.direction = 0
            
    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)
    
    def lose(self, screen, i):
        pygame.draw.rect(screen, (0,0,0), (self.centerx-5, self.centery-int(self.height*0.5), self.width, i), 0)


def main():
    pygame.init()

    screensize = (480,480)
    
    screen = pygame.display.set_mode(screensize)
    pygame.mixer.music.stop()
    
    clock = pygame.time.Clock()
    
    fim = False #Termino do jogo
    vitoria = False
    #Fonte
    myfont = pygame.font.SysFont("comicsansms",50)
    
    venceu = myfont.render("VENCEU!", 1, (0,0,255))
    perdeu = myfont.render("PERDEU!", 1, (255,0,0))
    
    #pong = Pong(screensize)
    Balls.append(Pong(screensize))
    pygame.mixer.music.load('sons\gaming.mp3')            
    ai_paddle_0 = AIPaddle_vert(screensize)
    ai_paddle_1 = AIPaddle_hor(screensize,1)
    ai_paddle_2 = AIPaddle_hor(screensize,0)
    player_paddle = PlayerPaddle(screensize)
    
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
    cornerBR = Corner(screensize, 480, 480)
    cornerUL = Corner(screensize, 0, 0)
    cornerUR = Corner(screensize, 480, 0) 
    scored = pygame.mixer.Sound('sons\scored.wav')
    pygame.mixer.music.play(-1)
    SP = 0
    SA0 = 0
    SA1 = 0
    SA2 = 0
    #Tempo em Milisegundos para aparecer uma nova bola
    timer = 5 #a cada 5 segundos
    startTime = time.time()
    
    while running:
        #fps limiting/reporting phase
        clock.tick(60)

        #Teste         
        currentTime = time.time()
        actualTime = currentTime - startTime
        #print(actualTime / timer)
        if (actualTime / timer > 1):
            Balls.append(Pong(screensize))
            timer += 5
        #---------------    
        
        
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
        if score_ai_0 > 0:
            ai_paddle_0.update(Balls,cornerUL, cornerBL)
        if score_ai_1 > 0:
            ai_paddle_1.update(Balls,cornerUL, cornerUR)
        if score_ai_2 > 0:
            ai_paddle_2.update(Balls,cornerBL, cornerBR)
        if score_player > 0:
            player_paddle.update(cornerUR, cornerBR)
        #Teste        
        for Ball in Balls:
            Ball.update(player_paddle, ai_paddle_0,ai_paddle_1,ai_paddle_2,cornerBL, cornerBR, cornerUL, cornerUR)
        
        

        #CODE TASK: make some text on the screen over everything else saying you lost/won, and then exit on keypress
        #CODE BONUS: allow restarting of the game (hint: you can recreate the Pong/Paddle objects the same way we made them initially)
        
        #TESTE
        for Ball in Balls:
            if Ball.hit_edge_left:
                #print 'You Won'
                if score_ai_0 <= 0:
                    Ball.direction[0] = 1
                    Ball.hit_edge_left = False
                else:
                    score_ai_0 -= 1
                    #------------
                    SA0 += 10
                    #-------------
                    Balls.remove(Ball)
                    #Balls.append(Pong(screensize))
                    label_0 = myfont.render(str(score_ai_0),1,(255,255,255))
                    scored.play()
            elif Ball.hit_edge_top :
                #print 'You Won'
                if score_ai_1 <= 0:
                    Ball.direction[1] = 1
                    Ball.hit_edge_top = False
                else:
                    score_ai_1 -= 1
                    #------------
                    SA1 += 10
                    #ai_paddle_1.lose(screen, SA1)
                    #----------
                    Balls.remove(Ball)
                    #Balls.append(Pong(screensize))
                    label_1 = myfont.render(str(score_ai_1),1,(255,255,255))
                    scored.play()
            elif  Ball.hit_edge_bot :
               # print 'You Won'
                if score_ai_2 <= 0:
                    Ball.direction[1] = -1
                    Ball.hit_edge_bot = False
                else:
                    score_ai_2 -= 1
                    #----------
                    SA2 += 10
                    #ai_paddle_2.lose(screen, SA2)
                    #-----------
                    Balls.remove(Ball)
                    #Balls.append(Pong(screensize))
                    label_2 = myfont.render(str(score_ai_2),1,(255,255,255))
                    scored.play()
            elif Ball.hit_edge_right:
                #print 'You Lose'
                if score_player <= 0:
                    Ball.direction[0] *= -1
                    Ball.hit_edge_right = False
                else:    
                    score_player -= 1
                    #TESTE
                    SP += 10
                    player_paddle.lose(screen, SP)
                    #------------------------------------------------------
                    Balls.remove(Ball)
                    #Balls.append(Pong(screensize))
                    label_player = myfont.render(str(score_player),1,(255,255,255))
                    scored.play()
                        
        #Colisao entre os pongs
        ColisionDetect()
                
                
        #rendering phase
        screen.fill((100,200,100))
             
        for Ball in Balls:
            Ball.render(screen)
            
        if score_ai_0 > 0:
            ai_paddle_0.render(screen)
            ai_paddle_0.lose(screen, SA0)
        if score_ai_1 > 0:
            ai_paddle_1.render(screen)
            ai_paddle_1.lose(screen, SA1)
        if score_ai_2 > 0:
            ai_paddle_2.render(screen)
            ai_paddle_2.lose(screen, SA2)
        if score_player > 0:
            player_paddle.render(screen)
            player_paddle.lose(screen, SP)
        #pong.render(screen)
        cornerBL.render(screen, 0, 480)
        cornerBR.render(screen, 480, 480)
        cornerUL.render(screen, 0, 0)
        cornerUR.render(screen, 480, 0)        
        #screen.blit(label_player, (425, 415)) #585
        #screen.blit(label_2, (0,415))
        #screen.blit(label_0, (0,-10))
        #screen.blit(label_1, (425,-10))
        
        #Venceu ou perdeu
        if SP == 100: 
            fim = True
        if SA0 == 100 and SA1 == 100 and SA2 == 100:
            vitoria = True
            fim = True
        
        while fim:
            running = False
            pygame.display.update()
            if vitoria == True:
                screen.blit(venceu, (150, 200))
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.type == QUIT:
                            fim = False               
            else:
                screen.blit(perdeu, (150, 200))
                   
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE or event.type == QUIT:
                            fim = False
                                 
              
        pygame.display.flip()
        
    pygame.quit()

#main()