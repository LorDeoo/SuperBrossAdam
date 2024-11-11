import pygame
import math, sys

class Menu():
    #définition des images nécessaires au menu et aux niveaux
    def __init__(self):

        self.screen_width = 1320
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #Menu
        self.background_menu = pygame.image.load("image/Backgrounds/BGAdamPret.png")
        self.background_menu = pygame.transform.scale(self.background_menu, (self.screen_width, self.screen_height))

        #definition du bouton de niveau 1
        self.niveau1 = pygame.image.load("image/Level/niveau1.jpg")
        self.niveau1_rect = self.niveau1.get_rect()
        self.niveau1_rect.x =  50
        self.niveau1_rect.y = 350

        #definition du bouton de niveau 1
        self.niveau2 = pygame.image.load("image/Level/niveau2lock.jpg")
        self.niveau2_rect = self.niveau2.get_rect()
        self.niveau2_rect.x =  250
        self.niveau2_rect.y = 350

        self.niveau3 = pygame.image.load("image/Level/niveau3lock.jpg")
        self.niveau3_rect = self.niveau3.get_rect()
        self.niveau3_rect.x =  950
        self.niveau3_rect.y = 350

        self.niveau4 = pygame.image.load("image/Level/niveau4lock.jpg")
        self.niveau4_rect = self.niveau4.get_rect()
        self.niveau4_rect.x =  1150
        self.niveau4_rect.y = 350


    #Fonction permettant de gérer le choix de niveau du joueur et d'afficher les niveaux bloqué ou non
    def ChoixNiveau(self, acces):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Super BrossAdam")
        if acces == 2:
            self.niveau2 = pygame.image.load("image/Level/niveau2.jpg")
        elif acces == 3:
            self.niveau3 = pygame.image.load("image/Level/niveau3.jpg")
        elif acces == 4:
            self.niveau4 = pygame.image.load("image/Level/niveau4.jpg")
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.niveau1_rect.collidepoint(event.pos):
                        run = False
                        return 1
                    elif self.niveau2_rect.collidepoint(event.pos) and acces > 1:
                        run = False
                        return 2
                    elif self.niveau3_rect.collidepoint(event.pos) and acces > 2:
                        run = False
                        return 3
                    elif self.niveau4_rect.collidepoint(event.pos) and acces > 3:
                        run = False
                        return 4
            self.screen.blit(self.background_menu, (0, 0))
            self.screen.blit(self.niveau1, self.niveau1_rect)
            self.screen.blit(self.niveau2, self.niveau2_rect)
            self.screen.blit(self.niveau3, self.niveau3_rect)
            self.screen.blit(self.niveau4, self.niveau4_rect)
            pygame.display.flip()