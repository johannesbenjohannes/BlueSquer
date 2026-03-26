import pygame
import sys

# --- 1. Initialisation ---
pygame.init()
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


def main():

    LARGEUR = 800
    HAUTEUR = 600
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


        # --- Mise a jour de l'affichage ---
        pygame.draw.rect( fenetre, BLUE ,(10, 10, 10, 10))
        pygame.display.flip()           # Rafraichissement de l'ecran
        clock.tick(60)                # Limite a 60 images par seconde


if __name__=="__main__":
    main()