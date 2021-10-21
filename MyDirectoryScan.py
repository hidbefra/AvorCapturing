import os
import re
import glob
import json


class DirectoryIndex:

    __EstimateSize = 17000

    def __init__(self):
        self.dict = {}
        self.pattern = {"pattern": r"(\d\d-\d{6})", "AuftragsNr": 1,}    #(.*\\)(\d\d-\d{6})([\w\d\s]*)(\\.*)?

    def scan(self, path):
        i = 0
        for filename in glob.iglob(path + '**/**/', recursive=True):
            if os.path.isdir(filename):
                dirname = os.path.basename(os.path.normpath(filename)) # name des letzten ordners
                m = re.search(self.pattern["pattern"], dirname)
                if m is not None:
                    nr = m.group(self.pattern["AuftragsNr"])
                    print("{}%, {}".format(round(100/self.__EstimateSize*i, 2), nr))
                    self.dict[nr] = filename
            i += 1

    def getpath(self, key):
        if key in self.dict.keys():
            return self.dict[key]
        return None

    def save2json(self):
        with open('DirectoryIndex.txt', 'w', encoding='utf8') as outfile:
            json.dump(self.dict, outfile, indent=4, ensure_ascii=False)
        pass

    def loadjson(self):
        with open('DirectoryIndex.txt', encoding='utf8') as json_file:
            data = json.load(json_file)
            self.dict = data
        pass



if __name__ == "__main__":
    myDi = DirectoryIndex()
    mypath = r"P:\01a Verkauf\04 Aufträge"
    #mypath = r"C:\Users\franz.hidber\Desktop\Kunde\Test\10-114459 - Spezial"

    myDi.scan(mypath)
    myDi.save2json()
    #myDi.loadjson()

    print("Test:")
    print("{} liegt hier: {}".format("10-113246", myDi.getpath("10-113246")))
