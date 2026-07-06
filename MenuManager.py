import pygame, pygame_ui, json
from pygame_ui import Panel
from copy import deepcopy as clone

# upgradeMenu = UI.Panel()
# upgradeMenu.build({
#     "frame": {
#         "name": "main_frame",
#         "anchorPoint": (.5, .5),
#         "position": (.5,0,.5,0),
#         "color": "red",
#         "enabled": True,
        
#         "children": {
#             "text_button": {
#                 "name": "main_button",
#                 "text": "Next",
#                 "transparency": 1
#             }
#         }
#     }
# })
# def updateUpgradeMenu(self, gameData):
#     upgrades = gameData["active_upgrades"]

#     cardsPad = 30
    
#     for i, upgrade in enumerate(upgrades):
#         cardX = 1.5 - i
#         cardY = 0


active_menu = None
game_menus = {}

class Menu():
    name: str
    active = False
    panel: Panel
    update = None
    _onLoad = None

    nextMenu: str
    lastMenu: str

    menus = game_menus

    def __init__(self, name: str, panel, onUpdate, onLoad=None):
        assert type(name) is str, "argument 1 must be str"
        assert type(panel) is Panel and panel.parent is not None, "argument 'panel' must be Panel, parented to a layer"

        if self.menus.get(name):
            raise Exception(f"{self.name} game menu already exists")

        self.menus[name] = self

        self.name = name
        self.panel = panel
        self.update = onUpdate
        self._onLoad = onLoad

    # def initTransitions(self):
    #     if next is not None:
    #         self.nextMenu = next
    #     if last is not None:
    #         self.lastMenu = last

    #     for name, elem in self.panel.descendants:
    #         if name == "next_menu":
    #             if self.nextMenu is None: continue
    #             elem.bindAction("clicked", lambda: load(self.nextMenu))

    #         elif name == "exit_menu":
    #             if self.lastMenu is None: continue
    #             elem.bindAction("clicked", lambda: load(self.lastMenu))

    def load(self, gameData):
        self.active = True
        self.panel.enabled = True

        if self._onLoad is not None:
            self._onLoad(self, gameData)

    def exit(self):
        self.active = False
        self.panel.enabled = False


def load(name: str, gameData):
    global active_menu
    
    menu = game_menus.get(name)
    if menu is None:
        raise ValueError(f"{name} game menu does not exists")

    for m in game_menus.values():
        m.exit()

    active_menu = menu
    menu.load(gameData)


def refresh(gameData):
    global active_menu
    assert active_menu, "cannot refresh, no menu is loaded"
    active_menu.load(gameData)

    

def init(ui_layer, gameData):
    mainMenuPanel = Panel.fromLayer(ui_layer)
    mainMenuPanel.build([
        {
            "type": "TEXT_LABEL",
            "name": "title_frame",
            "position": (.5,0,.5,0),
            "anchorPoint": (.5, .5),
            "visible": False,
            "color": "black",
            
            "children": [
                {
                    "type": "TEXT_LABEL",
                    "name": "title_label",
                    "text": "Blue Squer",
                    "color": "blue",
                    "anchorPoint": (.5, 1),
                    "position": (.5, 0, .5, -100),
                    # "font": title_font,
                    # "transparency": 1
                },
                {
                    "type": "TEXT_BUTTON",
                    "name": "main_button",
                    "text": "Play",
                    "color": "red",
                    "anchorPoint": (.5, 0),
                    "position": (.5, 0, .5, 20),
                    # "font": button_font,
                    # "transparency": 1
                }
            ]
        }
    ])
    def mainMenuUpdate(self: Menu, gameData):
        gui = self.panel
        gui_descendants = gui.descendants
        main_button = gui_descendants["main_button"]

        if main_button.state == "clicked":
            load("Character", gameData)

    charMenuPanel = Panel.fromLayer(ui_layer)
    charMenuPanel.build([
        {
            "type": "FRAME",
            "name": "card_container",
            "position": (0,0,.5,0),
            "size": (1,0,.3,0),
            "anchorPoint": (0,.5),
            "color": "black",

            "children": [
                {
                    "type": "FRAME",
                    "name": "card_template",
                    "enabled": True,
                    "size": (1,0,1,0),
                    "anchorPoint": (.5,.5),
                    "color": "red"
                }
            ]
        },
        {
            "type": "FRAME",
            "name": "main_frame",
            "anchorPoint": (.5, .5),
            "position": (.5,0,.5,0),
            "visible": False,
            "color": "black",
            
            "children": [
                {
                    "type": "TEXT_BUTTON",
                    "name": "main_button",
                    "text": "Next",
                    "transparency": 1
                }
            ]
        }
    ])
    def updateCharMenu(self: Menu, gameData):
        pass

    def loadCharMenu(self: Menu, gameData):
        characters = gameData.Characters
        spacing = 1/len(characters)

        for i, char in enumerate(characters):
            card_y = spacing * i

    Menu("Main", mainMenuPanel, mainMenuUpdate)
    Menu("Character", charMenuPanel, updateCharMenu, loadCharMenu)
    
    if game_menus.get("Main"):
        load("Main", gameData)
