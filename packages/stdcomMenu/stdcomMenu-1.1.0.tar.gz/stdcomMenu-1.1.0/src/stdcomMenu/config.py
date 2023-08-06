import stdcomQt
from stdcomQt.stdcomvsettings import  VSettings
from PyQt5.QtCore import QSettings

class MenuConfigue( ):

    project = "stec-menu"
    definitions = {}

    def __init__(self, project: str = "stec-menu"):
        self.project = project

        settings = VSettings(self.project)
        self.definitions =  settings.value("definition", self.definitions)

    def addKey(self, key : str,  data : []):
        entryKey = key
        self.definitions.update ( { entryKey : data } )
        settings = VSettings(self.project)
        settings.setValue("definition", self.definitions)

    def getFromKey(self, key : str ):
        entryKey = key
        if entryKey in self.definitions :
            return self.definitions.get(entryKey)

    def deleteAllWithKey(self, key):

        keysOf = key
        keys = self.definitions.keys()
        for each in keys :
            try:
                if each.index(keysOf) == 0 :
                    self.definitions.update( { each : None } )
            except :
                print("Missing")

        settings = VSettings(self.project)
        settings.setValue("definition", self.definitions)

    def deleteKey(self, key):

        if key in self.definitions.keys() :
            self.definitions.update( {key : None} )

        settings = VSettings(self.project)
        settings.setValue("definition", self.definitions)

    def keys(self):
        return list(self.definitions.keys())
    def all(self):
        return list(self.definitions.keys()), list(self.definitions.values())

    def values(self):
        return list(self.definitions.values())




class DecodeData() :


    def getLabel(self, data ):
        if data is not None and len(data) >= 5 :
            return data[0]
        return None

    def getPositions(self, data ):
        print("Decode")

        if data is not None and len(data) >= 5 :
            return data[3]
        return None

    def getApp(self, data ):
        if data is not None and len(data) >= 5 :
            return data[1]
        return None

    def getParameters(self, data ):
        if data is not None and len(data) >= 5 :
            return data[2]
        return None

    def getHelp(self, data ):
        if data is not None and len(data) >= 5 :
            return data[4]
        return None

if __name__ == '__main__':

    print("stdcomMenu")
    import sys

    if "--version" in sys.argv:

        sys.exit()

    k = MenuConfigue()
    k.addKey("Testing",["this", "that","And"])

    print(k.getFromKey("Testing" ))
    k.deleteAllWithKey("Testing" )
    print(k.getFromKey("Testing"))
