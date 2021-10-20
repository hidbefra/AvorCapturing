import os
import re
import glob
import json


class DirectoryIndex:

    def __init__(self):
        self.dict = {}
        self.pattern = {"pattern": r"(.*\\)(\d\d-\d{6})([\w\d\s]*)(\\.*)?", "pfad": 1, "AuftragsNr": 2, "adding": 3}

    def scan(self, path):
        for filename in glob.iglob(path + '**/**/', recursive=True):
            if os.path.isdir(filename):
                m = re.search(self.pattern["pattern"], filename)
                if m is not None:
                    print(m.group(self.pattern["AuftragsNr"]))
                    self.dict[m.group(self.pattern["AuftragsNr"])] = m.group(self.pattern["pfad"]) \
                                                            + m.group(self.pattern["AuftragsNr"]) \
                                                            + m.group(self.pattern["adding"])

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
    #myDi.scan(mypath)
    #myDi.save2json()
    myDi.loadjson()
    myDi.save2json()
    print(myDi.getpath("10-113246"))
