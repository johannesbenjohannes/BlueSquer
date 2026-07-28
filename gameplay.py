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


class Sprite():
    image: Surface
    anchorPoint: Vector2
    size: Vector2

    def __init__(self, sprite: Surface, spriteDownscale: int=1):
        if spriteDownscale !=  1:
            self.image = pygame.transform.scale_by(sprite, spriteDownscale)
        else:
            self.image = sprite
        self.size = Vector2(self.image.get_size())
        self.anchorPoint = Vector2(0.5, 0.5)

    def draw(self, surface: Surface, at: Vector2):
        imagePos = at - self.size * self.anchorPoint
        surface.blit(self.image, imagePos.components)


class GameObject():
    name = "object"

    sprite: Sprite

    acceleration = Vector2()
    velocity = Vector2()
    position = Vector2()

    def __init__(self, sprite: Sprite):
        self.sprite = sprite

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity

    def draw(self, surface):
        self.sprite.draw(surface, self.position)


class CharacterController(GameObject):
    speed = 3
    health = 100
    state = "idle"
    
    walkDirection = Vector2()

    def __init__(self, sprite: Sprite):
        GameObject.__init__(self, sprite)
        self.name = "character"

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
    def update(self):
        if self.state == "dead":
            return

        if self.state == "walking":
            self.velocity = self.walkDirection*self.speed
            self.position += self.velocity


class Player():
    character: CharacterController
    data: AlteredDataTree

    def __init__(self, data: dict, sprite: Sprite):
        self.data = AlteredDataTree(data, name="PlayerData")
        self.character = CharacterController(sprite)

    def getData(self, key):
        return self.data[key]   
    __getattr__=getData

    def setData(self, key, value):
        self.data[key] = value


class GameLayer():
    surface: Surface
    gameObjects: [GameObject]
    players: [Player]
    
    def __init__(self, window: Surface):
        self.surface = Surface(window.get_size(), pygame.SRCALPHA)
        self.gameObjects = []

    
    def addPlayer(self, plr: Player):
        self.players.append(plr)
        self.simulate(plr.character)

    def removePlayer(self, plr: Player):
        self.players.remove(plr)
        self.remove(plr.character)

    
    def simulate(self, *objs: GameObject):
        for obj in objs:
            if not isinstance(obj, GameObject):
                raise ValueError(f"{obj.__class__.__name__} cannot be simulated")

            if obj in self.gameObjects:
                raise ValueError(f"{obj.__class__.__name__} '{obj.name}' is already being simulated")
            
            self.gameObjects.append(obj)

    def remove(self, *obj: GameObject):
        for obj in objs:
            if not obj in self.gameObjects:
                raise ValueError(f"cannot remove missing {obj.__class__.__name__} '{obj.name}' from simulation")

            self.gameObjects.remove(obj)

    
    def render(self):
        self.surface.fill((0, 0, 0, 0))

        for obj in self.gameObject:
            obj.update()
            obj.draw(self.surface)


def getDash():
    def dashUpdate(self: Ability, player: PlayerController, deltaTime):
        if self.elapsed >= self.length:
            self.deactivate(player)
            self.data.set("dashing", False)
            player.speed = player.charSpeed
        else:
            player.speed = self.speed
            player.walkDirection = self.direction
            player.state = "walking"
        

    def dashActivation(self: Ability, player):
        self.setData("dashing", True)
        self.setData("direction", player.walkDirection)

    def dashPoll(self: Ability, player):
        return player.state == "walking"

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


# def draw_animated_bg(window):
#     """ Shared animated dot-grid background. """
#     offset = time() % 40
#     spacing = 40
#     for gx in range(-spacing, LARGEUR + spacing, spacing):
#         for gy in range(-spacing, HAUTEUR + spacing, spacing):
#             x = (gx - offset) % (LARGEUR + spacing)
#             y = (gy + offset) % (HAUTEUR + spacing)
#             pygame.draw.circle(window, (220, 220, 220), (x, y), 2)

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

    
    game = GameLayer(window)

    spritePNG = pygame.image.load("sprites\\lobsta.png")
    plrSprite = Sprite(spritePNG, 70/800)
    # plrSprite = Surface((25, 25))
    plr = Player(
        {
            "charSpeed": 5,
            "abilites": [],
            "immortal": False,
        },
        plrSprite)
    
    # plr = CharacterController(
    #     plrSprite,
    #     {
    #         "charSpeed": 5,
    #         "abilites": [],
    #         "immortal": False,
    #     })
    plr.character.position = windowSize/2
    plr.character.speed = plr.charSpeed
    plr.abilites.append(getDash())
    plr.abilites.append(shieldAbil)

    while True:
        now = time()
        deltaTime = now - lastTick
        elapsed = now - startTick
        window.fill(WHITE)
        # draw_animated_bg(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            if event.type == pygame.KEYDOWN:
                # print(event.unicode , event.key)
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

        # plr.update(deltaTime)
        # plr.draw(window)

        game.render()

        window.blit(render.surface, (0, 0))

        pygdisplay.flip()
        mainClock.tick(60)
        lastTick = now

if __name__=="__main__":
    main()
