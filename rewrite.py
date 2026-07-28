import pygame, sys, gameplay
import pygame.draw as pygdraw
import pygame.display as pygdisplay
import MenuManager as menus
from data import GAME_DATA
from pyvectors import Vector2
from pygame_ui import UILayer
from time import time
from graphics.color_palette import *


pygame.init()


class Action():
    key: int
    callback = None
    requiredData = None

    def __init__(self, key, callback, requiredData: list=None):
        self.key, self.callback = key, callback
        if requiredData:
            self.requiredData = requiredData

        setattr(self, "__call__", callback)
        # self.__call__ = callback

    def __call__(self, inputData: dict):
        if self.requiredData:
            requiredData = [inputData[name] for name in self.requiredData]
            self.callback(*requiredData)
        else:
            self.callback()

class ActionGroup():
    actions: dict

    def __init__(self, actions: list=None):
        self.actions = {action.key: action for action in actions}

    def __getitem__(self, key):
        return self.actions.get(key)

    def execute(self, key, inputData: dict):
        action = self[key]
        if not action:
            return
            
        action(inputData)

    def bind(self, action):
        self.actions[action.key] = action


def exit():
    pygame.quit()
    sys.exit()
    return False


def processInputs(actionGroup: ActionGroup, inputData: dict):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return exit()
        
        if event.type == pygame.KEYDOWN:
            print(event.key)
            actionGroup.execute(event.key, inputData)

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

    keyBinds = ActionGroup(
        [
            Action(27, exit),
        ]
    )

    print(keyBinds[27].__call__)

    ## INITIALIZATION
    menus.init(ui_layer, GAME_DATA)
    
    inputData = {"game_data": GAME_DATA}
    lastTick = time()

    sprite = pygame.image.load("sprites\\sprite.png")
    playerController = gameplay.CharacterController(pygame.transform.scale_by(sprite, .2))
    playerController.position = windowSize/2
    playerController.steer(Vector2.one)
    keyBinds.bind(Action(122, lambda: playerController.steer(Vector2(0, 1))))
    keyBinds.bind(Action(113, lambda: playerController.steer(Vector2(1))))
    keyBinds.bind(Action(100, lambda: playerController.steer(Vector2(-1))))
    keyBinds.bind(Action(115, lambda: playerController.steer(Vector2(0, -1))))


    while True:
        now = time()
        deltaTime = lastTick - now

        playerController.walkDirection = Vector2()
        active_menu = menus.active_menu

        if not processInputs(keyBinds, inputData):
            break

        window.fill(WHITE)

        if GAME_DATA.gameplay_state != "Paused":
            if active_menu:
                active_menu.exit()
                active_menu = None
            
            GAME_DATA.set("game_state", "Playing")
            playerController.update(deltaTime)
            playerController.draw(window)

        if active_menu is not None:
            GAME_DATA.set("game_state", "Menu")
            GAME_DATA.gameplay_state = "Paused"
            active_menu.update(active_menu, GAME_DATA)

        for layer in layers:
            layer.render()
            window.blit(layer.surface)

        pygdisplay.flip()
        lastTick = now
        mainClock.tick(60)

if __name__=="__main__":
    main()
