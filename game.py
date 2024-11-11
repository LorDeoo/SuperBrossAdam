import pygame
from block import Block
from map import *
from adam import Player
from mob import Mob
import time

#La classe game gère toutes les variables nécessaires au fonctionnement du niveau
class game():
    #Initiation de variables nécessaires
    def __init__(self,level_data, screen, id, background):
        self.bg = background
        self.id = id
        if self.id == 4:
            self.detruire = 0
        self.verif = 0
        self.surface = screen
        self.setup_level(level_data)
        self.cam_affichage = 0
        self.fin = 0

    """
    Création des variables du joueur et des blocks et mobs de la map ainsi
    que leurs sprites associés.
    La map est créée dans le fichier map.py, une boucle lit chaque caractère et 
    créée chaque block ou mob associé
    """
    def setup_level(self, layout):
        pygame.mixer.init()
        self.camera = 0
        self.seconde = 0
        self.delai = 0
        self.blocks = pygame.sprite.Group()
        self.adam = pygame.sprite.GroupSingle()
        self.mobs = pygame.sprite.Group()
        joueur = Player((150, 300))
        self.adam.add(joueur)
        self.collide = 0
        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * block_size
                y = row_index * block_size
                if cell == 'X': 
                    block = Block((x, y),"mur")
                    self.blocks.add(block)
                elif cell == "G":
                    block = Block((x, y),"herbe")
                    self.blocks.add(block)
                elif cell == "A":
                    block = Block((x, y),"ascenseur")
                    self.blocks.add(block)
                elif cell == "H":
                    block = Block((x, y),"horizontal")
                    self.blocks.add(block)
                elif cell == "R":
                    block = Block((x, y),"demi")
                    self.blocks.add(block)
                elif cell == "S":
                    block = Block((x, y),"sol")
                    self.blocks.add(block)
                elif cell == "T":
                    block = Block((x, y),"trampo")
                    self.blocks.add(block)
                elif cell == "D":
                    block = Block((x, y),"drapeau")
                    self.blocks.add(block)
                elif cell == 'O':
                    mob = Mob("mob1", (x, y))
                    self.mobs.add(mob)
                elif cell == 'P':
                    mob = Mob("mob2", (x, y))
                    self.mobs.add(mob)
                elif cell == 'B':
                    mob = Mob("boss", (x, y))
                    self.mobs.add(mob)
                elif cell == 'C':
                    block = Block((x, y + 10),"canon2")
                    self.blocks.add(block)

    #Fonction principale actualisant tout le jeux
    def run(self):
        self.surface.blit(self.bg ,(0, -200))
        player = self.adam.sprite
        valeur = self.adam.update()

        if self.id == 4 and player.body.position.x > 1000 and self.verif == 0:
            block = Block((900, 450),"mur2")
            self.blocks.add(block)
            block = Block((900, 500),"mur2")
            self.blocks.add(block)
            block = Block((950, 450),"mur2")
            self.blocks.add(block)
            block = Block((950, 500),"mur2")
            self.blocks.add(block)
            self.verif = 1


        if valeur == 1:
            player.pdv = 0
        self.Collision()
        self.blocks.update(self.camera, self.cam_affichage, self.blocks, player.body.position.x, player.body.velocity.x, self.surface, self.adam)
        self.mobs.update(self.camera, self.cam_affichage, self.blocks, player.body.position.x, player.body.velocity.x, self.adam, self.surface)
        self.Camera()
        player.Draw_Player(self.surface)
        self.blocks.draw(self.surface)
        self.mobs.draw(self.surface)
        player.update_health_bar(self.surface)
        if player.pdv <= 0: 
            return 2, self.id

        elif self.fin == 1:
            return 0, self.id
        else:
            return 1, self.id

    """
    Permet de gérer la caméra du joueur en fonction de ce qu'il fait:
    lorsque le x du joueur est < 600 elle ne bouge pas, sinon elle bouge
    cependant seuls le rect du joueur pas sa position. Nous avons donc 2 
    variables distinctes qui sont le rect et la position pour éviter tout
    problèmes de position dans l'espace.
    Cette fonction adapte donc la caméra en fonctio nde ce que fait le joueur 
    (droite ou gauche)
    """
    def Camera(self):
        adam = self.adam.sprite
        if adam.body.position.x > 600 and adam.body.velocity.x > 0:
            self.camera = -3
            self.cam_affichage -= adam.body.velocity.x
            adam.rect.x += self.cam_affichage
        elif adam.body.position.x > 600 and adam.body.velocity.x < 0:
            self.camera = 3 
            self.cam_affichage -= adam.body.velocity.x
            adam.rect.x += self.cam_affichage
        else:
            adam.rect.x += self.cam_affichage
            self.camera= 0
        
    """
    Fonction faisant les collisions entre le joueur et les blocks de la map
    Comme nous avons un moteur physique propre au jeu, les collisions sont faites
    avec des grosses conditions car il fallait discerner la position et le rect, problème
    non résolu avec la fonction déjà faites de pygame
    """
    def Collision(self):
        self.Collision_mob()
        player = self.adam.sprite

        compteur = 0
        compteur2 = 0
        for sprite in self.blocks.sprites():
            compteur2 += 1
            if sprite.name == "mur" or sprite.name == "sol" or sprite.name == "ascenseur" or sprite.name == "horizontal" or sprite.name == "mur2":
                if (player.body.bas2.x >= sprite.body.haut2.x and player.body.bas2.x <= sprite.body.haut1.x or player.body.bas1.x >= sprite.body.haut2.x and player.body.bas1.x <= sprite.body.haut1.x) and player.body.velocity.y >= 0 and player.body.bas1.y > sprite.body.haut1.y - 10 and player.body.bas1.y <= sprite.body.haut1.y + 3 :
                    player.body.position.y = sprite.body.haut1.y - 100
                    player.body.velocity.y = 0   
                    player.CanJump = True

                if (player.body.bas2.x >= sprite.body.haut2.x and player.body.bas2.x <= sprite.body.haut1.x or player.body.bas1.x >= sprite.body.haut2.x and  player.body.bas1.x <= sprite.body.haut1.x) and player.body.velocity.y <= 0 and player.body.haut1.y < sprite.body.bas1.y + 10 and player.body.haut1.y >= sprite.body.bas1.y - 3 :
                    player.body.velocity.y = 0
                    player.body.position.y = sprite.body.bas1.y + 1

                if sprite.body.gauche1.y >= player.body.droite1.y - 2 and sprite.body.gauche1.y <= player.body.droite2.y - 5 and  player.body.droite1.x  > sprite.body.gauche1.x and player.body.droite1.x <= sprite.body.gauche1.x + 20:
                    player.body.velocity.x = 0
                    player.body.position.x = sprite.body.gauche1.x - 2
                    if player.body.position.x > 600:
                        self.cam_affichage += 3
                        self.camera += 3

                if sprite.body.gauche1.y >= player.body.droite1.y  - 2 and sprite.body.gauche1.y <= player.body.droite2.y - 5  and  player.body.gauche1.x  < sprite.body.droite1.x and player.body.gauche1.x >= sprite.body.droite1.x - 20:
                    player.body.velocity.x = 0
                    player.body.position.x = sprite.body.haut1.x + 52
                    if player.body.position.x > 600:
                        compteur += 1
    
            elif sprite.name == "trampo":
                if (player.body.bas2.x >= sprite.body.haut2.x and player.body.bas2.x <= sprite.body.haut1.x or player.body.bas1.x >= sprite.body.haut2.x and player.body.bas1.x <= sprite.body.haut1.x) and player.body.velocity.y >= 0 and player.body.bas1.y > sprite.body.haut1.y - 10 and player.body.bas1.y <= sprite.body.haut1.y + 3 :
                    player.body.velocity.y = -10

            elif sprite.name == "demi":
                if (player.body.bas2.x >= sprite.body.haut2.x and player.body.bas2.x <= sprite.body.haut1.x or player.body.bas1.x >= sprite.body.haut2.x and player.body.bas1.x <= sprite.body.haut1.x) and player.body.velocity.y >= 0 and player.body.bas1.y > sprite.body.haut1.y - 10 and player.body.bas1.y <= sprite.body.haut1.y + 3 :
                    player.body.position.y = sprite.body.haut1.y - 100
                    player.body.velocity.y = 0   
                    player.CanJump = True

            elif sprite.name == "herbe":
                if (player.body.bas2.x >= sprite.body.haut2.x and player.body.bas2.x <= sprite.body.haut1.x or player.body.bas1.x >= sprite.body.haut2.x and player.body.bas1.x <= sprite.body.haut1.x) and player.body.velocity.y >= 0 and player.body.bas1.y > sprite.body.bas1.y - 10 and player.body.bas1.y <= sprite.body.bas1.y + 3 :
                    player.body.position.y = sprite.body.haut1.y - 50
                    player.body.velocity.y = 0   
                    player.CanJump = True    
                    
            elif sprite.name == "drapeau":
                 if player.body.droite1.x >= sprite.body.gauche1.x + 15 and player.body.gauche1.x <= sprite.body.droite1.x - 15  and player.body.bas1.y - 10 >= sprite.body.haut1.y  and player.body.haut1.y + 15 <= sprite.body.bas1.y:
                    self.fin = 1

            if compteur2 == len(self.blocks.sprites()) and compteur >= 1:
                    self.cam_affichage -= 3 
                    self.camera -= 3 

            if  self.id == 4 and self.detruire == 1 and ((sprite.body.position.x == 1750 and sprite.body.position.y == 400) or (sprite.body.position.x == 1750 and sprite.body.position.y) == 450 or (sprite.body.position.x == 1800 and sprite.body.position.y) == 400 or (sprite.body.position.x == 1800 and sprite.body.position.y == 450)):
                sprite.kill() 
                del sprite
                pass

    #Permet de gérer les collisions avec les mobs et d'infliger des dégats lorsque c'est nécessaires
    def Collision_mob(self):
        player = self.adam.sprite
        for sprite in self.mobs.sprites():
            if player.body.droite1.x >= sprite.body.gauche1.x and player.body.gauche1.x <= sprite.body.droite1.x  and player.body.bas1.y - 10 >= sprite.body.haut1.y  and player.body.haut1.y + 15 <= sprite.body.bas1.y and time.time() > player.invincibilite:
                if sprite.name == "boss":
                    if (player.body.bas2.x >= sprite.body.haut2.x + 10 and player.body.bas2.x <= sprite.body.haut1.x - 10 or player.body.bas1.x >= sprite.body.haut2.x and player.body.bas1.x <= sprite.body.haut1.x) and player.body.velocity.y >= 0 :
                        sprite.pv -= 1
                        player.body.velocity.y = -8
                        print("boss : ", sprite.pv)
                        if sprite.pv <= 0:
                            sprite.kill() 
                            del sprite
                            self.detruire = 1
                            return
                    else:
                        pygame.mixer.music.load("damage.mp3")
                        pygame.mixer.music.play(loops=0)
                        player.pdv -= 1
                        player.invincibilite = time.time() + 1
                        print("joueur:", player.pdv)
                else:
                    pygame.mixer.music.load("damage.mp3")
                    pygame.mixer.music.play(loops=0)
                    player.pdv -= 1
                    player.invincibilite = time.time() + 1
                    print("joueur:", player.pdv)

            if sprite.body.position.x < 100:
                sprite.kill() 
                del sprite
