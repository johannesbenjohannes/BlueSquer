import pygame
import sys
import math as m
import random as rd
import time as t


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
    compteur = 0
    attacking = False
    alive = True
    compteur_attaque=0
    has_dashed = False
    compteur_dash=600
    Ispattern_ligne=False
    attaques = 0


    
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Premier projet pygame")
    rect_y = 10
    compteur = 0
    
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Premier projet pygame")
    fenetre.fill(WHITE)   # Fond blanc (RGB)

    drawline = False
    def pattern_ligne(nb_attaques):
        Ispattern_ligne = True
        attaques = 0
        if attaques == nb_attaques:
            Ispattern_ligne
            return




    

    # --- 2. Boucle principale ---
    while True:
        compteur+=1
        if compteur%60==0 or Ispattern_ligne: 
            drawline = True
        if attacking:
            compteur_attaque+=0.25
        if has_dashed :
            compteur_dash+=1
        global speed

            

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
            rect_x -= speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_RIGHT] and touches[pygame.K_UP]:
            rect_x += speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_RIGHT] and touches[pygame.K_DOWN]:
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

        if touches[pygame.K_SPACE]:
            if compteur_dash==600:
                    has_dashed= True
                    compteur_dash = 0
                    speed = 13
                   
            
        if has_dashed:
            if compteur_dash>7:
                    speed = 3
        if has_dashed ==True:
            if compteur_dash==600:
                has_dashed=False


               
        




        # --- Mise a jour de l'affichage --- 
        fenetre.fill(WHITE)
        if alive:
            pygame.draw.rect( fenetre, BLUE ,(rect_x, rect_y, 10, 10))
            pygame.draw.circle(fenetre, WHITE,(rect_x+5, rect_y+5,), 200,1)
            pygame.draw.rect(fenetre, BLUE,(50,50,round(compteur_dash/10),50))
            pygame.draw.rect(fenetre, BLACK,(45,45,70,55),5)
            if drawline:
                if attacking ==False:
                    rdTheta= rd.uniform(0, 2*m.pi)
                    attack_x = rect_x+2000*m.cos(rdTheta)
                    attack_y = rect_y+2000*m.sin(rdTheta)
                    end_x = rect_x+2000*m.cos(rdTheta+m.pi) 
                    end_y = rect_y+2000*m.sin(rdTheta+m.pi)
                attacking = True
                pygame.draw.line(fenetre, GREEN,(attack_x, attack_y),(end_x, end_y),round(compteur_attaque%50))
                if compteur_attaque%10==9:
                    pygame.draw.line(fenetre, RED,(attack_x, attack_y),(end_x, end_y),round(compteur_attaque%50))
                    drawline=False
                    attacking=False
                    compteur_attaque = 0
                    attaques+=1


            

        pygame.display.flip()           # Rafraichissement de l'ecran
        clock.tick(60)                # Limite a 60 images par seconde


if __name__=="__main__":
    main()