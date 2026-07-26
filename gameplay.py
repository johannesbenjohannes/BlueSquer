import pygame, sys, os
from pygame import Surface, Rect, Clock
import pygame.display as pygdisplay
from pyvectors import Vector2
from time import time
from graphics.color_palette import *
from data import DataTree, AlteredDataTree


class Ability():
    _onActivation = None
    _onDeactivation = None
    _onUpdate = None

    active = False
    enabled = True

    data: AlteredDataTree

    def __init__(self, data: dict, onUpdate, onActivation, onDeactivation=None):
        self.data = AlteredDataTree(data)
        self._onActivation = onActivation
        self._onDeactivation = onDeactivation
        self._onUpdate = onUpdate

    def activate(self, player):
        if not self.active and self.enabled:
            self.active = True
            self._onActivation(self, player)

    def deactivate(self, player):
        print("deactivated")
        self.active = False
        if self._onDeactivation:
            self._onDeactivation(self, player)

    def update(self, player):
        self._onUpdate(self, player)

    def getData(self, name):
        return self.data[name]

    __getattr__=getData


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
    data: AlteredDataTree

    def __init__(self, sprite, data: dict=None):
        CharacterController.__init__(self, sprite)
        self.data = AlteredDataTree(data or {})
        self.data.name = "PlayerData"

    def getData(self, name):
        return self.data[name]
    __getattr__=getData


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

    def dashUpdate(self: Ability, player: PlayerController):
        self.data.set("tick", self.tick + 1)
        
        if self.data.tick >= 15:
            self.deactivate(player)
        elif self.tick >= 7:
            player.speed = player.charSpeed
        else:
            player.speed = self.dashSpeed
        

    def dashActivation(self: Ability, player):
        print("activated dash")
        self.data.set("tick", 0)

    dashAbil = Ability({
        "tick": 0,
        "dashSpeed": 20
    },
        dashUpdate,
        dashActivation
    )

    # plrSprite = pygame.image.load("sprites\\sprite.png")
    plrSprite = Surface((25, 25))
    plr = PlayerController(
        plrSprite,
        {
            "charSpeed": 5
        }
        )
    plr.position = windowSize/2
    plr.speed = plr.charSpeed

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
        plr.stop()
        
        if pressedKeys[pygame.K_z]:
            plr.step(Vector2(0, -1))
        if pressedKeys[pygame.K_q]:
            plr.step(Vector2(-1))
        if pressedKeys[pygame.K_d]:
            plr.step(Vector2(1))
        if pressedKeys[pygame.K_s]:
            plr.step(Vector2(0, 1))

        if pressedKeys[pygame.K_SPACE]:
            dashAbil.activate(plr)

        ## Update
        if dashAbil.active:
            dashAbil.update(plr)

        plr.update(deltaTime)
        plr.draw(window)

        pygdisplay.flip()
        mainClock.tick(60)
        lastTick = now

if __name__=="__main__":
    main()
