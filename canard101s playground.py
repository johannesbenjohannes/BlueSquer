import pygame
import sys
import math as m
import random as rd


# --- 1. Initialisation ---
pygame.init()
pygame.font.init()
base_font=pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Sol:
    x=0
    y=400
    width=800
    height=2

class Player:
    x=400
    y=0
    radius=20
    velocity=10
    cinetic=0
    jump=False
    jumpCount=0
    jumpMax=15

    def calc_fall():
        if Player.y<Sol.y-Player.radius and Player.jump==False:
            Player.y += Player.velocity

    def calc_jump():
        if Player.jump:
            Player.y -= Player.jumpCount
            if Player.jumpCount > -Player.jumpMax:
                Player.jumpCount -= 1
            else:
                Player.jump = False 


    def move(dir_x, dir_y):
        if dir_y == 1 and Player.y + Player.velocity <= Sol.y-Player.radius:
            Player.y += Player.velocity
        elif dir_y == -1:
            pass
        elif dir_x == 1 and Player.x <= Sol.width-Player.radius-5:
            Player.x += Player.velocity
        elif dir_x == -1 and Player.x >= Player.radius+5:  
            Player.x -= Player.velocity

class Obstacle:

    def __init__(self):
        self.rect = pygame.Rect(x,y,width,height)
        

        

def main():

    LARGEUR = 800
    HAUTEUR = 600

    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("suppa duppa platafomma")
    fenetre.fill(WHITE)   # Fond blanc (RGB)

   
    # --- 2. Boucle principale ---
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        Player.calc_fall()
        Player.calc_jump()
        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT] and touches[pygame.K_SPACE]:
            Player.move(-1,0)
            if not Player.jump:
                Player.jump = True
                Player.jumpCount = Player.jumpMax
        elif touches[pygame.K_RIGHT] and touches[pygame.K_SPACE]:
            Player.move(1,0)
            if not Player.jump:
                Player.jump = True
                Player.jumpCount = Player.jumpMax

        elif touches[pygame.K_LEFT]:
            Player.move(-1,0)
        elif touches[pygame.K_RIGHT]:
            Player.move(1,0)
         
 
        elif touches[pygame.K_SPACE]:
            if not Player.jump:
                Player.jump = True
                Player.jumpCount = Player.jumpMax


        # --- Mise a jour de l'affichage --- 
        fenetre.fill(WHITE)
        pygame.draw.rect(fenetre, BLACK, (Sol.x, Sol.y, Sol.width, Sol.height))
        pygame.draw.circle(fenetre, BLACK, (Player.x, Player.y), Player.radius)
        text_x=base_font.render(f"x={Player.x}", False, (0,0,0))
        text_y=base_font.render(f"y={Player.y}", False, (0,0,0))
        text_vty=base_font.render(f"velocity={Player.velocity}", False, (0,0,0))
        text_cinetic=base_font.render(f"cinetic={Player.cinetic}", False, (0,0,0))
        fenetre.blit(text_x, (2,2))
        fenetre.blit(text_y, (2,22))
        fenetre.blit(text_vty, (2,42))
        fenetre.blit(text_cinetic, (2,62))

        pygame.display.flip()           # Rafraichissement de l'ecran
        clock.tick(60)                # Limite a 60 images par seconde


if __name__=="__main__":
    main()