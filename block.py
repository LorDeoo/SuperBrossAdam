import pygame
from body import Body
import time
from mob import Mob
from vector import vecteur

#initialisation des variables nécessaires au block
class Block(pygame.sprite.Sprite):
    def __init__(self, pos, name):
        super().__init__()
        self.name = name
        self.time = time.time()
        self.setup(pos)

    #Chargement de l'image du block et création de son corp
    def setup(self, pos):
        if(self.name == "mur"):
            self.image = pygame.image.load("image/Blocs/mur.png")
        elif(self.name == "mur2"):
            self.image = pygame.image.load("image/Blocs/mur.png")
        elif self.name == "herbe":
            self.image = pygame.image.load("image/Blocs/herbe.png")
        elif self.name == "sol":
            self.image = pygame.image.load("image/Blocs/sol.png")
        elif self.name == "demi":
            self.image = pygame.image.load("image/Blocs/demibloc.png")
        elif self.name == "ascenseur":
            self.image = pygame.image.load("image/Blocs/ascenseur.png")
        elif self.name == "horizontal":
            self.image = pygame.image.load("image/Blocs/horizontal.png")
        elif self.name == "trampo":
            self.image = pygame.image.load("image/Blocs/trampoline.png")
        elif self.name == "drapeau":
            self.image = pygame.image.load("image/Blocs/drapeau.png")
        elif self.name == "canon2":
            self.image = pygame.image.load("image/Blocs/canon2.png")
            self.munitions = pygame.sprite.Group()
            
        self.rect = self.image.get_rect(topright = pos)
        if self.name == "ascenseur":
            self.departy = self.rect.y
            self.speed = 1
        elif self.name == "horizontal":
            self.departx = self.rect.x
            self.speed = 1
        self.body = Body(1, self.rect.x, self.rect.y, 50 , 50)
        if self.name == "mur2":
            self.rect.x = self.rect.x - 398
            self.rect.y = self.rect.y - 50

    #Gère la caméra des blocks et update les blocks avec des capacités
    def update(self, x_shift, cam_affichage, blocks,  position, velocity, surface, adam):
        self.rect.x += x_shift
        if self.name =="canon2":
            self.shoot(x_shift, cam_affichage, blocks,  position, velocity, surface, adam)
        elif self.name =="ascenseur":
            self.move(position, velocity, cam_affichage)
        elif self.name =="horizontal":
            self.move(position, velocity, cam_affichage)

    #Permet de gérer la création des boulets de canon et leur update
    def shoot(self, x_shift, cam_affichage, blocks,  position, velocity, surface, adam):
        player = adam.sprite
        
        if time.time() + 2 > self.time and self.body.position.x - player.body.position.x < 600 and self.body.position.x - player.body.position.x > -600:
            mob = Mob("canon", (self.body.position.x , self.body.position.y))
            self.munitions.add(mob)
            self.time = time.time() + 8

        self.munitions.update( x_shift, cam_affichage, blocks,  position, velocity, adam, surface)
        self.Collision_mob(adam)
        self.munitions.draw(surface)

    #Collision entre les boulets de canon et le joueur
    def Collision_mob(self, adam):
        player = adam.sprite
        for sprite in self.munitions.sprites():
            if player.body.droite1.x >= sprite.body.gauche1.x + 5 and player.body.gauche1.x <= sprite.body.droite1.x - 5  and player.body.bas1.y - 10 >= sprite.body.haut1.y  and player.body.haut1.y + 15 <= sprite.body.bas1.y and time.time() > player.invincibilite:
                player.pdv -= 1
                player.invincibilite = time.time() + 1
                print("joueur:", player.pdv)

            if sprite.body.position.x < 100:
                sprite.kill() 
                del sprite

    #Actualisation de blocks ascenseur horizontal et vertical et de leur corp
    def move(self, position, velocity, cam_affichage):
        if self.name == "ascenseur":
            if self.body.position.y < self.departy - 100:
                self.speed = 1
            elif self.body.position.y > self.departy + 100:
                self.speed = -1

            self.body.position.y += self.speed

        elif self.name == "horizontal":
            if self.body.position.x < self.departx - 100:
                self.speed = 1
            elif self.body.position.x > self.departx + 100:
                self.speed = -1
                

            self.body.position.x += self.speed


        self.body.haut1 = self.body.position
        self.body.haut2 = vecteur(self.body.position.x - self.body.largeur, self.body.position.y)
     
        self.body.droite1 = self.body.position
        self.body.droite2 = vecteur(self.body.position.x , self.body.position.y + self.body.longueur)

        self.body.gauche1 = vecteur(self.body.position.x - self.body.largeur, self.body.position.y)
        self.body.gauche2 = vecteur(self.body.position.x - self.body.largeur , self.body.position.y + self.body.longueur)
     
        self.body.bas1 = vecteur(self.body.position.x , self.body.position.y + self.body.longueur)
        self.body.bas2 = vecteur(self.body.position.x - self.body.largeur , self.body.position.y + self.body.longueur)
        if self.name == "ascenseur":
            self.rect.y = int(self.body.position.y)
        elif self.name == "horizontal":
            self.rect.x = int(self.body.position.x)
            if position > 600 and velocity > 0:
                cam_affichage -= self.speed
                self.rect.x += cam_affichage

            elif position > 600 and velocity < 0:
                cam_affichage -= self.speed
                self.rect.x += cam_affichage
            else:
                self.rect.x += cam_affichage
