import pygame
import sys
import math as m
import random as rd
from pyvectors import Vector2

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
    
    HAUTEUR = 600 # Hauteur de la frenêtre
    
    rect_x = 10
    rect_y = 10

    compteur = 0 # Compteur global des ticks

    #line_attacking = False  Etat d'attaque de ligne 
    #circle_attacking = False #Etat d'attaque de cercle

    #compteur_attaque_ligne = 0 # Compteur de tick lors de l'attaque de la ligne 
    #compteur_attaque_cercle = 0 # Compteur tick lors de l'attaque de la lignefenêtre

    #ispattern_ligne = False # Est-ce que le pattern en cours est la ligne ?
    #ispattern_cercle = True # Est-ce que le pattern en cours est le cercle ?

    #attaques_ligne = 0 # Compteur des attaques  ligne 
    #attaques_cercle = 0 #compteur des attaques cercle

    #drawcircle = False # Est-ce qu'il faut dessiner le cercle actuellement ?
    #drawline = False # Est-ce qu'il faut dessiner la ligne actuellement ?

    nb_phase = 1 # Nombre de la phase actuelle

    current_pattern = "NO PATTERN" # Pattern actuel
    draw_what = "NO PATTERN" # Que doit-on dessiner

    patterns = {
        "line": {
            "attacking": False, # État d'attaque de la ligne
            "compteur_attaque": 0, # Compteur de tick lors de l'attaque de la ligne
            "attaques": 0, # Compteur des attaques de la ligne
            "attaques_max": 15 # Nombre d'attaques max avant de changer de pattern
        },
        "circle": {
            "attacking": False, # État d'attaque du cercle
            "compteur_attaque": 0, # Compteur de tick lors de l'attaque du cercle
            "attaques": 0, # Compteur des attaques du cercle
            "attaques_max": 15 # Nombre d'attaques max avant de changer de pattern
        }
    }

    phase_1 = ["line", "circle"] # Patterns de la phase 1

    alive = True # Etat du player

    has_dashed = False # Etat du dash
    compteur_dash = 600 # Cooldown du dash

    mouse_x = 0 #Abscisse de la souri
    mouse_y = 0 #Ordonnée de la souri
    projectile_active = False

    class Bullet: # Classe pour les projectiles
        def __init__(self, x, y, target_x, target_y, velocity=5) :
            self.x = x
            self.y = y
            self.target_x = target_x
            self.target_y = target_y
            self.velocity = velocity

    class CircleAttack:
        circles=[]
        def __init__(self,x,y,t):
            self.x = x
            self.y = y
            self.t = t
            self.r = 0
            self.color = GREEN
        def draw(self):
            pass

        def update(self):
            if self.t == 36:
                self.color = RED
            if self.t % 4:
                self.r += 1

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
        if touches[pygame.K_q] and touches[pygame.K_s] and rect_x > 0 and rect_y < 590:
            rect_x -= speed/2
            rect_y += speed/2 
        elif touches[pygame.K_q] and touches[pygame.K_z] and rect_x > 0 and rect_y > 0:
            rect_x -= speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_d] and touches[pygame.K_z] and rect_x < 790 and rect_y > 0:
            rect_x += speed/2   
            rect_y -= speed/2
        elif touches[pygame.K_d] and touches[pygame.K_s] and rect_x < 790 and rect_y < 590:
            rect_x += speed/2   
            rect_y += speed/2
        elif touches[pygame.K_q] and rect_x > 0:
            rect_x -= speed
        elif touches[pygame.K_d] and rect_x < 790:
            rect_x += speed
        elif touches[pygame.K_s] and rect_y < 590:
            rect_y+= speed
        elif touches[pygame.K_z] and rect_y > 0:
            rect_y-= speed

        if touches[pygame.K_SPACE]:
            if compteur_dash==600:
                    has_dashed= True
                    compteur_dash = 0
                    speed = 13
        
        """if event.type == pygame.MOUSEBUTTONDOWN : 
            mouse_x,mouse_y = event.pos
            
            if event.button == 1:
<<<<<<< HEAD
                projectile = Bullet(rect_x, rect_y, mouse_x)
"""
           
