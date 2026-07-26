import pygame, sys


class WrappedDict():
    """ dict wrapper 
        Permits to query dict values stored with str keys by indexing 
        as an object attribute
        ex: self.key -> value is a shortcut for dataDictObject["key"] -> value

        self.VERBOSE attribute precises if Warning are raised when
        theres potentially missing data when que

        Write data using the set() method or by indexing like a dict
        ex: self.set(name, value) ; self[name] = value

        get(); pop(); clear() methods act similar to the dict methods
    """

    __slots__= {'_data', 'VERBOSE'}

    _data: dict
    VERBOSE: bool
    def __init__(self, src: dict=None):
        self._data = src or {}
        self.VERBOSE = True

    def __iter__(self):
        return iter(self._data)

    def __getattr__(self, attr):
        value = self.get(attr)
        
        if value is None and self.VERBOSE:
            raise Warning(" ".join((f"potentially missing data entry '{attr}',", 
                f"turn this warning off by setting {self.__class__.__name__}.VERBOSE to False")
            ))

        return value
    
    def set(self, key, value):
        """ Write data """
        self._data[key] = value

    def __str__(self):
        return f"<{self.__class__.__name__}>"
    __repr__=__str__

    __getitem__ = __getattr__
    __setitem__ = set


    def get(self, key):
        """ Read data """
        return self._data.get(key)

    def pop(self, key):
        return self._data.pop(key)

    def clear(self):
        self._data.clear()


