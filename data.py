import pygame

class DataContainer():
    name: str
    data: dict

    VERBOSE = True

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __getattr__(self, name):
        data = self.data.get(name)

        if not data and self.VERBOSE:
            raise Warning(f"'{name}' data block is not registered in '{self.name}' DataContainer, set DataContainer.VERBOSE to False to silence")
        
        return data

GAME_DATA = DataContainer("Game data", {
    "game_state": "Menu",
    "gameplay_state": "Paused",
    "Characters": [
        {
            "name": "Blue Squer",
            "id": "BLUE_SQUER"
        }
    ]
})
