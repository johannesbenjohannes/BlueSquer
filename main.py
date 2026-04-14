import pygame
import sys
import math as m
import random as rd

# --- 1. Initialisation ---
pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
base_font=pygame.font.SysFont('Comic Sans MS', 30)

def check_surrounding_pixel_colors(surface,x,y,target,n):
    for i in range(int(x),int(x+n)):
        for j in range(int(y),int(y+n)):
            if surface.get_at((int(i), int(j))) == target:
                return True
    return False


def main():

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    speed = 3

    LARGEUR = 800 # Largeur de la 
    compteur_attaque_ligne = 0 # Compteur de tick lors de l'attaque de la ligne 
    compteur_attaque_cercle = 0 # Compteur tick lors de l'attaque de la lignefenêtre
    HAUTEUR = 600 # Hauteur de la frenêtre
    
    rect_x = 10
    rect_y = 10

    compteur = 0 # Compteur global des ticks

    line_attacking = False # Etat d'attaque de ligne 
    circle_attacking = False #Etat d'attaque de cercle

    alive = True # Etat du player

    compteur_attaque_ligne = 0 # Compteur de tick lors de l'attaque de la ligne 
    compteur_attaque_cercle = 0 # Compteur tick lors de l'attaque de la ligne

    has_dashed = False # Etat du dash
    compteur_dash = 600 # Cooldown du dash

    ispattern_ligne = False # Est-ce que le pattern en cours est la ligne ?
    ispattern_cercle = True # Est-ce que le pattern en cours est le cercle ?

    attaques_ligne = 0 # Compteur des attaques  ligne 
    attaques_cercle = 0 #compteur des attaques cercle
    drawcircle = False # Est-ce qu'il faut dessiner le cercle actuellement ?
    drawline = False # Est-ce qu'il faut dessiner la ligne actuellement ?

    class BossBullet: # Classe pour les projectiles du boss
        def __init__(self, x, y, target_x, target_y, velocity=5):
            self.x = x
            self.y = y
            self.target_x = target_x
            self.target_y = target_y
            self.velocity = velocity

    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Premier projet pygame")
    fenetre.fill(WHITE) # Fond blanc (RGB)

    # --- 2. Boucle principale ---
    while True:

        compteur+=1 # CHECKS DU LANCEMENT DU PATTERN
        
        

        # --- 3. Gestion des events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and touches[pygame.K_DOWN] and rect_x > 0 and rect_y < 590:
            rect_x -= speed/2
            rect_y += speed/2 
        elif touches[pygame.K_LEFT] and touches[pygame.K_UP] and rect_x > 0 and rect_y > 0:
            rect_x -= speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_RIGHT] and touches[pygame.K_UP] and rect_x < 790 and rect_y > 0:
            rect_x += speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_RIGHT] and touches[pygame.K_DOWN] and rect_x < 790 and rect_y < 590:
            rect_x += speed/2   
            rect_y += speed/2
        
        elif touches[pygame.K_LEFT] and rect_x > 0:
            rect_x -= speed
        elif touches[pygame.K_RIGHT] and rect_x < 790:
            rect_x += speed
        elif touches[pygame.K_DOWN] and rect_y < 590:
            rect_y+= speed
        elif touches[pygame.K_UP] and rect_y > 0:
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

        # --- Mise a jour de l'affichage Ceci est généralement causé par un autre dépôt poussé
        fenetre.fill(WHITE)
        if alive:
            
            pygame.draw.rect( fenetre, BLUE ,(rect_x, rect_y, 10, 10))
            pygame.draw.circle(fenetre, WHITE,(rect_x+5, rect_y+5,), 200,1)
            pygame.draw.rect(fenetre, BLUE,(50,50,round(compteur_dash/10),50))
            pygame.draw.rect(fenetre, BLACK,(45,45,70,55),5)


            # CHECK DE LA PHASE - TRES SENSIBLE - NE PAS CODER AUTRE CHOSE
            # POUR L'INSTANT; que le check du pattern ligne
            ispattern_ligne = True
            attaques_ligne = 0
            if attaques_ligne == 10*1.5:
                ispattern_ligne = False
                    
            
            """      
            def phase(nb_phase): # Lancer le comportement associé à sa phase
                
                
                if nb_phase == 1:
                    patternes=[pattern_ligne, pattern_cercle]
                    patternes[rd.randint(0,1)](10)"/home/canard101/NSI_proj/main.py", line 212, in <module>
    main()
  File "/home/canard101/NSI_proj/main.py", line 189, in
            """
            # FIN DE LA ZONE INTERDITE

            if compteur%60 == 0 and ispattern_ligne: 
                drawline = True
            if compteur%5==0 and ispattern_cercle:
                drawcircle = True

            if line_attacking:
                compteur_attaque_ligne+=0.25
            if has_dashed :
                compteur_dash+=1

            if drawline:
                if line_attacking == False:
                    rdTheta = rd.uniform(0, 2*m.pi)
                    attack_x = rect_x+2000*m.cos(rdTheta)
                    attack_y = rect_y+2000*m.sin(rdTheta)
                    end_x = rect_x+2000*m.cos(rdTheta+m.pi) 
                    end_y = rect_y+2000*m.sin(rdTheta+m.pi)
                line_attacking = True
                
                pygame.draw.line(fenetre, GREEN,(attack_x, attack_y),(end_x, end_y),round(compteur_attaque_ligne%50))
                if compteur_attaque_ligne%50 == 9:
                    pygame.draw.line(fenetre, RED,(attack_x, attack_y),(end_x, end_y),round(compteur_attaque_ligne%50))
                    drawline=False
                    line_attacking=False
                    compteur_attaque_ligne = 0
                    attaques_ligne+=1

            if drawcircle:
                if circle_attacking == False:
                    attack_x = rect_x+5
                    attack_y = rect_y+5
                circle_attacking = True
                pygame.draw.circle(fenetre, GREEN,(attack_x,attack_y),round(compteur_attaque_cercle))
                if compteur_attaque_cercle == 9:
                    pygame.draw.circle(fenetre, RED,(attack_x,attack_y),round(compteur_attaque_cercle))
                    drawcircle = False
                    circle_attacking = False
                    compteur_attaque_cercle = 0


            current_color = fenetre.get_at((int(rect_x)+5, int(rect_y)+5))
            
            text_color=base_font.render(f"color: {current_color}", False, (0,0,0))
            if check_surrounding_pixel_colors(fenetre,rect_x,rect_y,RED,10):
                text_collison=base_font.render("collision", False, (0,0,0))
                fenetre.blit(text_collison, (400,2))
            fenetre.blit(text_color, (2,2))

            pygame.draw.rect( fenetre, BLUE ,(rect_x, rect_y, 10, 10))
            pygame.draw.circle(fenetre, WHITE,(rect_x+5, rect_y+5,), 200,1)
            
        pygame.display.flip()           # Rafraichissement de l'ecran
        clock.tick(60)                # Limite a 60 images par seconde



"""      
def phase(nb_phase): # Lancer le comportement associé à sa phase
    
    
    if nb_phase == 1:
        patternes=[pattern_ligne, pattern_cercle]
        patternes[rd.randint(0,1)](10)
    """

if __name__=="__main__":
    main()