import glob

import numpy as np
import matplotlib.pyplot as plt
import spacy
import cv2
import pytesseract as pt
from pytesseract import Output

#
# img_list  = glob.glob("./data/raw_images/*.jpg")
# img=img_list[6]


def read_image(img_path: str):
    image = cv2.imread(img_path)
    return image


def get_gray_image_and_dilate(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Create rectangular structuring element and dilate
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    return gray, dilate


def get_contours(dilate: np.ndarray) -> tuple:
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts


def get_contour_center(contour):
    x, y, w, h = cv2.boundingRect(contour)
    X = x + (w // 2)
    Y = y + (h // 2)

    return (X, Y)

def extract_text_from_contour(contour, gray, image):
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
    ROI = gray[y:y + h, x:x + w]
    txt = pt.image_to_string(ROI, lang='lit', config='--psm 6')
    txt = txt.replace('\n', '. ')

    return txt

def convert_image_to_contours(image: np.ndarray):
    gray, dilate = get_gray_image_and_dilate(image)
    contours = get_contours(dilate)

    return gray, contours



# data = []
# for img in img_list:
#     # Load image, grayscale, Gaussian blur, Otsu's threshold
#     image = cv2.imread(img)
#     # d = pt.image_to_data(image, output_type=Output.DICT)
#
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (7, 7), 0)
#     thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#
#     # Create rectangular structuring element and dilate
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
#     dilate = cv2.dilate(thresh, kernel, iterations=4)
#
#     # Find contours and draw rectangle
#     cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#     # data = []
#     for c in cnts:
#         x,y,w,h = cv2.boundingRect(c)
#         cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
#         ROI = gray[y:y + h, x:x + w]
#         txt = pt.image_to_string(ROI, lang='lit', config='--psm 6')
#         txt = txt.replace('\n', '. ')
#         data.append(txt)
#         print(txt)
#         print("---------------------")
#
# nlp = spacy.load("lt_core_news_lg")
#
# clean_data = [nlp(x) for x in data]
# with open("./data/processed_data/paragraphs.txt", "w") as output:
#     for row in clean_data:
#         output.write(str(row) + '\n')
#
# # cv2.imshow('thresh', thresh)
# # cv2.imshow('dilate', dilate)
# imS = cv2.resize(image, (860, 1024))                # Resize image
# cv2.imshow('image', imS)
# cv2.waitKey()
