import numpy as np
import pytesseract as pt
import spacy
from spacy import displacy
# from langdetect import detect

from src.utils.read_data import pdf_to_image
from src.processing.ocr_image import convert_image_to_contours, extract_text_from_contour, read_image, get_contour_center


path="./data/raw/VST_0215333_2022_3.pdf"
doc_image = pdf_to_image(path)

# Convert a page to a string [0] first page
content = pt.image_to_string(doc_image[0], lang='lit', config='--psm 6')

# nlp = spacy.load("lt_core_news_lg")
#
def entites(text, nlp):
    # lang = detect(text)
    try:
        nlp2 = nlp#[lang]
    except KeyError:
        return Exception(lang + " model is not loaded")
    return [(str(x).lower(), x.label_) for x in nlp2(str(text)).ents]



def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def define_moketojas_tiekejas(c1: tuple, c2: tuple, ent1: list, ent2: list):
    angle = angle_between(c1, c2)
    if angle <= 180:
        print(ent1, "Moketojas")
        print(ent2, "Tiekejas")
        return ent2

    elif angle > 180:
        print(ent1, "Tiekejas")
        print(ent2, "Moketojas")
        return ent1


ents = entites(content)
print(ents)

nlp = spacy.load("./output/model-last/")
# doc = nlp(content)
# html_text = displacy.render(doc, style="ent", jupyter=False)
#
# with open("./data/html_output/invoice_ner_3.html", "w") as file:
#     file.write(html_text)

# entites(doc, nlp)

##############################

nlp = spacy.load("./output/model-last/")

path="./data/raw_images/VST_0215333_2022_3-1.jpg"

image = read_image(path)
gray, contours = convert_image_to_contours(image)

results = []
coords = []

for cnt in contours:
    text = extract_text_from_contour(cnt, gray, image)
    center = get_contour_center(cnt)

    ner_result = entites(text, nlp)
    if len(ner_result) > 0:
        for res in ner_result:
            results.append(res)
            coords.append(center)


## TODO: nustatyti moketoja ir tiekeja pagal ju realityvias pozicijas
imones = []
# imoniu_coords = []
for ent, cord in zip(results, coords):
    if ent[1] == 'imone':
        imones.append([ent, cord])
        # imoniu_coords.append(cord)

define_moketojas_tiekejas(imoniu_coords[2], imoniu_coords[1], imones[2], imones[1])