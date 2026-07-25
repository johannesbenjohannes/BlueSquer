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

    def clear(self):
        self._data.clear()


class DataTree(WrappedDict):
    """ dict wrapper 
        inherit from WrappedDict, used to create a tree of data
        every 
        
    """

    name: str

    def __init__(self, src: dict=None, name="anonymous", tree=True):
        self._data = {}
        self.name = name

        if src is None: return
        
        for k, v in src.items():
            self.setd(k, v, tree)

    def __repr__(self):
        return f"<'{self.name}' {self.__class__.__name__}>"

    def setd(self, key, value, recursion=True):
        """ 
            set data: shortcut for DataTree._data['name'] = 'value'   
            'recursion' indicates the descendant dict type, type(self) if set to true
        """
        if type(value) is dict and recursion:
            recursion = recursion is True and type(self) or recursion
            name = value.get("name")
            
            if name is None or type(name) is not str:
                name = "anonymous"
                
            value = recursion(value, name=name)

        self._data[key] = value
    __setitem__ = setd


class AlteredDataTree(DataTree):
    """ dict wrapper
        inherit from DataTree, adds an altered data layer
        
        when querying data altered data will be returned other raw data
        alter data by using the alter() (and not ) methods
        use the restore() methods to bring data back to raw value
     """
    _alteredData: dict

    def __init__(self, src: dict=None, name="anonymous", tree=True):
        DataTree.__init__(self, src, name, tree)
        setattr(self, "_alteredData", {})


    ## Public API
    def merge(self) -> dict:
        """ returns a dict of the merge of altered and row data """
        mergedDict = self._data.copy()
        for name, value in self._alteredData.items():
            mergedDict[name] = value

        return mergedDict

    def restore(self, name: str=None, getAlteredClone=False):
        """
            used to restore data to its raw value
            when no data name is given the entire data is restore to raw

            returns the altered data value

            getAlteredClone defines if a clone of the altered data dict is returned
        """
        if not name:
            alteredCopy = None
            if getAlteredClone:
                alteredCopy = self._alteredData.copy()
            
            self._alteredData.clear()
            return alteredCopy

        altered = self._alteredData[name]
        self._alteredData.pop(name)
        return altered

    def alter(self, name, alteredValue):
        """ alters data """
        if self.getRaw(name) is None:
            raise IndexError(f"cannot create altered data other missing {name} raw data")
        
        self._alteredData[name] = alteredValue
    # Setting data using index will create altered data
    __setitem__=alter

    def setd(self, name, value, recursion=DataTree):
        """
            set data: shortcut for AlteredDataTree._data['name'] = 'value'   
            'recursion' indicates the descendant dict type, type(self) if set to true
        """
        DataTree.setd(self, name, value, recursion=recursion)
    
    ## Dict methods
    def getRaw(self, key):
        return self._data.get(key)

    def get(self, key):
        altered = self._alteredData.get(key)
        
        if altered is not None:
            return altered
        else:
            return self._data.get(key)

    def pop(self, key):
        altered = self._alteredData.get(key)
        if altered is not None:
            self._data.pop(key)
            return self._alteredData.pop(key)
        
        return self._data.pop(key)

    def clear(self):
        self._data.clear()
        self._alteredData.clear()


GAME_DATA = DataTree({
    "game_state": "Menu",
    "gameplay_state": "Paused",
    
    
    "characters": [
        {
            "name": "Blue Squer",
            "id": "BLUE_SQUER"
        }
    ],
}, name="GAME_DATA")
