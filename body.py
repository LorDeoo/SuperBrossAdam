from pygame import Vector2
from vector import vecteur

class Body():
    #Création d'un corp pour un sprite en fonction de ses dimensions et des lois physique qui s'applique à lui
    def __init__(self, masse, pos_x, pos_y, longueur, largeur ):
        self.masse = masse
        self.moment = float(0)
        self.longueur = longueur
        self.largeur = largeur

        self.gravity = vecteur(0, 10)

        self.position = vecteur(pos_x, pos_y)

        self.velocity = vecteur(0, 0)

        self.force = vecteur(self.masse * self.gravity.x, self.masse * self.gravity.y)
       
        self.acceleration = vecteur(self.force.x / self.masse, self.force.y / self.masse)

        #Création des 4 côtés du corp pour gérer les collisions
        self.haut1 = vecteur(pos_x, pos_y)
        self.haut2 = vecteur(pos_x - largeur, pos_y)

        self.droite1 = vecteur(pos_x, pos_y)
        self.droite2 = vecteur(pos_x , pos_y + longueur)

        self.bas1 = vecteur(pos_x, pos_y + longueur)
        self.bas2 = vecteur(pos_x - largeur , pos_y + longueur)

        self.gauche1 = vecteur(pos_x - largeur, pos_y )
        self.gauche2 = vecteur(pos_x - largeur , pos_y + longueur)

        
      