class AlteredWrappedDict():
    __slots__ = {'_data', '_alteredData','name'}

    _alteredData: dict

    def __init__(self, src: dict=None):
        WrappedDict.__init__(self, src)
        self._alteredData = {}

    ## Public API
    def merge(self) -> dict:
        """ Merge altered and raw data in a dict """
        mergedDict = self._data.copy()
        for name, value in self._alteredData.items():
            mergedDict[name] = value

        return mergedDict

    def restore(self, name: str=None, getAlteredClone=False):
        """
            Restore altered data to its raw value.
            If no 'name' parameter is precised the 
            entire data tree is restored to raw data.

            returns the altered data value

            'getAlteredClone' only affects when no 'name' param is precised.
            when set to True a copy of the altered data is created and returned. 
            Thus this methods returns None if no 'name' param is precised and 
            'getAlteredClone' param is set to False.
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
        """ Alter data """
        if not (name in self._data):
            raise IndexError(f"cannot write altered data over missing '{name}' raw data")
        
        self._alteredData[name] = alteredValue
    
    def stamp(self, name=None):
        """ Write altered data into raw data.
            If 'name' param is let to None the entire altered 
            data layer will be written into the raw data. 
        """
        if name is None:
            for k, v in self._alteredData.items():
                self._alteredData.pop(name)
                self._data[name] = altered
        else:
            if not (name in self._alteredData):
                raise IndexError(f"cannot stamp missing '{name}' altered data into raw data")
            
            altered = self.getAltered(name)
            self._alteredData.pop(name)
            self._data[name] = altered
    
    ## Data methods
    def getRaw(self, key):
        return self._data.get(key)
    
    def getAltered(self, key):
        return self._alteredData.get(key)

    def get(self, key):
        altered = self.getAltered(key)
        
        if altered is not None:
            return altered
        else:
            return self.getRaw(key)

    def pop(self, key):
        altered = self._alteredData.get(key)
        if altered is not None:
            self._data.pop(key)
            return self._alteredData.pop(key)
        
        return self._data.pop(key)

    def clear(self):
        self._data.clear()
        self._alteredData.clear()


class DataTree(WrappedDict):
    """ dict wrapper 
        inherit from WrappedDict, Permits to query dict values stored 
        with str keys by indexing as an object attribute.
        ex: self.key -> value is a shortcut for dataDictObject["key"] -> value

        Used to create advanced data trees, every data entry of type dict
        is converted to another tree.
        ex: self.tree1.tree2.key == dataDictObject["tree1"]["tree2"]["key"]

        self.VERBOSE attribute precises if Warning are raised when
        theres potentially missing data when que

        Write data using the set() method or by indexing like a dict
        ex: self.set(name, value) ; self[name] = value

        get(); pop(); clear() methods act similar to the dict methods
    """
    __slots__ = {'_data', 'name', 'VERBOSE'}

    name: str

    def __init__(self, src: dict=None, name="anonymous", recursive=True):
        self._data = {}
        self.VERBOSE = True
        self.name = name

        if src is None: return
        
        for k, v in src.items():
            self.set(k, v, recursive)

    def __str__(self):
        return f"<'{self.name}' {self.__class__.__name__}>"
    __repr__=__str__

    def set(self, key, value, recursive=True):
        """ 
            Write data
            
            'recursive' param indicates the descendant dict type.
            type(self) is used if set to True
        """
        if type(value) is dict and recursive:
            recursionType = recursive is True and type(self) or recursive
            name = value.get("name")
            
            if type(name) is not str:
                name = "anonymous"
                
            value = recursionType(value, name=name, recursive=recursive)
            value.VERBOSE = self.VERBOSE

        self._data[key] = value
    __setitem__ = set


class AlteredDataTree(DataTree):
    """ dict wrapper 
        inherit from both DataTree and AlteredWrappedDict, Permits to 
        query dict values stored with str keys by indexing as object attribute.
        ex: self.key -> value is a shortcut for dataDictObject["key"] -> value

        Used to create advanced data trees that contains two layer of data: 
        raw data and altered data.
        When reading the altered data is red over the raw data.
        Alter data by using the alter() method.
        When writing data with set() method or by indexing it only affects raw data.
        Use the restore() methods to revert altered data to raw data.

        self.VERBOSE attribute precises if Warning are raised when
        theres potentially missing data when que

        Write data using the set() method or by indexing like a dict
        ex: self.set(name, value) ; self[name] = value

        get(); pop(); clear() methods act similar to the dict methods
    """
    __slots__ = {'_data', '_alteredData', 'name'}

    _alteredData: dict

    def __init__(self, src: dict=None, name="anonymous", recursive=DataTree):
        DataTree.__init__(self, src, name, recursive)
        self._alteredData = {}


    ## Public API
    merge = AlteredWrappedDict.merge
    restore = AlteredWrappedDict.restore
    alter = AlteredWrappedDict.alter
    stamp = AlteredWrappedDict.stamp

    def set(self, name, value, recursive=DataTree):
        """
            Writes raw data
            
            'recursive' param indicates the descendant dict type
            type(self) is used if this param is set to true
        """
        DataTree.set(self, name, value, recursive=recursive)
    __setitem__=set
    
    
    ## Data methods
    getAltered = AlteredWrappedDict.getAltered
    getRaw = AlteredWrappedDict.getRaw
    get = AlteredWrappedDict.get
    pop = AlteredWrappedDict.pop
    clear = AlteredWrappedDict.clear

def test():
    test = AlteredDataTree({
        "nice": True
    })

    test.set("nice", False)
    print("test.nice", test.nice)
    print("test.getRaw('nice')", test.getRaw("nice"))

    print(test._data, test._alteredData)

    print()
    test.alter("nice", True)
    print("test.nice", test.nice)
    print("test.getRaw('nice')", test.getRaw("nice"))

    print(test._data, test._alteredData)

    print()
    test.restore()
    print("test.nice", test.nice)
    print("test.getRaw('nice')", test.getRaw("nice"))

    print(test._data, test._alteredData)


    print()
    dih = {
        "name": "SUPER",
        "xd": True,
        "recursive": {
            "name": "RECURSIVE",
            "damn": 1
        }
    }
    test.set("superDict", dih, recursive=True)

    print("test.superDict", test.superDict)
    print(test._data, test._alteredData)

    print()
    print("test.superDict.recursive.damn", test.superDict.recursive.damn)

    print()
    test.superDict.recursive.alter('damn', 2)
    print("test.superDict.recursive.damn", test.superDict.recursive.damn)
    print("test.superDict.recursive.getRaw('damn')", test.superDict.recursive.getRaw('damn'))

    print()
    print("test.superDict.recursive", test.superDict.recursive)

    print()
    test.superDict.recursive.stamp('damn')
    # print(test.damn)
    print(test.superDict.recursive.getRaw("damn"))
    print(test.superDict.recursive.getAltered("damn"))

if __name__=="__main__":
    test()

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
