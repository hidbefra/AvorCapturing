import os
import re
import glob
import MyDirectoryScan
import logging
import configparser

from pyzbar import pyzbar
from pdf2image import convert_from_path
import shutil

import textract


def find_regex_on_barcode_in_pdf(path, patern):
    images_from_path = convert_from_path(path)
    for image in images_from_path:
        decoded = pyzbar.decode(image)
        for d in decoded: #testen der Barcods auf einer Seite
            m = re.search(patern, d.data.decode("utf-8"))
            if m is not None:
                #print(m.group(__AuftragsNr) + "_" + m.group(__typ) + "_" + m.group(__PageNr))
                return m
    pass


def find_regex_in_pdf(path, patern):
    text = textract.process(path)
    text = text.decode("utf-8")
    # print(text)
    m = re.search(patern, text)
    #print(m.group(1))
    return m
    pass


def analyze_pdf(path):
    nr = None
    name = None

    m = find_regex_on_barcode_in_pdf(path, config['AvorBarcodPatern']["patern"]) #ist ein ensprechender Barcod vorhanden?
    if m is not None:
        nr = m.group(int(config['AvorBarcodPatern']["AuftragsNr"]))
        name = nr + "_" + m.group(int(config['AvorBarcodPatern']["typ"])) + "_" + m.group(int(config['AvorBarcodPatern']["PageNr"]))
    m = find_regex_in_pdf(filename, config['AuftragNrPatern']["patern"]) #alternativ kann die AUftrags Nr gefunden werden
    if m is not None:
        name = m.group(int(config['AuftragNrPatern']["AuftragsNr"]))
        nr = name
    m = re.search(config['DateinamePatern']["patern"], path) #alternative benutze name der pdf datei
    if m is not None:
        nr = m.group(int(config['DateinamePatern']["AuftragsNr"]))
        name = nr + m.group(int(config['DateinamePatern']["info"]))
    return nr, name


if __name__ == "__main__":
    logging.basicConfig(filename='AvorCapturing.log', encoding='utf-8', level=logging.DEBUG)
    logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

    config = configparser.ConfigParser()
    if not os.path.exists('AvorCapturing.ini'):
        config['DEFAULT']["Ablage"] = r"\ScannAvor"
        config['DEFAULT']["AvorScanPath"] = r"C:\Users\franz.hidber\Desktop\Avor"
        config['DEFAULT']["KundenPath"] = r"C:\Users\franz.hidber\Desktop\Kunde"
        config['AvorBarcodPatern'] = {"patern": r"(\d\d-\d{6})#(.*)#(.*)", "AuftragsNr": 1, "typ": 2, "PageNr": 3}
        config['AuftragNrPatern'] = {"patern": r"(\d\d-\d{6})", "AuftragsNr": 1}
        config['DateinamePatern'] = {"patern": r"(\d\d-\d{6})(.*)(?:.pdf)", "AuftragsNr": 1, "info": 2}

        with open('AvorCapturing.ini', 'w') as configfile:
            config.write(configfile)

    config.read('AvorCapturing.ini', encoding='utf-8')
    config.sections()

    myDi = MyDirectoryScan.DirectoryIndex()
    #myDi.scan(config['DEFAULT']["KundenPath"])
    myDi.loadjson()

    for filename in glob.iglob(config['DEFAULT']["AvorScanPath"] + '**/**.pdf', recursive=False):
        #print(filename)
        nr, name = analyze_pdf(filename) #suche nach Auftragsnummer im PDF
        if nr is not None:
            dst = myDi.getpath(nr) #prüfe ob auftragsNr einen Ordner hatt
            if dst is not None:

                dst = dst + config['DEFAULT']["Ablage"] + "\\" + name
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
