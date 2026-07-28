import pygame, sys
from pygame.time import Clock
from pygame import Surface

pygame.init()

# def draw_sprite(surface: Surface):


def main():
    size = WIDTH, HEIGHT = 800, 800
    window = pygame.display.set_mode(size)
    window.set_alpha(255)
    clock = Clock()

    color = (255, 0, 0)
    cx = 35
    cy = 35
    spriteSize = 800/70

    sprite = Surface(size, pygame.SRCALPHA)
    sprite.set_alpha(255)
    pygame.draw.ellipse
    pygame.draw.ellipse(sprite, color, ((cx - 12)*spriteSize, (cy - 18)*spriteSize, (24)*spriteSize, (38)*spriteSize))   # body
    pygame.draw.ellipse(sprite, color, ((cx - 30)*spriteSize, (cy - 6)*spriteSize, (18)*spriteSize, (12)*spriteSize))   # left claw
    pygame.draw.ellipse(sprite, color, ((cx + 12)*spriteSize, (cy - 6)*spriteSize, (18)*spriteSize, (12)*spriteSize))   # right claw
    pygame.draw.line(sprite, color, (WIDTH/2-25, HEIGHT/2-150), (WIDTH/2-200, HEIGHT/2-500), 15)
    pygame.draw.line(sprite, color, (WIDTH/2+22, HEIGHT/2-150), (WIDTH/2+200, HEIGHT/2-500), 15)
    # pygame.draw.line(sprite, color, ((cx - 6)*spriteSize, (cy - 22)*spriteSize), ((cx - 20)*spriteSize, (cy - 38)*spriteSize), 30)  # antennae
    # pygame.draw.line(sprite, color, ((cx + 6)*spriteSize, (cy - 22)*spriteSize), ((cx + 20)*spriteSize, (cy - 38)*spriteSize), 30)
    pygame.draw.ellipse(sprite, color, ((cx - 8)*spriteSize, (cy + 20)*spriteSize, (16)*spriteSize, (10)*spriteSize))    # tail

    pygame.image.save(sprite, "sprites\\lobsta.png")

    firstPass = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill((0, 0, 0, 255))

        window.blit(sprite, (0, 0))

        if firstPass:
            firstPass = False
            # pygame.image.save(window, "sprites\\lobsta.png")

        pygame.display.flip()
        clock.tick(60)

if __name__=="__main__":
    main()
