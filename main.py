import pygame, sys
from map import *
from menu import Menu
from game import game     

#Création du menu pour gérer le choix des niveaux
menu = Menu()

#initialisation de variables nécessaires
acces = 1
reusltat = 1

choix = menu.ChoixNiveau(acces)
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
background = pygame.image.load("image/Backgrounds/bg.jpg")
background2 = pygame.image.load("image/Backgrounds/bg3.jpg")
background3 = pygame.image.load("image/Backgrounds/bg2.jpg")
background4 = pygame.image.load("image/Backgrounds/bg4.jpg")

#Création du niveau
Game = game(level_map, screen, choix, background)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
    #Vérification si le joueur est mort ou à finis le niveau pour passer au suivant
    test, resultat = Game.run()
    if test == 2 or test == 0:
        if test == 0:
            if resultat == 1 and acces == 1:
                acces +=1
            elif resultat == 2 and acces == 2:
                acces += 1
            elif resultat == 3 and acces == 3:
                acces += 1
            else:
                pass
        acces = 3
        choix = menu.ChoixNiveau(acces)
        if choix == 1:
            Game = game(level_map, screen, choix, background)
        elif choix == 2:
            Game = game(level_map2, screen, choix, background2)
        elif choix == 3:
            Game = game(level_map3, screen, choix, background3)
        elif choix == 4:
            Game = game(level_map4, screen, choix, background4)

        screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.flip()
    clock.tick(60)