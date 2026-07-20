import pygame, sys
import pygame.draw as pygdraw
import pygame.display as pygdisplay
import MenuManager as menus
from data import GAME_DATA
from pyvectors import Vector2
from pygame_ui import UILayer
from time import time
from color_palette import *
pygame.init()


def exit():
    pygame.quit()
    sys.exit()
    return False


def processInputs(keyBinds: dict, inputData: dict):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return exit()
        
        if event.type == pygame.KEYDOWN:
            print(event.key)
            bind = keyBinds.get(event.key)
            if bind:
                args = [inputData.get(requiredArg) for requiredArg in bind["requiredData"]]
                if bind["call"](*args) == False:
                    return False

    return True


def main():
    windowSize = Vector2(800, 600)
    window = pygdisplay.set_mode(windowSize.components, pygame.SRCALPHA)
    pygdisplay.set_caption("Blue Squer")

    mainClock = pygame.time.Clock()

    ui_layer = UILayer(window)
    layers = [
        ui_layer
    ]

    keyBinds = {
        27: {
                "call": exit,
                "requiredData": []
        },
        # 97: {
        #     "call": enableFrame,
        #     "requiredData": []
        # }
    }
    inputData = {}

    ## INITIALIZATION
    menus.init(ui_layer, GAME_DATA)


    while True:
        if not processInputs(keyBinds, inputData):
            break

        window.fill(WHITE)

        active_menu = menus.active_menu
        if active_menu is not None:
            GAME_DATA.game_state = "Menu"
            GAME_DATA.gameplay_state = "Paused"
            active_menu.update(active_menu, GAME_DATA)


        if GAME_DATA.gameplay_state != "Paused":
            print("playing")

        for layer in layers:
            layer.render()
            window.blit(layer.surface)

        pygdisplay.flip()
        mainClock.tick(60)

if __name__=="__main__":
    main()
