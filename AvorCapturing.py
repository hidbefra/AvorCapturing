import os
import re
import glob
import MyDirectoryScan
import logging
import configparser
import myPDFocr

from pyzbar import pyzbar
from pdf2image import convert_from_path
import shutil

import textract


class AvorCapturing:

    def __init__(self):

        # noinspection PyArgumentList
        logging.basicConfig(
            filename='AvorCapturing.log',
            level=logging.DEBUG,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y.%m.%d %H:%M:%S',
            encoding='utf-8',
        )

        # logging.basicConfig(filename='AvorCapturing.log', encoding='utf-8', level=logging.DEBUG)
        # formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s","%Y-%m-%d %H:%M:%S")
        logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)
        logging.info("--- start process ---")

        self.config = configparser.ConfigParser()
        if not os.path.exists('AvorCapturing.ini'):
            self.config['DEFAULT']["Ablage"] = r"\ScannAvor"
            self.config['DEFAULT']["AvorScanPath"] = r"C:\Users\franz.hidber\Desktop\Avor"
            self.config['DEFAULT']["KundenPath"] = r"C:\Users\franz.hidber\Desktop\Kunde"
            self.config['AvorBarcodPatern'] = {"patern": r"(\d\d-\d{6})#(.*)#(.*)", "AuftragsNr": 1, "typ": 2, "PageNr": 3}
            self.config['AuftragNrPatern'] = {"patern": r"(\d\d-\d{6})", "AuftragsNr": 1}
            self.config['DateinamePatern'] = {"patern": r"(\d\d-\d{6})(.*)(?:.pdf)", "AuftragsNr": 1, "info": 2}

            with open('AvorCapturing.ini', 'w') as configfile:
                self.config.write(configfile)

        self.config.read('AvorCapturing.ini', encoding='utf-8')
        self.config.sections()

        self.myDi = MyDirectoryScan.DirectoryIndex()
        # myDi.scan(config['DEFAULT']["KundenPath"])
        self.myDi.loadjson()
        pass

    def find_regex_on_barcode_in_pdf(self, path, patern):
        images_from_path = convert_from_path(path)
        for image in images_from_path:
            decoded = pyzbar.decode(image)
            for d in decoded: #testen der Barcods auf einer Seite
                m = re.search(patern, d.data.decode("utf-8"))
                if m is not None:
                    #print(m.group(__AuftragsNr) + "_" + m.group(__typ) + "_" + m.group(__PageNr))
                    return m
        pass


    def find_regex_in_pdf(self, path, patern):
        text = textract.process(path)
        text = text.decode("utf-8")
        text = text.replace(" ", "") #leehrzeichen entfernen
        # print(text)
        m = re.search(patern, text)
        #print(m.group(1))
        return m
        pass


    def analyze_pdf(self, path):
        nr = None
        name = None

        m = self.find_regex_on_barcode_in_pdf(path, self.config['AvorBarcodPatern']["patern"]) #ist ein ensprechender Barcod vorhanden?
        if m is not None:
            nr = m.group(int(self.config['AvorBarcodPatern']["AuftragsNr"]))
            name = nr + "_" + m.group(int(self.config['AvorBarcodPatern']["typ"])) + "_" + m.group(int(self.config['AvorBarcodPatern']["PageNr"]))
            if self.myDi.getpath(nr):
                return nr, name

        m = re.search(self.config['DateinamePatern']["patern"], path)  # alternative benutze name der pdf datei
        if m is not None:
            nr = m.group(int(self.config['DateinamePatern']["AuftragsNr"]))
            name = nr + m.group(int(self.config['DateinamePatern']["info"]))
            if self.myDi.getpath(nr):
                return nr, name

        m = self.find_regex_in_pdf(path, self.config['AuftragNrPatern']["patern"]) #alternativ kann die AUftrags Nr im Dokumnet gefunden werden
        if m is not None:
            name = m.group(int(self.config['AuftragNrPatern']["AuftragsNr"]))
            nr = name
            if self.myDi.getpath(nr):
                return nr, name

        m = re.search(self.config['AuftragNrPatern']["patern"], myPDFocr.pdf2ocr(path))  #benutzen der tesseract OCR
        if m is not None:
            name = m.group(int(self.config['AuftragNrPatern']["AuftragsNr"]))
            nr = name
            if self.myDi.getpath(nr):
                return nr, name
        nr = None
        name = None
        return nr, name


    def count_dir(self, path):
        files =0
        folders = 0
        path, dirnames, filenames = next(os.walk(path))
        # ^ this idiom means "we won't be using this value"
        files += len(filenames)
        folders += len(dirnames)
        #print("{:,} files, {:,} folders".format(files, folders))
        return folders, files


    def process(self):


        progress = 0
        _, filescount = self.count_dir(self.config['DEFAULT']["AvorScanPath"])

        for filename in glob.iglob(self.config['DEFAULT']["AvorScanPath"] + '**/**.pdf', recursive=False):
            progress += 1
            print("{}%".format(round(100/filescount*progress, 1)))
            #print(filename)
            nr, name = self.analyze_pdf(filename) #suche nach Auftragsnummer im PDF
            if nr is not None:
                dst = self.myDi.getpath(nr) #prüfe ob auftragsNr einen Ordner hatt
                if dst is not None:

                    dst = dst + self.config['DEFAULT']["Ablage"] + "\\" + name
                    os.makedirs(os.path.dirname(dst), exist_ok=True)

                    if os.path.exists(dst + ".pdf"): #prüfe ob zeil datei exisiter
                        i = 1
                        while os.path.exists(dst + "(" + str(i) + ")" + ".pdf"):
                            i += 1
                        dst = dst + "(" + str(i) + ")" + ".pdf"
                    else:
                        dst = dst + ".pdf"

                    src = filename
                    logging.info("copy to; {}".format(dst))
                    shutil.move(src, dst)


if __name__ == "__main__":
    myAvorCapturing = AvorCapturing()
    myAvorCapturing.process()
