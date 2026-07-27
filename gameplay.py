import pygame, sys, os
from data import DataTree, AlteredDataTree
from pygame import Surface, Rect
from pygame.time import Clock
from pyvectors import Vector2
from time import time
from graphics.color_palette import *
import pygame.display as pygdisplay


class Ability():
    _onActivation = None
    _onDeactivation = None
    _onUpdate = None
    _onPoll = None

    active = False
    enabled = True
    elapsed = 0
    deactivatedAt = 0
    cooldown: float

    data: AlteredDataTree

    def __init__(self, data: dict, onUpdate, onActivation, onDeactivation=None, poll=None, cooldown=1):
        self.data = AlteredDataTree(data)
        self._onActivation = onActivation
        self._onDeactivation = onDeactivation
        self._onUpdate = onUpdate
        self._onPoll = poll
        self.cooldown = cooldown
    
    def poll(self, player):
        now = time()
        onCooldown = (now - self.deactivatedAt) <= self.cooldown
        if self.active or not self.enabled or onCooldown:
            return False

        elif self._onPoll:
            return self._onPoll(self, player)
        
        return True
    
    def activate(self, player):
        if self.poll(player):
            self.elapsed = 0
            self.active = True
            self._onActivation(self, player)

    def deactivate(self, player):
        if self.active:
            self.active = False
            self.deactivatedAt = time()
            
            if self._onDeactivation:
                self._onDeactivation(self, player)

    def update(self, player, deltaTime):
        self.elapsed += deltaTime
        self._onUpdate(self, player, deltaTime)

    def getData(self, key):
        return self.data[key]
    __getattr__=getData
    
    def setData(self, key, value):
        self.data.set(key, value)


class CharacterController():
    sprite: Surface
    data: AlteredDataTree
    
    speed = 3
    health = 100
    state = "idle"
    
    walkDirection = Vector2()
    position = Vector2()

    def __init__(self, sprite: Surface, data: dict=None):
        self.sprite = sprite
        self.data = AlteredDataTree(data)
        self.data.name = "PlayerData"

    def getData(self, key):
        return self.data[key]
    __getattr__=getData

    def setData(self, key, value):
        self.data.set(key, value)


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


def getDash():
    def dashUpdate(self: Ability, player: PlayerController, deltaTime):
        if self.elapsed >= self.length:
            self.deactivate(player)
            self.data.set("dashing", False)
            player.speed = player.charSpeed
        else:
            print(deltaTime)
            player.speed = self.speed
            player.walkDirection = self.direction
            player.state = "walking"
        

    def dashActivation(self: Ability, player):
        self.setData("dashing", True)
        self.setData("direction", player.walkDirection)

    def dashPoll(self: Ability, player):
        return not self.active and self.enabled and player.state == "walking"

    return Ability({
        "speed": 13,
        "length": .2,
        "dashing": False,
        "direction": Vector2(1)
    },
        dashUpdate,
        dashActivation,
        poll=dashPoll,
        cooldown=2
    )

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

    def shieldUpdate(self: Ability, player: CharacterController, deltaTime):
        if self.elapsed >= self.duration:
            self.deactivate(player)
            player.setData("immortal", False)

    def shieldActivation(self: Ability, player: CharacterController):
        print("shield")
        player.setData("immortal", True)

    shieldAbil = Ability(
        {
            "duration": 1,
        },
        shieldUpdate,
        shieldActivation
    )

    # plrSprite = pygame.image.load("sprites\\sprite.png")
    plrSprite = Surface((25, 25))
    plr = CharacterController(
        plrSprite,
        {
            "charSpeed": 5,
            "abilites": [],
            "immortal": False
        }
        )
    plr.position = windowSize/2
    plr.speed = plr.charSpeed
    plr.abilites.append(getDash())
    plr.abilites.append(shieldAbil)

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
            plr.abilites[0].activate(plr)
        if pressedKeys[pygame.K_a]:
            plr.abilites[1].activate(plr)

        ## Update
        for abil in plr.abilites:
            if not abil.active: continue
            abil.update(plr, deltaTime)

        plr.update(deltaTime)
        plr.draw(window)

        pygdisplay.flip()
        mainClock.tick(60)
        lastTick = now

if __name__=="__main__":
    main()
