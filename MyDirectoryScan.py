import os
import re
import glob


class DirectoryIndex:

    def __init__(self):
        self.dict = {}
        self.pattern = {"pattern": r"(.*\\)(\d\d-\d{6})([\w\d\s]*)(\\.*)?", "pfad": 1, "AuftragsNr": 2, "adding": 3}

    def scan(self, path):
        for filename in glob.iglob(path + '**/**', recursive=True):
            if os.path.isdir(filename):
                m = re.search(self.pattern["pattern"], filename)
                if m is not None:
                    self.dict[m.group(self.pattern["AuftragsNr"])] = m.group(self.pattern["pfad"]) \
                                                            + m.group(self.pattern["AuftragsNr"]) \
                                                            + m.group(self.pattern["adding"])

    def getpath(self, key):
        if key in self.dict.keys():
            return self.dict[key]
        return None

    def test(self):
        pass


if __name__ == "__main__":
    myDi = DirectoryIndex()
    mypath = r"C:\Users\franz.hidber\Desktop\Kunde"
    myDi.scan(mypath)
    print(myDi.getpath("10-113743"))
