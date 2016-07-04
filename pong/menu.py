import pygame
from pygame.locals import *
import game

def run():
	pygame.init()
	
	clock = pygame.time.Clock()

	screensize = (480, 480)

	bg = pygame.image.load("imagens\Franco_BG.png")
	
	pygame.mixer.music.load('sons\Kombat.wav')
	
	startMusic = pygame.mixer.Sound('sons\horadoshow.wav')
	
	screen = pygame.display.set_mode(screensize)

	myfont = pygame.font.SysFont("comicsansms",50) 
	
	titulo = myfont.render("Pong Mutante", 1, (0,0,255))
	start = myfont.render("Start", 1, (0,255,0))
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
		
		#Apertar botao Start
		if 75+180 > mouse[0] > 75 and 165+50 > mouse[1] > 165:
			pygame.draw.rect(screen, (0,200, 0), (75, 165, 180, 50), 10)
			if click[0] == 1:
				startMusic.play()
				game.main()			
		else:
			pygame.draw.rect(screen, (0,200, 0), (75, 165, 180, 50), 1)
		
		#Apertar Botao Sair
		if 75+180 > mouse[0] > 75 and 315+50 > mouse[1] > 315:
			pygame.draw.rect(screen, (200, 0, 0), (75, 315, 180, 50), 10)
			if click[0] == 1:
				menu = False
		else:
			pygame.draw.rect(screen, (200, 0, 0), (75, 315, 180, 50), 1)
			
		screen.blit(titulo, (100, 20))
		screen.blit(start, (100, 150))
		screen.blit(quit, (100, 300))
		
		pygame.display.update()
		
	pygame.quit()
	
run()
