import pygame
import sys
from math import sqrt

# --- 1. Initialisation ---
pygame.init()
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

speed = 3


def main():

    LARGEUR = 800
    HAUTEUR = 600
    rect_x = 10
    rect_y = 10
    
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Premier projet pygame")
    fenetre.fill(WHITE)   # Fond blanc (RGB)

   
    # --- 2. Boucle principale ---
    while True:

        # --- 3. Gestion des events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and touches[pygame.K_DOWN]:
            rect_x -= speed/2
            rect_y += speed/2 
        elif touches[pygame.K_LEFT] and touches[pygame.K_UP]:
            print("shatta run di place and guess who a bring it up")
            rect_x -= speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_RIGHT] and touches[pygame.K_UP]:
            print("shatta run di place and guess who a bring it up")
            rect_x += speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_RIGHT] and touches[pygame.K_DOWN]:
            print("shatta run di place and guess who a bring it up")
            rect_x += speed/2   
            rect_y += speed/2
        
        elif touches[pygame.K_LEFT]:
            rect_x -= speed
        elif touches[pygame.K_RIGHT]:
            rect_x += speed
        elif touches[pygame.K_DOWN]:
            rect_y+= speed
        elif touches[pygame.K_UP]:
            rect_y-= speed




        # --- Mise a jour de l'affichage --- 
        fenetre.fill(WHITE)
        pygame.draw.rect( fenetre, BLUE ,(rect_x, rect_y, 10, 10))
        pygame.draw.circle(fenetre, BLUE,(rect_x+5, rect_y+5,), 200,1)
        pygame.display.flip()           # Rafraichissement de l'ecran
        clock.tick(60)                # Limite a 60 images par seconde


if __name__=="__main__":
    main()