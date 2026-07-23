import pygame


class WrappedDict():
    """ dict wrapper where dict keys stored as strings can be directly indexed as object attribute """
    _data = None
    VERBOSE = True

    def __init__(self, d: dict=None):
        self._data = d or {}

    def __iter__(self):
        return iter(self._data)

    def __getattr__(self, attr):
        value = self.get(attr)

        if value is None and self.VERBOSE:
            raise Warning(" ".join((f"missing dict entry {attr},", 
                f"turn this warning off by setting {self.__class__.__name__}.VERBOSE to False")
            ))

        return value
    
    def setd(self, key, value):
        """ set data: shortcut for WrappedDict._data['key'] = 'value' """
        self._data[key] = value

    def __str__(self):
        return str(self._data)

    __getitem__ = __getattr__
    __setitem__ = setd


    def get(self, key):
        return self._data.get(key)

    def pop(self, key):
        return self._data.pop(key)

    def remove(self, value):
        return self._data.remove(value)

    def clear(self):
        return self._data.clear()


class DataTree(WrappedDict):
    """ inherit from WrappedDict, descendants dictionnaries are converted to data trees """

    name: str

    def __init__(self, src: dict=None, name="anonymous", tree=True):
        self._data = {}
        self.name = name

        if src is None: return

        for k, v in src.items():
            self.setd(k, v, tree)

    def __repr__(self):
        return f"<'{self.name}' {self.__class__.__name__}>"

    def setd(self, key, value, tree=True):
        """ 
            set data: shortcut for WrappedDict._data['key'] = 'value'
            'tree' indicates wether or not 'value' should be converted to DataTree
        """

        if tree and type(value) is dict:
            name = value.get("name")
            if name is None or type(name) is not str:
                name = "anonymous"
                
            value = DataTree(value, name=name)

        self._data[key] = value



GAME_DATA = DataTree({
    "game_state": "Menu",
    "gameplay_state": "Paused",
    "Characters": [
        {
            "name": "Blue Squer",
            "id": "BLUE_SQUER"
        }
    ],
    "Nope": {"Pop": "nice", "name": "Player"}
}, name="GAME_DATA")
