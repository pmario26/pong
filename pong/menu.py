import pygame
from pygame.locals import *
import game

# executar esse script

def run():
	pygame.init()
	
	clock = pygame.time.Clock()

	screensize = (480, 480)

	bg = pygame.image.load("imagens\menu.jpg")
	
	pygame.mixer.music.load('sons\Kombat.wav')
	
	startMusic = pygame.mixer.Sound('sons\horadoshow.wav')
	
	screen = pygame.display.set_mode(screensize)

	myfont = pygame.font.Font('fontetitulo.ttf',40) 
	
	titulo = myfont.render("Pong Mutante", 1, (255,255,255))
	normal = myfont.render("Normal", 1, (0,255,0))
	monstro = myfont.render("Monstro", 1, (0,255,0))
	quit = myfont.render("Exit", 1, (255,0,0))

	menu = True
	pygame.mixer.music.play(-1)
	while menu:
		
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				menu = False 		

		screen.fill((100,100,100))
		screen.blit(bg, (0,0))
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()
		
		#Apertar botao Normal
		if 130+220 > mouse[0] > 130 and 185+50 > mouse[1] > 185:
			pygame.draw.rect(screen, (0,200, 0), (130, 185, 220, 50), 10)
			if click[0] == 1:
				startMusic.play()
				game.main(2)			
		else:
			pygame.draw.rect(screen, (0,200, 0), (130, 185, 220, 50), 1)
		#Apertar o botão monstro
		if 130+220 > mouse[0] > 130 and 245+50 > mouse[1] > 245:
			pygame.draw.rect(screen, (0,200, 0), (130, 245, 220, 50), 10)
			if click[0] == 1:
				startMusic.play()
				game.main(1)			
		else:
			pygame.draw.rect(screen, (0,200, 0), (130, 245, 220, 50), 1)		
		
		#Apertar Botao Sair
		if 130+180 > mouse[0] > 130 and 315+50 > mouse[1] > 315:
			pygame.draw.rect(screen, (200, 0, 0), (130, 315, 220, 50), 10)
			if click[0] == 1:
				menu = False
		else:
			pygame.draw.rect(screen, (200, 0, 0), (130, 315, 220, 50), 1)
			
		screen.blit(titulo, (75, 70))
		screen.blit(normal, (150, 185))
		screen.blit(monstro,(132,245))
		screen.blit(quit, (190, 315))
		
		pygame.display.update()
		
	pygame.quit()
	
run()
