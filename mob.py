import pygame
from body import Body
import time
from vector import vecteur

#Création des variables nécessaires au mob
class Mob(pygame.sprite.Sprite):
    def __init__(self, name, pos):
        super().__init__()
        self.time = time.time()
        self.name = name
        self.setup( pos)

    #Chargement de l'image du mob et de son corp
    def setup(self, pos):
        if self.name == "mob1":
            self.image = pygame.image.load("image/Mobs/monstre.png")
            self.rect = self.image.get_rect(topright = pos)
            self.body = Body(1, self.rect.x, self.rect.y, 50 , 50)
        elif self.name == "mob2":
            self.dir = 1
            self.image = pygame.image.load("image/Mobs/monstre2.png")
            self.rect = self.image.get_rect(topright = pos)
            self.body = Body(1, self.rect.x, self.rect.y, 50 , 50)
        elif self.name == "canon":
            self.dir = -1
            self.image = pygame.image.load("image/Blocs/canon.png")
            self.rect = self.image.get_rect(topright = pos)
            self.body = Body(1, self.rect.x, self.rect.y, 50 , 50)
        elif self.name == "bdf":
            self.dir = 0
            self.image = pygame.image.load("image/Blocs/bdf.png")
            self.rect = self.image.get_rect(topright = pos)
            self.body = Body(1, self.rect.x, self.rect.y, 35 , 35)
        elif self.name == "boss":
            self.dir = 0
            self.image = pygame.image.load("image/Mobs/boss.png")
            self.rect = self.image.get_rect(topright = pos)
            self.body = Body(1, self.rect.x, self.rect.y, 100 , 50)
            self.timebdf = time.time()
            self.pv = 3
            self.max_pv = 3
            self.boule = pygame.sprite.Group()

    #Actualisation de chaque mob, dépend de son type
    def update(self, x_shift, cam_affichage, blocks,  position, velocity, player, surface):
        if self.name == "mob1":
            self.rect.x += x_shift

        elif self.name == "boss":
            self.move(blocks, player)
            self.collision()
            self.shoot( x_shift, cam_affichage, blocks,  position, velocity, player, surface)
            self.camera(x_shift, cam_affichage, position, velocity)
            self.update_health_bar(surface)
        else:
            self.move(blocks, player)
            self.collision()
            self.camera(x_shift, cam_affichage, position, velocity)
                
    """
    Déplace le mob en fonction de qui il est: 
    mob2 fait des droites gauche tant qu'il n'a pa de collision avec un mur
    Boulet de canon et boule de feu vont juste tout droit
    le boss se déplace en fonction de la position du joueur 
    et actualisation de tout les corps
    """
    def move(self, blocks, player):
        if self.name == "mob2":
            self.body.position.x += self.dir
            for sprite in blocks.sprites():
                if (self.body.bas2.x >= sprite.body.haut2.x and self.body.bas2.x <= sprite.body.haut1.x or self.body.bas1.x >= sprite.body.haut2.x and self.body.bas1.x <= sprite.body.haut1.x) and self.body.velocity.y >= 0 and self.body.bas1.y > sprite.body.haut1.y - 10 and self.body.bas1.y <= sprite.body.haut1.y + 3 :
                    self.body.position.y = sprite.body.haut1.y - 50
                    self.body.velocity.y = 0

                if sprite.body.gauche1.y >= self.body.droite1.y - 2 and sprite.body.gauche1.y <= self.body.droite2.y - 5 and  self.body.droite1.x  > sprite.body.gauche1.x and self.body.droite1.x <= sprite.body.gauche1.x + 20 and self.dir == 1 and time.time() > self.time:
                    self.dir = -1
                    self.time = self.time + 0.4
                if sprite.body.gauche1.y >= self.body.droite1.y  - 2 and sprite.body.gauche1.y <= self.body.droite2.y - 5  and  self.body.gauche1.x  < sprite.body.droite1.x and self.body.gauche1.x >= sprite.body.droite1.x - 20 and self.dir == -1 and time.time() > self.time:
                  self.dir = 1
                  self.time = self.time + 0.4

            self.body.velocity.y = self.body.velocity.y + (self.body.moment*self.body.acceleration.y)
            self.body.velocity.x = self.body.velocity.x + (self.body.moment*self.body.acceleration.x)

            self.body.position.x = self.body.position.x + self.body.velocity.x
            self.body.position.y = self.body.position.y + self.body.velocity.y

        elif self.name == "canon":
            self.body.position.x += self.dir
        elif self.name == "bdf":
            self.body.position.x += self.dir

        elif self.name == "boss":
            player = player.sprite
            if self.body.position.x - player.body.position.x < 200 and self.body.position.x - player.body.position.x > -200:
                if self.body.position.x - player.body.position.x < 200 and self.body.position.x - player.body.position.x >= 0 :
                    if self.pv >= 2:
                        self.body.velocity.x = 2
                    else:
                        self.body.velocity.x = 3
                elif self.body.position.x - player.body.position.x > -200 and self.body.position.x - player.body.position.x < 0:
                    if self.pv >= 2:
                        self.body.velocity.x = -2
                    else:
                        self.body.velocity.x = -3
                else:
                    self.body.velocity.x = 0
                self.body.position.x += self.body.velocity.x

            for sprite in blocks.sprites():

                if sprite.rect.colliderect(self.rect ) and (self.body.velocity.x == 2 or self.body.velocity.x == 3)   :
                    self.body.velocity.x = 0
                    self.body.position.x = sprite.body.gauche1.x - 2

                if sprite.rect.colliderect(self.rect ) and (self.body.velocity.x == -2 or self.body.velocity.x == -3) :
                    self.body.velocity.x = 0
                    self.body.position.x = sprite.body.haut1.x + 52

        delai = 17
        self.body.moment = delai / 1000

        self.body.haut1 = self.body.position
        self.body.haut2 = vecteur(self.body.position.x - self.body.largeur, self.body.position.y)
     
        self.body.droite1 = self.body.position
        self.body.droite2 = vecteur(self.body.position.x , self.body.position.y + self.body.longueur)

        self.body.gauche1 = vecteur(self.body.position.x - self.body.largeur, self.body.position.y)
        self.body.gauche2 = vecteur(self.body.position.x - self.body.largeur , self.body.position.y + self.body.longueur)
     
        self.body.bas1 = vecteur(self.body.position.x , self.body.position.y + self.body.longueur)
        self.body.bas2 = vecteur(self.body.position.x - self.body.largeur , self.body.position.y + self.body.longueur)
        self.rect.x = int(self.body.position.x)
        self.rect.y = int(self.body.position.y)


    #Permet de gérer la caméra des mobs
    def camera(self,x_shift, cam_affichage, position, velocity):
        if position > 600 and velocity > 0:
            cam_affichage -= velocity
            self.rect.x += cam_affichage
        elif position > 600 and velocity < 0:
            cam_affichage -= velocity
            self.rect.x += cam_affichage
        else:
            self.rect.x += cam_affichage

    #Les mobs ne peuvent pas tomber dans le vide
    def collision(self):
        if self.body.bas2.y > 550:
            self.body.position.y = 500
            self.body.velocity.y = 0

    """
    Fonction permettant de gérer les boules de feu du boss
    il tire toutes les 3 secondes lorsqu'il a 3pv et toutes les 1,5 secondes lorsqu'il a moin de 2 pv
    Gère également dans quel direction doit aller le boss en fonction de la position du joueur
    et update toutes les boules de feu
    """
    def shoot(self, x_shift, cam_affichage, blocks,  position, velocity, adam, surface, ):
        player = adam.sprite
        if self.body.position.x - player.body.position.x < 300 or self.body.position.x - player.body.position.x < -300:
                if time.time()  > self.time:
                    mob = Mob("bdf", (self.body.position.x , self.body.position.y))
                    if self.body.position.x - player.body.position.x < 300 and self.body.position.x - player.body.position.x > 0:
                        mob.dir = -1
                    else:
                        mob.dir = 1
                    self.boule.add(mob)
                    if self.pv == 3:
                        self.time = time.time() + 3
                    else:
                        self.time = time.time() + 1.5
        self.boule.update( x_shift, cam_affichage, blocks,  position, velocity, adam, surface)
        self.Collision_mob(adam)
        self.boule.draw(surface)

    #Permet de gérer les collisions entre les boules de feu et le joueur
    def Collision_mob(self, adam):
        player = adam.sprite
        for sprite in self.boule.sprites():
            if player.body.droite1.x >= sprite.body.gauche1.x + 10 and player.body.gauche1.x <= sprite.body.droite1.x - 10  and player.body.bas1.y - 10 >= sprite.body.haut1.y  and time.time() > player.invincibilite:
                player.pdv -= 1
                player.invincibilite = time.time() + 1
                print("joueur:", player.pdv)

            if sprite.body.position.x < 700 or sprite.body.position.x > 2000:
                sprite.kill() 
                del sprite

    #Fonction permettant d'afficher la bar de point de vie du boss
    def update_health_bar(self, screen):
        bar_color = (111, 210, 46)
        back_bar_color = (60, 60, 60)
        bar_position = [self.rect.x, self.rect.y - 10, self.pv*15, 5]
        back_bar_position = [self.rect.x, self.rect.y - 10, self.max_pv*15, 5]

        pygame.draw.rect(screen, back_bar_color, back_bar_position)
        pygame.draw.rect(screen, bar_color, bar_position)