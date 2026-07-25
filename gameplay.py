import pygame, sys, os
from pygame import Surface, Rect, Clock
import pygame.display as pygdisplay
from pyvectors import Vector2
from time import time
from graphics.color_palette import *
from data import DataTree


class Ability():
    _onActivation = None
    _onDeactivation = None
    _onUpdate = None

    active = False
    enabled = True

    data: dict
    modifiedData: dict

    def __init__(self, data: dict, onUpdate, onActivation, onDeactivation):
        self.data = data
        self.modifiedData = {}

    def getData(self, name):
        modified = self.modifiedData.get(name)
        return modified or self.data[name]
    __getattr__ = getData

    def getBaseData(self, name):
        return self.data[name]

    def setData(self, name, value):
        self.data[name] = value

    def modifyData(self, name, value):
        originalData = self.data[name]
        if originalData == value:
            return

        self.modifiedData[name] = value
        
    def dataModified(self, name):
        return self.modifiedData.get(name) is not None

    def activate(self, player, gameData):
        if not self.active and self.enabled:
            self.active = True
            self._onActivation(self, player, gameData)

    def deactivate(self, player, gameData):
        self.active = False
        if self._onDeactivation:
            self._onDeactivation(self, player, gameData)

    def update(self, player, gameData):
        self._onUpdate(self, player, gameData)


class CharacterController():
    sprite: Surface
    speed = 3
    health = 100
    walkDirection = Vector2()
    
    state = "idle"

    position = Vector2()

    def __init__(self, sprite: Surface):
        self.sprite = sprite


    ## Movement
    def stop(self):
        self.walkDirection = Vector2()
        self.state = "idle"

    def steer(self, direction):
        direction += self.walkDirection

        if direction.magnitude == 0:
            self.walkDirection = direction
            return

        self.walkDirection = direction.unit()

    def step(self, direction: Vector2):
        self.steer(direction)
        
        if not self.walkDirection:
            self.state = "idle"
        else:
            self.state = "walking"

    def walk(self, direction: Vector2):
        if not direction: return

        self.stop()
        self.walkDirection = direction
        self.state = "walking"

    
    ## State
    def damage(self, damages):
        if self.state == "dead": return

        self.health -= damages
        
        if self.health <= 0:
            self.state = "dead"
            self.health = 0

    ## Update
    def update(self, deltaTime):
        if self.state == "dead":
            return

        if self.state == "walking":
            self.position += self.walkDirection*self.speed

    def draw(self, window: Surface):
        spriteSize = Vector2(self.sprite.get_size())
        drawPos = self.position - spriteSize/2
        
        return window.blit(self.sprite, drawPos.components)


class PlayerController(CharacterController):
    username = "Player"

    abilites: list
    data: DataTree

    

    def __init__(self, sprite, data: DataTree=None):
        CharacterController.__init__(self, sprite)
        self.data = data or DataTree()
        self.username = username

    def __getattr__(self, attr):
        return self.data[attr]


def exit():
    pygame.quit()
    sys.exit()
    return False


def main():
    pygame.init()
    mainClock = Clock()

    windowSize = Vector2(800, 800)
    window = pygdisplay.set_mode(windowSize)

    lastTick = time()
    startTick = lastTick

    def dashUpdate(self, player, gameData):
        self.data["tick"] += 1
        if 

    def dashActivation(self, player, gameData):
        pass

    dashAbil = Ability({
        "tick": 0
    }, 
        dashUpdate,

    )

    # plrSprite = pygame.image.load("sprites\\sprite.png")
    plrSprite = Surface((100, 100))
    playerController = CharacterController(pygame.transform.scale_by(plrSprite, .2))
    playerController.position = windowSize/2

    while True:
        now = time()
        deltaTime = now - lastTick
        elapsed = now - startTick
        window.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                # przint(event.unicode , event.key)
                if event.key == 27:
                    exit()

        pressedKeys = pygame.key.get_pressed()
        moving = False

        playerController.stop()
        
        if pressedKeys[pygame.K_z]:
            playerController.step(Vector2(0, -1))
            moving = True
        if pressedKeys[pygame.K_q]:
            playerController.step(Vector2(-1))
            moving = True
        if pressedKeys[pygame.K_d]:
            playerController.step(Vector2(1))
            moving = True
        if pressedKeys[pygame.K_s]:
            playerController.step(Vector2(0, 1))
            moving = True
        
        if elapsed > 1:
            playerController.damage(1)

        ## Update
        playerController.update(deltaTime)
        playerController.draw(window)

        pygdisplay.flip()
        mainClock.tick(60)
        lastTick = now

if __name__=="__main__":
    main()
