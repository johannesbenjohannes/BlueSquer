import pygame
import sys
import os
import math as m
import random as rd
from pyvectors import Vector2
from time import sleep

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
    LIGHT_BLUE = (0,160,255)
    BRASS = (255, 159, 41)
    LIGHT_BRASS = (255, 200, 91)
    SALMON = (255, 99, 85)
    DARK_SALMON = (200, 60, 85)
    BORDEAUX = (159, 7, 18)
    speed = 3
    

    LARGEUR = 800 # Largeur de la 
    compteur_attaque_ligne = 0 # Compteur de tick lors de l'attaque de la ligne 
    compteur_attaque_cercle = 0 # Compteur tick lors de l'attaque de la lignefenêtre
    HAUTEUR = 600 # Hauteur de la frenêtre
    
    rect_x = 10
    rect_y = 10
    moving = False

    past_rect_x = 0
    past_rect_y = 0

    boss_target_x = 0
    boss_target_y = 0
    boss_target_pos = Vector2(1,1)

    player_direction = Vector2(1,1)

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

    nb_phase = 2 # Nombre de la phase actuelle

    current_pattern = "NO PATTERN" # Pattern actuel
    previous_pattern = "NO PATTERN"
    draw_what = "NO PATTERN" # Que doit-on dessiner


    projectile = []

    patterns = {
        "line": {
            "attacking": False, # État d'attaque de la ligne
            "compteur_attaque": 0, # Compteur de tick lors de l'attaque de la ligne
            "attaques": 0, # Compteur des attaques de la ligne
            "attaques_max": 15, # Nombre d'attaques max avant de changer de pattern

        },
        "circle": {
            "attacking": False, # État d'attaque du cercle
            "compteur_attaque": 0, # Compteur de tick lors de l'attaque du cercle
            "attaques": 0, # Compteur des attaques du cercles
            "attaques_max": 30, # Nombre d'attaques max avant de changer de pattern

        },
        "bullets":{
            "attacking": False,
            "angles": [i*(m.pi/6) for i in range(12)],
            "attaques": 0,
            "attaques_max": 12,
            "compteur_attaque":0
        },
        "line2":{
            "attacking": False, # État d'attaque de la ligne
            "compteur_attaque": 0, # Compteur de tick lors de l'attaque de la ligne
            "attaques": 0, # Compteur des attaques de la ligne
            "attaques_max": 20, # Nombre d'attaques max avant de changer de pattern

        }
    }

    phase_1 = ["circle", "bullets","line"] # Patterns de la phase 1
    phase_2 = ["line"]
    alive = True # Etat du player
    immortel = True # Mettre 'True' pour ne pas mourrir à la moindre collision

    has_dashed = False # Etat du dash
    compteur_dash = 300 # Cooldown du dash

    has_shot = False
    compteur_shot = 30

    mouse_x = 0
    mouse_y = 0



    class Bullet: # Classe pour les projectiles
        def __init__(self, pos, target, nature, velocity=6) :
            self.pos = pos
            self.target = target
            self.velocity = velocity
            self.nature = nature

    class Ennemy:
        def __init__(self,pos,w,h,health):
            self.pos = pos
            self.w = w
            self.h = h
            self.health = health
        
        def draw(self):
            pygame.draw.rect(fenetre, BORDEAUX, (self.pos.x, self.pos.y, self.w, self.h))

    class CircleAttack:
        circles=[]
        def __init__(self,x,y):
            self.x = x
            self.y = y
            self.t = 0
            self.r = 0
            self.color = GREEN

        def draw(self):
            pygame.draw.circle(fenetre, self.color, (self.x, self.y), self.r)

        def update(self):
            self.r += 0.4
            self.t += 1
            if self.t == 28:
                self.color = RED
            if self.r >= 12:
                if self in CircleAttack.circles:
                    CircleAttack.circles.remove(self)

    class LineAttack:
        lines=[]
        def __init__(self,ax,ay,ex,ey):
            self.ax = ax
            self.ay = ay
            self.ex = ex
            self.ey = ey
            self.t = 0
            self.w = 0
            self.color = GREEN

        def draw(self):
            pygame.draw.line(fenetre, self.color, (self.ax, self.ay),(self.ex,self.ey), int(self.w))

        def update(self):
            self.w += 0.4
            self.t += 1
            if self.t == 28:
                self.color = RED
            if self.w >= 12:
                if self in LineAttack.lines:
                    LineAttack.lines.remove(self)

    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Blue Squer")
    boss = Ennemy(Vector2(400,300),50,50,600)
    fenetre.fill(WHITE) # Fond blanc (RGB)
   
    # --- 2. Boucle principale ---
    while True:

        compteur+=1 # CHECKS DU LANCEMENT DU PATTERN

        # --- 3. Gestion des events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and compteur_shot == 30:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                dx = mouse_x-rect_x
                dy = mouse_y - rect_y
                projectile.append(Bullet(Vector2(rect_x,rect_y), Vector2(dx,dy).unit, BLACK))
                has_shot = True
                compteur_shot = 0
                
        touches = pygame.key.get_pressed()
        if touches[pygame.K_q] and touches[pygame.K_s] and rect_x > 0 and rect_y < 590:
            rect_x -= speed*0.6
            rect_y += speed*0.6
        elif touches[pygame.K_q] and touches[pygame.K_z] and rect_x > 0 and rect_y > 0:
            rect_x -= speed*0.6 
            rect_y -= speed*0.6
        elif touches[pygame.K_d] and touches[pygame.K_z] and rect_x < 790 and rect_y > 0:
            rect_x += speed*0.6 
            rect_y -= speed*0.6
        elif touches[pygame.K_d] and touches[pygame.K_s] and rect_x < 790 and rect_y < 590:
            rect_x += speed*0.6  
            rect_y += speed*0.6
        elif touches[pygame.K_q] and rect_x > 0:
            rect_x -= speed
        elif touches[pygame.K_d] and rect_x < 790:
            rect_x += speed
        elif touches[pygame.K_s] and rect_y < 590:
            rect_y+= speed
        elif touches[pygame.K_z] and rect_y > 0:
            rect_y-= speed

        
        
        
       
        for obj in projectile:
            obj.pos+= obj.target * obj.velocity
        
        player_direction = Vector2(int(past_rect_x-rect_x),int(past_rect_y-rect_y))
        if compteur%10==0:
            past_rect_x = rect_x
            past_rect_y = rect_y    
        
 
     



        if touches[pygame.K_SPACE]:
            if compteur_dash==300:
                    has_dashed= True
                    compteur_dash = 0
                    speed = 13
        if has_shot:
            compteur_shot +=1
            if compteur_shot == 30:
                has_shot = False

        if has_dashed:
            if compteur_dash>7:
                    speed = 3
        if has_dashed ==True:
            if compteur_dash==300:
                has_dashed=False

        # --- Mise a jour de l'affichage Ceci est généralement causé par un autre dépôt poussé
        fenetre.fill(WHITE)

        boss.draw()
        if alive:
            
            #UI elements
            pygame.draw.rect( fenetre, BLUE ,(rect_x, rect_y, 10, 10) )#player
            pygame.draw.circle(fenetre, WHITE,(rect_x+5, rect_y+5,), 200,1)
            pygame.draw.rect(fenetre, LIGHT_BLUE,(50,50,round(compteur_dash/5),50))#dash bar
            pygame.draw.rect(fenetre, BLACK,(45,45,70,55),5)#dash box
            pygame.draw.rect(fenetre, LIGHT_BRASS,(45,110,30,15))#casing
            pygame.draw.rect(fenetre, BRASS,(45,110,compteur_shot,15))#bullet
            pygame.draw.rect(fenetre, DARK_SALMON,(105,555,boss.health,40))
            pygame.draw.rect(fenetre, SALMON,(100,550,boss.health,40))
            


            # CHECK DE LA PHASE - TRES SENSIBLE - NE PAS CODER AUTRE CHOSE
            if current_pattern == "NO PATTERN":
                print("Y'a pas de pattern là, on choisit")
                if nb_phase == 1:
                    current_pattern = rd.choice(phase_1)
                    while current_pattern == previous_pattern:
                        current_pattern = rd.choice(phase_1)
                    print(current_pattern)
                    patterns[current_pattern]["attaques"] = 0
                    previous_pattern = current_pattern
                elif nb_phase ==2:
                    current_pattern = rd.choice(phase_2)
                    print(current_pattern)
                    patterns[current_pattern]["attaques"] = 0
                    boss_target_x = rd.randint(100,700)
                    boss_target_y = rd.randint(100,500)
                    boss_target_pos = Vector2(boss_target_x, boss_target_y)
                    print(boss_target_pos)



            if patterns[current_pattern]["attaques"] == patterns[current_pattern]["attaques_max"]:
                print("YEP CFINI")
                patterns[current_pattern]["attaques"] = 0
                patterns[current_pattern]["attacking"] = False
                current_color = fenetre.get_at((int(rect_x)+5, int(rect_y+5)))
                patterns[current_pattern]["compteur_attaque"] = 0
                current_pattern = "NO PATTERN"
            
            if current_pattern != "NO PATTERN":
                pass
                #print(patterns[current_pattern]["attaques"])
            
            # FIN DE LA ZONE INTERDITE

            #if compteur%60 == 0 and ispattern_ligne: 
            #    drawline = True
            #if compteur%60==0 and ispattern_cercle:
            #    drawcircle = True
            
            if compteur%60 == 0 and current_pattern != "NO PATTERN":
                draw_what = current_pattern

            if current_pattern != "NO PATTERN" and patterns[current_pattern]["attacking"] == True:
                patterns[current_pattern]["compteur_attaque"]+=1
            if nb_phase == 2:
                boss.pos.x += boss_target_pos.unit.x 
                boss.pos.y += boss_target_pos.unit.y
                dx = boss_target_pos.x - boss.pos.x
                dy = boss_target_pos.y - boss.pos.y

                distance = (dx**2 + dy**2) ** 0.5

                if distance < 2:
                    boss.pos.x = boss_target_pos.x
                    boss.pos.y = boss_target_pos.y
                    quit()
                else:
                    ux = dx / distance
                    uy = dy / distance

                    speed = 2
                    boss.pos.x += ux * speed
                    boss.pos.y += uy * speed
            if has_dashed :
                compteur_dash+=1

            if draw_what == "line":
                if compteur %60 == 0:
                    rdTheta = rd.uniform(0, 2*m.pi)
                    LineAttack.lines.append(LineAttack(rect_x+2000*m.cos(rdTheta),rect_y+2000*m.sin(rdTheta),rect_x+2000*m.cos(rdTheta+m.pi),rect_y+2000*m.sin(rdTheta+m.pi)))
                    patterns["line"]["attaques"]+=1
                    patterns["line"]["attacking"] = True
                for line in LineAttack.lines:
                    line.update()
                    line.draw()
                if patterns["line"]["attaques"] >= patterns["line"]["attaques_max"]:
                        draw_what = "NO PATTERN"
                        patterns["line"]["attacking"] = False
                        patterns["line"]["compteur_attaque"] = 0
                    
            if draw_what == "circle":
                 if compteur % 10 == 0:
                     CircleAttack.circles.append(CircleAttack(rect_x+5+player_direction.x*(-2.6), rect_y+5+player_direction.y*(-2.6)))
                     patterns["circle"]["attacking"] = True
                     patterns["circle"]["attaques"] += 1
                    
                 for circle in CircleAttack.circles:
                    circle.update()
                    circle.draw()
                
                 if patterns["circle"]["attaques"] >= patterns["circle"]["attaques_max"]:
                    draw_what = "NO PATTERN"
                    patterns["circle"]["attacking"] = False
                    patterns["circle"]["compteur_attaque"] = 0

                    CircleAttack.circles.clear()
            if draw_what == "bullets":
                patterns["bullets"]["attacking"] = True
                attaques = patterns["bullets"]["attaques"]
                angles = patterns["bullets"]["angles"]
                if compteur % 20 == 0:
                    if attaques < len(angles):
                        a = angles[attaques]
                        projectile.append(
                            Bullet(Vector2(rect_x + 200*m.cos(a), rect_y + 200*m.sin(a)),Vector2(m.cos(a), m.sin(a)),RED,0))
                        patterns["bullets"]["attaques"] += 1
                    else:
                        draw_what = "NO PATTERN"
                for obj in projectile:
                    if obj.nature == RED:
                        if compteur %20 == 0:
                            obj.velocity = -4
            if draw_what == "line2":
                if compteur %40 == 0:
                    rdTheta = rd.uniform(0, 2*m.pi)
                    LineAttack.lines.append(LineAttack(rect_x+2000*m.cos(rdTheta),rect_y+2000*m.sin(rdTheta),rect_x+2000*m.cos(rdTheta+m.pi),rect_y+2000*m.sin(rdTheta+m.pi)))
                    rdTheta = rd.uniform(0, 2*m.pi)
                    LineAttack.lines.append(LineAttack(rect_x+2000*m.cos(rdTheta),rect_y+2000*m.sin(rdTheta),rect_x+2000*m.cos(rdTheta+m.pi),rect_y+2000*m.sin(rdTheta+m.pi)))
                    patterns["line"]["attaques"]+=1
                    patterns["line"]["attacking"] = True
                for line in LineAttack.lines:
                    line.update()
                    line.draw()
                if patterns["line"]["attaques"] >= patterns["line"]["attaques_max"]:
                        draw_what = "NO PATTERN"
                        patterns["line"]["attacking"] = False
                        patterns["line"]["compteur_attaque"] = 0
            
            
            if boss.health <= 0:
                print("\a")
                print("YOU WON!")
                if sys.platform == "darwin":
                    os.system("say you won")
                    print("\a")
                sleep(0.5)
                print("\a")
                quit()

            for obj in projectile:
                pygame.draw.circle(fenetre, obj.nature,(obj.pos.components), 10,)
                if obj.pos.x<(-100) or obj.pos.x>900 or obj.pos.y<(-600) or obj.pos.y>700:
                    projectile.remove(obj)
                elif 20<obj.pos.x<780 and 20<obj.pos.y<580:  
                    if check_surrounding_pixel_colors(fenetre, obj.pos.x-10,obj.pos.y-10,BORDEAUX,20) and obj.nature == BLACK:
                        projectile.remove(obj)
            if 1<rect_x<799 and 2<rect_y<598:
                if check_surrounding_pixel_colors(fenetre,rect_x,rect_y,RED,10):
                    text_collison=base_font.render("collision", False, (0,0,0))
                    fenetre.blit(text_collison, (400,2))
                    if not immortel:
                        alive = False
            pygame.draw.rect( fenetre, BLUE ,(rect_x,rect_y, 10, 10))
            if check_surrounding_pixel_colors(fenetre,boss.pos.x,boss.pos.y,BLACK,50):
                boss.health-=2
            if boss.health < 500:
                nb_phase = 2
            text_ticks=base_font.render(f"boss_target: {boss_target_x};{boss_target_y}", False, (0,0,0))
            fenetre.blit(text_ticks, (500, 2))
            text_posboss=base_font.render(f"boss_pos: {round(boss.pos.x, 0)};{round(boss.pos.y, 0)}", False, (0,0,0))
            fenetre.blit(text_posboss, (500, 22))
            pygame.draw.rect( fenetre, BLUE ,(rect_x,rect_y, 10, 10))

        else: # Si le joueur n'est pas en vie
            print("\a")
            if sys.platform == "darwin":
                os.system("say game over")
                print("\a")
            sleep(0.5)
            quit()
        pygame.display.flip()           # Rafraichissement de l'ecranssssss
        clock.tick(60)                # Limite a 60 images par seconde
if __name__=="__main__":
    main()










    """Si objet atour du pc (ie epée):
     mouse_x = pygame.mouse.get_pos()[0]
        mouse_y = pygame.mouse.get_pos()[1]
        dx = mouse_x-rect_x
        dy = mouse_y - rect_y
        theta_b = m.atan2(dy,dx)
        print(m.degrees(theta_b))
   
        if event.type == pygame.MOUSEBUTTONDOWN:
            direction = Vector2(dx,dy).unit
        else:
            direction = Vector2(0,0)
            
            
    pygame.draw.circle(fenetre, BLACK,((Vector2((rect_x+5)+25*m.cos(theta_b), (rect_y+5)+25*m.sin(theta_b))+direction*5).components), 10,)
            """