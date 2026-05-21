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
    

    LARGEUR = 800

    HAUTEUR = 600
    
    rect_x = 10
    rect_y = 10


    past_rect_x = 0
    past_rect_y = 0

    boss_target_x = 0
    boss_target_y = 0
    boss_target_pos = Vector2(1,1)
    score_attaques_boss = 0
    player_direction = Vector2(1,1)

    compteur = 0

    nb_phase = 1

    nb_upgrade = 0

    current_pattern = "NO PATTERN"
    previous_pattern = "NO PATTERN"
    draw_what = "NO PATTERN"

    projectile = []

    patterns = {
        "line": {
            "attacking": False,
            "compteur_attaque": 0,
            "attaques": 0,
            "attaques_max": 15,
        },
        "circle": {
            "attacking": False,
            "compteur_attaque": 0,
            "attaques": 0,
            "attaques_max": 30,
        },
        "bullets":{
            "attacking": False,
            "angles": [i*(m.pi/6) for i in range(12)],
            "attaques": 0,
            "attaques_max": 12,
            "compteur_attaque":0
        },
        "line2":{
            "attacking": False,
            "compteur_attaque": 0,
            "attaques": 0,
            "attaques_max": 20,
        },
        "bullets2":{
            "attacking": False,
            "angles": [i*(m.pi/12) for i in range(24)],
            "attaques": 0,
            "attaques_max": 24,
            "compteur_attaque":0
        },
    }

    phase_1 = ["circle", "bullets","line"]
    phase_2 = ["line2", "bullets2"]
    alive = True
    immortel = False
    toggled_upgrade = False
    has_dashed = False # Etat du dash
    compteur_dash = 120 # Cooldown du dash

    has_shot = False
    compteur_shot = 30

    mouse_x = 0
    mouse_y = 0



    class Bullet:
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

    class Upgrade:
        class upgrade1:
            key=pygame.K_b
            def __init__(self,timer):
                self.timer=timer
                self.toggled=True
            def update(self):
                if self.toggled:
                    self.timer+=1
                    if self.timer > 150:
                        self.toggled=False


    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Blue Squer")
    boss = Ennemy(Vector2(400,300),50,50,600)
    fenetre.fill(WHITE)

    restart_game = False

    # --- 2. Start Menu ---
    title_font = pygame.font.SysFont('Comic Sans MS', 64, bold=True)
    big_font   = pygame.font.SysFont('Comic Sans MS', 52, bold=True)
    button_font = pygame.font.SysFont('Comic Sans MS', 28)
    label_font  = pygame.font.SysFont('Comic Sans MS', 20)

    # Character card layout
    CARD_W, CARD_H = 180, 200
    card_gap = 40
    cards_total_w = 2 * CARD_W + card_gap
    card_left_x  = LARGEUR // 2 - cards_total_w // 2
    card_right_x = card_left_x + CARD_W + card_gap
    card_y = HAUTEUR // 2 + 10
    def draw_squer_preview(cx, cy, selected):
        color = LIGHT_BLUE if selected else BLUE
        pygame.draw.rect(fenetre, color, (cx - 18, cy - 18, 36, 36), border_radius=4)

    def draw_lobsta_preview(cx, cy, selected):
        color = LIGHT_BLUE if selected else BLUE
        pygame.draw.ellipse(fenetre, color, (cx - 12, cy - 22, 24, 38))   # body
        pygame.draw.ellipse(fenetre, color, (cx - 30, cy - 10, 18, 12))   # left claw
        pygame.draw.ellipse(fenetre, color, (cx + 12, cy - 10, 18, 12))   # right claw
        pygame.draw.line(fenetre, color, (cx - 6, cy - 22), (cx - 20, cy - 38), 2)  # antennae
        pygame.draw.line(fenetre, color, (cx + 6, cy - 22), (cx + 20, cy - 38), 2)
        pygame.draw.ellipse(fenetre, color, (cx - 8, cy + 16, 16, 10))    # tail

    def draw_animated_bg(offset):
        """Shared animated dot-grid background."""
        fenetre.fill(WHITE)
        spacing = 40
        for gx in range(-spacing, LARGEUR + spacing, spacing):
            for gy in range(-spacing, HAUTEUR + spacing, spacing):
                x = (gx - offset) % (LARGEUR + spacing)
                y = (gy + offset) % (HAUTEUR + spacing)
                pygame.draw.circle(fenetre, (220, 220, 220), (x, y), 2)

    def draw_title():
        """Shared title + underline."""
        title_surf = title_font.render("Blue Squer", True, BLUE)
        title_rect = title_surf.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 130))
        fenetre.blit(title_surf, title_rect)
        pygame.draw.line(fenetre, LIGHT_BLUE,
                         (title_rect.left + 10, title_rect.bottom + 6),
                         (title_rect.right - 10, title_rect.bottom + 6), 3)


    def draw_main_menu(offset):
        draw_animated_bg(offset)
        title_surf = title_font.render("Blue Squer", True, BLUE)
        title_rect = title_surf.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 80))
        fenetre.blit(title_surf, title_rect)
        pygame.draw.line(fenetre, LIGHT_BLUE,
                         (title_rect.left + 10, title_rect.bottom + 6),
                         (title_rect.right - 10, title_rect.bottom + 6), 3)
        mx, my = pygame.mouse.get_pos()
        btn_w, btn_h = 160, 52
        btn_rect = pygame.Rect(LARGEUR // 2 - btn_w // 2, HAUTEUR // 2 + 20, btn_w, btn_h)
        hovered = btn_rect.collidepoint(mx, my)
        btn_color = LIGHT_BLUE if hovered else BLUE
        pygame.draw.rect(fenetre, btn_color, btn_rect, border_radius=6)
        pygame.draw.rect(fenetre, BLACK, btn_rect, 2, border_radius=6)
        btn_text = button_font.render("PLAY", True, WHITE)
        fenetre.blit(btn_text, btn_text.get_rect(center=btn_rect.center))
        return btn_rect

    def draw_start_menu(offset, selected_char):
        draw_animated_bg(offset)
        draw_title()

        pick_surf = label_font.render("choose your character", True, (160, 160, 160))
        fenetre.blit(pick_surf, pick_surf.get_rect(center=(LARGEUR // 2, card_y - 22)))

        mx, my = pygame.mouse.get_pos()

        # --- Left card: Blue Squer ---
        left_rect = pygame.Rect(card_left_x, card_y, CARD_W, CARD_H)
        squer_sel = selected_char == "Blue Squer"
        squer_hov = left_rect.collidepoint(mx, my)
        border_col_l = BLUE if squer_sel else (BLACK if squer_hov else (200, 200, 200))
        pygame.draw.rect(fenetre, WHITE, left_rect, border_radius=8)
        pygame.draw.rect(fenetre, border_col_l, left_rect, 3 if (squer_sel or squer_hov) else 2, border_radius=8)
        draw_squer_preview(card_left_x + CARD_W // 2, card_y + 80, squer_sel)
        name_l = button_font.render("Blue Squer", True, BLUE if squer_sel else BLACK)
        fenetre.blit(name_l, name_l.get_rect(center=(card_left_x + CARD_W // 2, card_y + CARD_H - 35)))
        if squer_sel:
            tick_l = label_font.render("✓ selected", True, BLUE)
            fenetre.blit(tick_l, tick_l.get_rect(center=(card_left_x + CARD_W // 2, card_y + CARD_H - 12)))

        # --- Right card: Blue Lobsta ---
        right_rect = pygame.Rect(card_right_x, card_y, CARD_W, CARD_H)
        lobsta_sel = selected_char == "Blue Lobsta"
        lobsta_hov = right_rect.collidepoint(mx, my)
        border_col_r = BLUE if lobsta_sel else (BLACK if lobsta_hov else (200, 200, 200))
        pygame.draw.rect(fenetre, WHITE, right_rect, border_radius=8)
        pygame.draw.rect(fenetre, border_col_r, right_rect, 3 if (lobsta_sel or lobsta_hov) else 2, border_radius=8)
        draw_lobsta_preview(card_right_x + CARD_W // 2, card_y + 80, lobsta_sel)
        name_r = button_font.render("Blue Lobsta", True, BLUE if lobsta_sel else BLACK)
        fenetre.blit(name_r, name_r.get_rect(center=(card_right_x + CARD_W // 2, card_y + CARD_H - 35)))
        if lobsta_sel:
            tick_r = label_font.render("✓ selected", True, BLUE)
            fenetre.blit(tick_r, tick_r.get_rect(center=(card_right_x + CARD_W // 2, card_y + CARD_H - 12)))

        # --- Next button (greyed out until a character is picked) ---
        btn_w, btn_h = 160, 52
        btn_rect = pygame.Rect(LARGEUR // 2 - btn_w // 2, card_y + CARD_H + 28, btn_w, btn_h)
        btn_active = selected_char != "NONE"
        btn_hov = btn_rect.collidepoint(mx, my) and btn_active
        btn_color = (LIGHT_BLUE if btn_hov else BLUE) if btn_active else (200, 200, 200)
        txt_color = WHITE if btn_active else (160, 160, 160)
        brd_color = BLACK if btn_active else (180, 180, 180)
        pygame.draw.rect(fenetre, btn_color, btn_rect, border_radius=6)
        pygame.draw.rect(fenetre, brd_color, btn_rect, 2, border_radius=6)
        btn_text = button_font.render("NEXT  ›", True, txt_color)
        fenetre.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

        return left_rect, right_rect, btn_rect

    # --- Upgrade selection menu ---
    UPD_W, UPD_H = 160, 80
    upd_gap = 30
    upd_total_w = 3 * UPD_W + 2 * upd_gap
    upd_start_x = LARGEUR // 2 - upd_total_w // 2
    upd_y = HAUTEUR // 2 + 20

    def draw_upgrade_menu(offset, selected_upd):
        draw_animated_bg(offset)
        draw_title()

        pick_surf = label_font.render("choose your upgrade", True, (160, 160, 160))
        fenetre.blit(pick_surf, pick_surf.get_rect(center=(LARGEUR // 2, upd_y - 22)))

        mx, my = pygame.mouse.get_pos()
        upd_rects = []

        for i, label in enumerate(["Upgrade 1", "Upgrade 2", "Upgrade 3"]):
            rx = upd_start_x + i * (UPD_W + upd_gap)
            rect = pygame.Rect(rx, upd_y, UPD_W, UPD_H)
            upd_rects.append(rect)

            sel = selected_upd == i + 1
            hov = rect.collidepoint(mx, my)
            border_col = BLUE if sel else (BLACK if hov else (200, 200, 200))
            pygame.draw.rect(fenetre, WHITE, rect, border_radius=8)
            pygame.draw.rect(fenetre, border_col, rect, 3 if (sel or hov) else 2, border_radius=8)

            lbl_surf = button_font.render(label, True, BLUE if sel else BLACK)
            fenetre.blit(lbl_surf, lbl_surf.get_rect(center=rect.center))

            if sel:
                tick = label_font.render("✓", True, BLUE)
                fenetre.blit(tick, tick.get_rect(center=(rect.centerx, rect.bottom - 14)))

        # Play button
        btn_w, btn_h = 160, 52
        btn_rect = pygame.Rect(LARGEUR // 2 - btn_w // 2, upd_y + UPD_H + 30, btn_w, btn_h)
        btn_active = selected_upd != 0
        btn_hov = btn_rect.collidepoint(mx, my) and btn_active
        btn_color = (LIGHT_BLUE if btn_hov else BLUE) if btn_active else (200, 200, 200)
        txt_color = WHITE if btn_active else (160, 160, 160)
        brd_color = BLACK if btn_active else (180, 180, 180)
        pygame.draw.rect(fenetre, btn_color, btn_rect, border_radius=6)
        pygame.draw.rect(fenetre, brd_color, btn_rect, 2, border_radius=6)
        btn_text = button_font.render("PLAY", True, txt_color)
        fenetre.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

        return upd_rects, btn_rect

    # --- End screens ---
    def draw_game_over_screen(offset, score):
        """Game Over / 'Git Gud!' screen — red-tinted dot grid, same style as menus."""
        # Animated background, red tint
        fenetre.fill(WHITE)
        spacing = 40
        for gx in range(-spacing, LARGEUR + spacing, spacing):
            for gy in range(-spacing, HAUTEUR + spacing, spacing):
                x = (gx - offset) % (LARGEUR + spacing)
                y = (gy + offset) % (HAUTEUR + spacing)
                pygame.draw.circle(fenetre, (255, 210, 210), (x, y), 2)

        # "Git Gud!" title
        git_surf = big_font.render("Git Gud!", True, RED)
        git_rect = git_surf.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 110))
        fenetre.blit(git_surf, git_rect)
        pygame.draw.line(fenetre, SALMON,
                         (git_rect.left + 10, git_rect.bottom + 6),
                         (git_rect.right - 10, git_rect.bottom + 6), 3)

        # Score
        score_label = label_font.render("Score", True, (160, 160, 160))
        fenetre.blit(score_label, score_label.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 28)))
        score_surf = title_font.render(str(score), True, RED)
        fenetre.blit(score_surf, score_surf.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 30)))

        mx, my = pygame.mouse.get_pos()

        # Retry button
        btn_w, btn_h = 200, 52
        retry_rect = pygame.Rect(LARGEUR // 2 - btn_w // 2 - 110, HAUTEUR // 2 + 120, btn_w, btn_h)
        retry_hov = retry_rect.collidepoint(mx, my)
        pygame.draw.rect(fenetre, SALMON if retry_hov else RED, retry_rect, border_radius=6)
        pygame.draw.rect(fenetre, BLACK, retry_rect, 2, border_radius=6)
        retry_text = button_font.render("PLAY AGAIN", True, WHITE)
        fenetre.blit(retry_text, retry_text.get_rect(center=retry_rect.center))

        # Quit button
        quit_rect = pygame.Rect(LARGEUR // 2 - btn_w // 2 + 110, HAUTEUR // 2 + 120, btn_w, btn_h)
        quit_hov = quit_rect.collidepoint(mx, my)
        pygame.draw.rect(fenetre, (200, 200, 200) if quit_hov else WHITE, quit_rect, border_radius=6)
        pygame.draw.rect(fenetre, BLACK, quit_rect, 2, border_radius=6)
        quit_text = button_font.render("QUIT", True, BLACK)
        fenetre.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        return retry_rect, quit_rect

    def draw_win_screen(offset, score):
        """Victory screen — blue dot grid."""
        fenetre.fill(WHITE)
        spacing = 40
        for gx in range(-spacing, LARGEUR + spacing, spacing):
            for gy in range(-spacing, HAUTEUR + spacing, spacing):
                x = (gx - offset) % (LARGEUR + spacing)
                y = (gy + offset) % (HAUTEUR + spacing)
                pygame.draw.circle(fenetre, (200, 230, 255), (x, y), 2)

        # "You Won!" title
        win_surf = big_font.render("You Won!", True, BLUE)
        win_rect = win_surf.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 110))
        fenetre.blit(win_surf, win_rect)
        pygame.draw.line(fenetre, LIGHT_BLUE,
                         (win_rect.left + 10, win_rect.bottom + 6),
                         (win_rect.right - 10, win_rect.bottom + 6), 3)

        # Score
        score_label = label_font.render("your score", True, (160, 160, 160))
        fenetre.blit(score_label, score_label.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 28)))
        score_surf = title_font.render(str(score), True, BLUE)
        fenetre.blit(score_surf, score_surf.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 + 30)))

        mx, my = pygame.mouse.get_pos()

        # Play again button
        btn_w, btn_h = 200, 52
        again_rect = pygame.Rect(LARGEUR // 2 - btn_w // 2 - 110, HAUTEUR // 2 + 120, btn_w, btn_h)
        again_hov = again_rect.collidepoint(mx, my)
        pygame.draw.rect(fenetre, LIGHT_BLUE if again_hov else BLUE, again_rect, border_radius=6)
        pygame.draw.rect(fenetre, BLACK, again_rect, 2, border_radius=6)
        again_text = button_font.render("↺  PLAY AGAIN", True, WHITE)
        fenetre.blit(again_text, again_text.get_rect(center=again_rect.center))

        # Quit button
        quit_rect = pygame.Rect(LARGEUR // 2 - btn_w // 2 + 110, HAUTEUR // 2 + 120, btn_w, btn_h)
        quit_hov = quit_rect.collidepoint(mx, my)
        pygame.draw.rect(fenetre, (200, 200, 200) if quit_hov else WHITE, quit_rect, border_radius=6)
        pygame.draw.rect(fenetre, BLACK, quit_rect, 2, border_radius=6)
        quit_text = button_font.render("QUIT", True, BLACK)
        fenetre.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        return again_rect, quit_rect

    menu_offset = 0
    player_character = "NONE"

    # -------------------------------------------------------
    # OUTER LOOP — main menu → character → upgrade → game
    # On death, loops back to character selection menu
    # -------------------------------------------------------
    show_main_menu = True
    restart_game = False

    while True:

        # --- Menu 1: Main menu ---
        if show_main_menu:
            in_main = True
            while in_main:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        btn_rect = draw_main_menu(menu_offset)
                        if btn_rect.collidepoint(event.pos):
                            in_main = False
                draw_main_menu(menu_offset)
                menu_offset = (menu_offset + 1) % 40
                pygame.display.flip()
                clock.tick(60)
            show_main_menu = False

        # --- Menu 2: Character selection ---
        if not restart_game:
            selected_char = "NONE"
            in_char = True

            while in_char:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        left_rect, right_rect, btn_rect = draw_start_menu(menu_offset, selected_char)
                        if left_rect.collidepoint(event.pos):
                            selected_char = "Blue Squer"
                        elif right_rect.collidepoint(event.pos):
                            selected_char = "Blue Lobsta"
                        elif btn_rect.collidepoint(event.pos) and selected_char != "NONE":
                            player_character = selected_char
                            in_char = False
                draw_start_menu(menu_offset, selected_char)
                menu_offset = (menu_offset + 1) % 40
                pygame.display.flip()
                clock.tick(60)
            player_character = selected_char

        # --- Menu 3: Upgrade selection ---
        # --- Menu 3: Upgrade selection ---
        if not restart_game:
            selected_upd = 0
            in_upd = True

            while in_upd:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        upd_rects, btn_rect = draw_upgrade_menu(menu_offset, selected_upd)
                        for i, rect in enumerate(upd_rects):
                            if rect.collidepoint(event.pos):
                                selected_upd = i + 1
                        if btn_rect.collidepoint(event.pos) and selected_upd != 0:
                            nb_upgrade = selected_upd
                            in_upd = False
                draw_upgrade_menu(menu_offset, selected_upd)
                menu_offset = (menu_offset + 1) % 40
                pygame.display.flip()
                clock.tick(60)
            nb_upgrade = selected_upd

        # --- Reset game state before each run ---
        rect_x = 10
        rect_y = 10
        past_rect_x = 0
        past_rect_y = 0
        boss_target_x = 0
        boss_target_y = 0
        boss_target_pos = Vector2(1,1)
        score_attaques_boss = 0
        player_direction = Vector2(1,1)
        compteur = 0
        nb_phase = 1
        player_color=BLUE
        current_pattern = "NO PATTERN"
        previous_pattern = "NO PATTERN"
        draw_what = "NO PATTERN"
        projectile.clear()
        LineAttack.lines.clear()
        CircleAttack.circles.clear()
        for p in patterns.values():
            p["attacking"] = False
            p["compteur_attaque"] = 0
            p["attaques"] = 0
        if "angles" in patterns["bullets"]:
            patterns["bullets"]["angles"] = [i*(m.pi/6) for i in range(12)]
        alive = True
        immortel = False
        has_dashed = False
        compteur_dash = 120
        has_shot = False
        compteur_shot = 30
        speed = 3
        boss = Ennemy(Vector2(400,300),50,50,600)

        # --- 3. Boucle principale ---
        game_running = True
        end_state = None   # "death" or "win"
    
        while game_running:

            compteur += 1

            # --- Gestion des events ---
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
                rect_y += speed
            elif touches[pygame.K_z] and rect_y > 0:
                rect_y -= speed

            if touches[pygame.K_SPACE]:
                if compteur_dash == 120:
                    has_dashed = True
                    compteur_dash = 0
                    speed = 13
                    immortel = True
            if touches[Upgrade.upgrade1.key] and nb_upgrade == 1:    #triggers boss blindness
                toggled_upgrade = Upgrade.upgrade1(timer=compteur)
                player_color = (204, 202, 232)

            for obj in projectile:
                obj.pos += obj.target * obj.velocity

            player_direction = Vector2(int(past_rect_x-rect_x),int(past_rect_y-rect_y))
            if compteur % 10 == 0:
                past_rect_x = rect_x
                past_rect_y = rect_y

            if has_shot:
                compteur_shot += 1
                if compteur_shot == 30:
                    has_shot = False

            if has_dashed:
                if compteur_dash > 7:
                    speed = 3
                    immortel = False
            if has_dashed == True:
                if compteur_dash == 120:
                    has_dashed = False

            fenetre.fill(WHITE)

            boss.draw()

            if alive:

                pygame.draw.rect(fenetre, BLUE, (rect_x, rect_y, 10, 10))
                pygame.draw.circle(fenetre, WHITE, (rect_x+5, rect_y+5,), 200, 1)
                pygame.draw.rect(fenetre, LIGHT_BLUE, (rect_x-3.5,rect_y+12,round(compteur_dash/8),6))  # dash bar
                pygame.draw.rect(fenetre, BLACK, (rect_x-3.5,rect_y+12,17,7), 2)  # dash box
                pygame.draw.rect(fenetre, LIGHT_BRASS, (45,110,30,15))  # casing
                pygame.draw.rect(fenetre, BRASS, (45,110,compteur_shot,15))  # bullet
                pygame.draw.rect(fenetre, DARK_SALMON, (105,555,boss.health,40))
                pygame.draw.rect(fenetre, SALMON, (100,550,boss.health,40))
                if nb_phase !=3:
                    if current_pattern == "NO PATTERN":
                        print("Y'a pas de pattern là, on choisit")
                        if nb_phase == 1:
                            current_pattern = rd.choice(phase_1)
                            while current_pattern == previous_pattern:
                                current_pattern = rd.choice(phase_1)
                            print(current_pattern)
                            patterns[current_pattern]["attaques"] = 0
                            previous_pattern = current_pattern
                        elif nb_phase == 2:
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

                    if compteur % 60 == 0 and current_pattern != "NO PATTERN":
                        draw_what = current_pattern

                    if current_pattern != "NO PATTERN" and patterns[current_pattern]["attacking"] == True:
                        patterns[current_pattern]["compteur_attaque"] += 1
                else:
                    if compteur % round(boss.health/10) == 0:
                        for i in range(12):
                            CircleAttack.circles.append(CircleAttack(rd.randint(10,790), rd.randint(10,590)))
                    if compteur % 6 == 0:
                        projectile.append(Bullet(Vector2(boss.pos.x+25,boss.pos.y+25), Vector2(boss.pos.x+25-rect_x+5+rd.randint(-100,100),boss.pos.y+25-rect_y+5+rd.randint(-100,100)).unit, RED,-4))
                    for circle in CircleAttack.circles:
                        circle.update()
                        circle.draw()
                if nb_phase == 2:
                    boss.pos.x += boss_target_pos.unit.x
                    boss.pos.y += boss_target_pos.unit.y
                    dx = boss_target_pos.x - boss.pos.x
                    dy = boss_target_pos.y - boss.pos.y
                    if compteur % 60 == 0:
                        projectile.append(Bullet(Vector2(boss.pos.x+25,boss.pos.y+25), Vector2(boss.pos.x+25-rect_x+5,boss.pos.y+25-rect_y+5).unit, RED,-4))
                    if compteur % 20 == 0:
                        CircleAttack.circles.append(CircleAttack(rect_x+5, rect_y+5))
                    for circle in CircleAttack.circles:
                        circle.update()
                        circle.draw()
                    distance = (dx**2 + dy**2) ** 0.5
                    if distance < 2:
                        boss.pos.x = boss_target_pos.x
                        boss.pos.y = boss_target_pos.y
                        boss_target_x = rd.randint(100,700)
                        boss_target_y = rd.randint(100,500)
                        boss_target_pos = Vector2(boss_target_x, boss_target_y)
                    else:
                        ux = dx / distance
                        uy = dy / distance
                        boss.pos.x += ux * 3
                        boss.pos.y += uy * 3

                if has_dashed:
                    compteur_dash += 1

                if draw_what == "line":
                    if compteur % 60 == 0:
                        rdTheta = rd.uniform(0, 2*m.pi)
                        LineAttack.lines.append(LineAttack(rect_x+2000*m.cos(rdTheta),rect_y+2000*m.sin(rdTheta),rect_x+2000*m.cos(rdTheta+m.pi),rect_y+2000*m.sin(rdTheta+m.pi)))
                        patterns["line"]["attaques"] += 1
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
                            projectile.append(Bullet(Vector2(rect_x + 200*m.cos(a), rect_y + 200*m.sin(a)),Vector2(m.cos(a), m.sin(a)),RED,0))
                            patterns["bullets"]["attaques"] += 1
                        else:
                            draw_what = "NO PATTERN"
                    for obj in projectile:
                        if obj.nature == RED:
                            if compteur % 20 == 0:
                                obj.velocity = -4
                if draw_what == "bullets2":
                    patterns["bullets2"]["attacking"] = True
                    attaques = patterns["bullets2"]["attaques"]
                    angles = patterns["bullets2"]["angles"]
                    if compteur % 20 == 0:
                        if attaques < len(angles):
                            a = angles[attaques]
                            projectile.append(Bullet(Vector2(rect_x + 200*m.cos(a), rect_y + 200*m.sin(a)),Vector2(m.cos(a), m.sin(a)),RED,0))
                            projectile.append(Bullet(Vector2(rect_x + 200*m.cos(-a), rect_y + 200*m.sin(-a)),Vector2(m.cos(-a), m.sin(-a)),RED,0))
                            patterns["bullets2"]["attaques"] += 1
                        else:
                            draw_what = "NO PATTERN"
                    for obj in projectile:
                        if obj.nature == RED:
                            if compteur % 20 == 0:
                                obj.velocity = -4

                if draw_what == "line2":
                    if compteur % 40 == 0:
                        rdTheta = rd.uniform(0, 2*m.pi)
                        LineAttack.lines.append(LineAttack(rect_x+2000*m.cos(rdTheta),rect_y+2000*m.sin(rdTheta),rect_x+2000*m.cos(rdTheta+m.pi),rect_y+2000*m.sin(rdTheta+m.pi)))
                        rdTheta = rd.uniform(0, 2*m.pi)
                        LineAttack.lines.append(LineAttack(rect_x+2000*m.cos(rdTheta),rect_y+2000*m.sin(rdTheta),rect_x+2000*m.cos(rdTheta+m.pi),rect_y+2000*m.sin(rdTheta+m.pi)))
                        patterns["line"]["attaques"] += 1
                        patterns["line2"]["attacking"] = True
                    for line in LineAttack.lines:
                        line.update()
                        line.draw()
                    if patterns["line2"]["attaques"] >= patterns["line2"]["attaques_max"]:
                        draw_what = "NO PATTERN"
                        patterns["line2"]["attacking"] = False
                        patterns["line2"]["compteur_attaque"] = 0

                if boss.health <= 0:
                    end_state = "win"
                    game_running = False

                if toggled_upgrade is not False:
                    if toggled_upgrade.toggled is True:
                        toggled_upgrade.update()
                    if toggled_upgrade.timer >= 150:
                        player_color=BLUE

                for obj in projectile:
                    pygame.draw.circle(fenetre, obj.nature,(obj.pos.components), 10,)
                    if obj.pos.x<(-100) or obj.pos.x>900 or obj.pos.y<(-600) or obj.pos.y>700:
                        projectile.remove(obj)
                    elif 20<obj.pos.x<780 and 20<obj.pos.y<580:
                        if check_surrounding_pixel_colors(fenetre, obj.pos.x-10,obj.pos.y-10,BORDEAUX,20) and obj.nature == BLACK:
                            projectile.remove(obj)

                if 0<rect_x+5<800 and 0<rect_y+5<600:
                    if check_surrounding_pixel_colors(fenetre,rect_x+5,rect_y+5,RED,10):
                        if not immortel:
                            alive = False

                pygame.draw.rect(fenetre, BLUE, (rect_x, rect_y, 10, 10))

                if check_surrounding_pixel_colors(fenetre,boss.pos.x,boss.pos.y,BLACK,50):
                    boss.health -= 4
                    score_attaques_boss += 100

                if boss.health < 500:
                    nb_phase = 2
                if boss.health < 300:
                    nb_phase = 3
                    boss_target_x = 400
                    boss_target_y = 300
                    boss_target_pos = Vector2(boss_target_x, boss_target_y)

                text_score=base_font.render(f"Score: {round(compteur/3)+score_attaques_boss}", False, (0,0,0))
                fenetre.blit(text_score, (600, 2))
                pygame.draw.rect(fenetre, player_color, (rect_x, rect_y, 10, 10))

            else:
                end_state = "death"
                game_running = False

            pygame.display.flip()
            clock.tick(60)

        # --- End screen ---
        final_score = round(compteur / 3) + score_attaques_boss
        end_offset = 0
        in_end = True
        while in_end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if end_state == "death":
                        retry_rect, quit_rect = draw_game_over_screen(end_offset, final_score)
                        if retry_rect.collidepoint(event.pos):
                            restart_game = True
                            in_end = False
                        elif quit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                    else:
                        again_rect, quit_rect = draw_win_screen(end_offset, final_score)
                        if again_rect.collidepoint(event.pos):
                            restart_game = True
                            in_end = False
                        elif quit_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

            if end_state == "death":
                draw_game_over_screen(end_offset, final_score)
            else:
                draw_win_screen(end_offset, final_score)

            end_offset = (end_offset + 1) % 40
            pygame.display.flip()
            clock.tick(60)
        show_main_menu = False

        # After end screen, loop back to character selection (show_main_menu stays False)

if __name__=="__main__":
    main()