=======
                if projectile_active is not True :
                    projectile = Bullet(rect_x+5, rect_y+5, mouse_x, mouse_y)
                    bullet_pos = Vector2(projectile.x, projectile.y)
                    start_x = projectile.x
                    start_y = projectile.y
                    projectile_active = True
                    text_bullet = base_font.render(str(projectile.x), False,(0,0,0))
                    fenetre.blit(text_bullet, (2,400))
                    if 0<projectile.x<800 and 0<projectile.y<600 : 
                        print(projectile_active)
                        pygame.draw.circle(fenetre, BLACK,bullet_pos.components,5)
                        increase_y = Vector2(start_x, projectile.target_y)
                        increase_x = Vector2(start_y, projectile.target_x)
                        bullet_pos += Vector2(increase_x,increase_y)
                    projectile_active = False
                    print("a")


            
>>>>>>> 0cde53afe2323704f55959d3bd74ffb3e68be931
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
            if current_pattern == "NO PATTERN":
                print("Y'a pas de pattern là, on choisit")
                if nb_phase == 1:
                    current_pattern = rd.choice(phase_1)
                    print(current_pattern)
                    patterns[current_pattern]["attaques"] = 0


            if patterns[current_pattern]["attaques"] == patterns[current_pattern]["attaques_max"]:
                print("YEP CFINI")
                patterns[current_pattern]["attaques"] = 0
                patterns[current_pattern]["attacking"] = False
                patterns[current_pattern]["compteur_attaque"] = 0
                current_pattern = "NO PATTERN"
            
            if current_pattern != "NO PATTERN":
                print(patterns[current_pattern]["attaques"])
            
            # FIN DE LA ZONE INTERDITE

            #if compteur%60 == 0 and ispattern_ligne: 
            #    drawline = True
            #if compteur%60==0 and ispattern_cercle:
            #    drawcircle = True
            
            if compteur%60 and current_pattern != "NO PATTERN":
                draw_what = current_pattern

            if current_pattern != "NO PATTERN" and patterns[current_pattern]["attacking"] == True:
                patterns[current_pattern]["compteur_attaque"]+=0.25

            if has_dashed :
                compteur_dash+=1

            if draw_what == "line":
                if patterns["line"]["attacking"] == False:
                    rdTheta = rd.uniform(0, 2*m.pi)
                    attack_x = rect_x+2000*m.cos(rdTheta)
                    attack_y = rect_y+2000*m.sin(rdTheta)
                    end_x = rect_x+2000*m.cos(rdTheta+m.pi) 
                    end_y = rect_y+2000*m.sin(rdTheta+m.pi)
                patterns["line"]["attacking"] = True
                
                pygame.draw.line(fenetre, GREEN,(attack_x, attack_y),(end_x, end_y),round(patterns["line"]["compteur_attaque"]%50))
                if patterns["line"]["compteur_attaque"]%50 == 9:
                    pygame.draw.line(fenetre, RED,(attack_x, attack_y),(end_x, end_y),round(patterns["line"]["compteur_attaque"]%50))
                    draw_what = "NO PATTERN"
                    patterns["line"]["attacking"] = False
                    patterns["line"]["compteur_attaque"] = 0
                    patterns["line"]["attaques"]+=1

            if draw_what == "circle":
                if patterns["circle"]["attacking"] == False:
                    attack_x = rect_x +5
                    attack_y = rect_y+5
                patterns["circle"]["attacking"] = True

                pygame.draw.circle(fenetre, GREEN,(attack_x,attack_y),round(patterns["circle"]["compteur_attaque"]))
                if patterns["circle"]["compteur_attaque"] == 9:
                    pygame.draw.circle(fenetre, RED,(attack_x,attack_y),round(patterns["circle"]["compteur_attaque"]))
                    draw_what = "NO PATTERN"
                    patterns["circle"]["attacking"] = False
                    patterns["circle"]["compteur_attaque"] = 0
                    patterns["circle"]["attaques"]+=1


            current_color = fenetre.get_at((int(rect_x)+5, int(rect_y)+5))
            
            text_color=base_font.render(f"color: {current_color}", False, (0,0,0))
            if check_surrounding_pixel_colors(fenetre,rect_x,rect_y,RED,10):
                text_collison=base_font.render("collision", False, (0,0,0))
                fenetre.blit(text_collison, (400,2))
            fenetre.blit(text_color, (2,2))
            text_ticks=base_font.render(f"t: {compteur}", False, (0,0,0))
            fenetre.blit(text_ticks, (700, 2))
            pygame.draw.rect( fenetre, BLUE ,(rect_x,rect_y, 10, 10))
            pygame.draw.circle(fenetre, WHITE,(rect_x+5, rect_y+5,), 200,1)
            
        pygame.display.flip()           # Rafraichissement de l'ecran
        clock.tick(60)                # Limite a 60 images par seconde

if __name__=="__main__":
    main()