from pdf2image import convert_from_path
import cv2
import pytesseract
import CV2autoRotat


def pdf2ocr(path):

    pages = convert_from_path(path, 350)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Users\franz.hidber\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    text = ""
    for page in pages:
        image_name = "Page_" + str(1) + ".jpg"
        page.save(image_name, "JPEG")

        img_cv = cv2.imread(r'Page_1.jpg')
        img_cv = CV2autoRotat.deskew(img_cv)
        #imS = cv2.resize(img_cv, (960, 540))
        #cv2.imshow('image', imS)
        #cv2.waitKey(0)

        # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
        # we need to convert from BGR to RGB format/mode:
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        text = text + pytesseract.image_to_string(img_rgb)
    return text.replace(" ", "") #leehrzeichen entfernen


# To accomplish OCR with Python on Windows, you will need Python and OpenCV which you already have, as well as Tesseract and the Pytesseract Python package.
#
# To install Tesseract OCR for Windows:
#
#     Run the installer(find 2021) from UB Mannheim https://digi.bib.uni-mannheim.de/tesseract/
#     Configure your installation (choose installation path and language data to include)
#     Add Tesseract OCR to your environment variables
#
# To install and use Pytesseract on Windows:
#
#     Simply run pip install pytesseract
#     You will also need to install Pillow with pip install Pillow to use Pytesseract. Import it in your Python document like so from PIL import Image.
#     You will need to add the following line in your code in order to be able to call pytesseract on your machine: pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#
# I've given a detailed walkthrough of how to install Tesseract OCR for Windows here if you would like further guidance.
