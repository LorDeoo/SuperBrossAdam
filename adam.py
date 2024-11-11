import pygame
from body import Body
from vector import vecteur
import time

class Player(pygame.sprite.Sprite):

    #Création du joueur et de son corp
    def __init__(self, pos):
        super().__init__()
        self.anim = 0
        self.invincibilite = time.time() - 1
        self.image1 = pygame.image.load("image/Adam/AdamRun/anim1clear.png")
        self.image2 = pygame.image.load("image/Adam/AdamRun/anim2clear.png")
        self.image3 = pygame.image.load("image/Adam/AdamRun/anim3clear.png")
        self.image4 = pygame.image.load("image/Adam/AdamRun/anim4clear.png")
        self.image5 = pygame.image.load("image/Adam/AdamJumpClear.png")
        self.image6 = pygame.image.load("image/Adam/AdamMort.png")
        self.AdamTete = pygame.image.load("image/Adam/AdamteteRd.png")
        self.rect = self.image1.get_rect(topright = pos)
        self.CanJump = True
        self.pdv = 3
        self.max_pdv = 3
        self.direction = pygame.math.Vector2(0, 0)

        self.body = Body(20, self.rect.x, self.rect.y, 100, 50)

    #Fonction gérant toutes les update du joueur à chaque tour de boucle du jeux
    def update(self):
        self.moving(17)
        self.CollisionMap()
        self.clavier()

    #Recupère l'action du joueur pour les déplacements
    def clavier(self):
        touche = pygame.key.get_pressed()
 
        if touche[pygame.K_SPACE]:
            self.Jump()
        if touche[pygame.K_d] :
            self.GoRight()
            pass
        elif touche[pygame.K_q]:
            self.GoLeft()
            pass
        else: 
            self.NoMove()
            pass

    #Actualisation du corp du joueur et de son placement sur l'écran
    def moving(self, time):
        
        self.Velocity(time)
        self.rect.x = int(self.body.position.x)
        self.rect.y = int(self.body.position.y)

    #Actualisation de tout les côtés du joueur ainsi que de sa vitesse
    def Velocity(self, time):
        self.body.moment = time / 1000
        self.body.velocity.y = self.body.velocity.y + (self.body.moment*self.body.acceleration.y)
        self.body.velocity.x = self.body.velocity.x + (self.body.moment*self.body.acceleration.x)
        if self.body.velocity.y > 10:
            self.body.velocity.y = 10

        self.body.position.x = self.body.position.x + self.body.velocity.x
        self.body.position.y = self.body.position.y + self.body.velocity.y

        self.body.haut1 = self.body.position
        self.body.haut2 = vecteur(self.body.position.x - self.body.largeur, self.body.position.y)
     
        self.body.droite1 = self.body.position
        self.body.droite2 = vecteur(self.body.position.x , self.body.position.y + self.body.longueur)

        self.body.gauche1 = vecteur(self.body.position.x - self.body.largeur, self.body.position.y)
        self.body.gauche2 = vecteur(self.body.position.x - self.body.largeur , self.body.position.y + self.body.longueur)
     
        self.body.bas1 = vecteur(self.body.position.x , self.body.position.y + self.body.longueur)
        self.body.bas2 = vecteur(self.body.position.x - self.body.largeur , self.body.position.y + self.body.longueur)

     

    #Vérification de la position du joueur pour detecter si il est tombé dans le vide ou si il est en bord de map
    def CollisionMap(self):
        if self.body.bas2.y > 650:
            self.pdv = 0

        if self.body.gauche1.x <= -50:
            self.body.position.x = 0
            self.body.velocity.x = 0


    #Saute si le joueur est sur un bloc, ne peut pas si il est en l'air
    def Jump(self):
        if self.CanJump == True:
            self.body.velocity.y -= 8
            self.CanJump = False

    #Mets la vélocité du joueur en x à 3 si le joueur appuie sur d
    def GoRight(self):

        if self.body.velocity.x == 0:
            self.body.velocity.x += 3
        elif self.body.velocity.x == 3:
            self.body.velocity.x +=0
        elif self.body.velocity.x == -3:
            self.body.velocity.x += 6
       
    #Mets la vélocité du joueur en x à -3 si le joueur appuie sur q
    def GoLeft(self):

        if self.body.velocity.x == 0:
            self.body.velocity.x -= 3
        elif self.body.velocity.x == -3:
            self.body.velocity.x +=0
        elif self.body.velocity.x == 3:
            self.body.velocity.x -= 6

    #ne fait rien si le joueur n'appuie pas
    def NoMove(self):
        self.body.velocity.x = 0
      
    #Fonction permettant d'afficher la bar de point de vie du joueur
    def update_health_bar(self, screen):
        screen.blit(self.AdamTete, (20, 15))
        bar_color = (111, 210, 46)
        back_bar_color = (60, 60, 60)
        bar_position = [100, 60, self.pdv*30, 7]
        back_bar_position = [100, 60, self.max_pdv*30, 7]

        pygame.draw.rect(screen, back_bar_color, back_bar_position)
        pygame.draw.rect(screen, bar_color, bar_position)

    #Permet de créer l'animation lorsque le joueur avance ou saute
    def Draw_Player(self, surface):
        if self.anim == 48:
            self.anim = 0

        if self.invincibilite + 1 > time.time():
            surface.blit(self.image6, self.rect)

        elif self.body.velocity.x > 0 and (self.body.velocity.y < -0.1 or self.body.velocity.y > 0.1):
            surface.blit(self.image5, self.rect)

        elif self.body.velocity.x == 0 and (self.body.velocity.y < -0.1 or self.body.velocity.y > 0.1):
            surface.blit(self.image5, self.rect)

        elif self.body.velocity.x < 0 and (self.body.velocity.y < - 0.1 or self.body.velocity.y > 0.1):
            surface.blit(pygame.transform.flip(self.image5, True, False), self.rect)

        elif self.body.velocity.x > 0 :
            if self.anim >= 0 and self.anim < 8:
                surface.blit(self.image1, self.rect)
                self.anim += 1
            elif self.anim >= 8 and self.anim < 16:
                surface.blit(self.image2, self.rect)
                self.anim += 1
            elif self.anim >= 16 and self.anim < 24:
                surface.blit(self.image3, self.rect)
                self.anim += 1
            elif self.anim >= 24 and self.anim < 32:
                surface.blit(self.image4, self.rect)
                self.anim += 1
            elif self.anim >= 32 and self.anim < 40:
                surface.blit(self.image3, self.rect)
                self.anim += 1
            elif self.anim >= 40 and self.anim < 48:
                surface.blit(self.image2, self.rect)
                self.anim += 1

        elif self.body.velocity.x < 0 :
            if self.anim >= 0 and self.anim < 8:
                surface.blit(pygame.transform.flip(self.image1, True, False), self.rect)
                self.anim += 1
            elif self.anim >= 8 and self.anim < 16:
                surface.blit(pygame.transform.flip(self.image2, True, False), self.rect)
                self.anim += 1
            elif self.anim >= 16 and self.anim < 24:
                surface.blit(pygame.transform.flip(self.image3, True, False), self.rect)
                self.anim += 1
            elif self.anim >= 24 and self.anim < 32:
                surface.blit(pygame.transform.flip(self.image4, True, False), self.rect)
                self.anim += 1
            elif self.anim >= 32 and self.anim < 40:
                surface.blit(pygame.transform.flip(self.image3, True, False), self.rect)
                self.anim += 1
            elif self.anim >= 40 and self.anim < 48:
                surface.blit(pygame.transform.flip(self.image2, True, False), self.rect)
                self.anim += 1

        elif self.body.velocity.x == 0:
            surface.blit(self.image1, self.rect)
            self.anim == 0


        
    