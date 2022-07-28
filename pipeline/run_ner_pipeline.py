import numpy as np
import re
import spacy

from src.utils.ner_utils import define_moketojas_tiekejas, get_text_from_contour, which_is_on_the_top
from src.processing.ocr_image import convert_image_to_contours, extract_text_from_contour, read_image, \
    get_contour_center


def get_total_amount_and_amount_before_taxes(pinigai: list, tax=0.8264462809917356) -> [float, float, float]:
    tmp_total_amount = max(pinigai)
    most_likely_amount_before_taxes = round(tmp_total_amount * tax, 2)
    ## TODO: change for "almost equal": abs(v1 - v2) <= allowed_error
    ## TODO 2: if there cant identify total amount and without tax, try another largest amount
    if most_likely_amount_before_taxes in pinigai:
        total_amount = tmp_total_amount
        amount_before_taxes = most_likely_amount_before_taxes
        total_taxes = total_amount - amount_before_taxes
        return total_amount, amount_before_taxes, total_taxes
    else:
        print("Cant identify amounts, please write more rules")
        return 0, 0, 0


def main(path: str):
    p = re.compile(r'\b\d{1,3}(?:\.\d{3})*,\d+\b')
    results = {}

    nlp = spacy.load("./output/model-last/")
    image = read_image(path)
    gray, contours = convert_image_to_contours(image)
    entities, coordinates = get_text_from_contour(contours, gray, image, nlp)
    imoniu_list = [(imones_ent, cord) for (imones_ent, cord) in zip(entities, coordinates) if imones_ent[1] == 'imone']

    pinigai = [float(re.findall(p, pinigai_ent[0])[0].replace(',', '.')) for pinigai_ent in entities if pinigai_ent[1] == 'pinigai']
    results['total_amount'], results['amount_before_taxes'], results['total_taxes'] = get_total_amount_and_amount_before_taxes(pinigai)


    if imoniu_list > 2:
        imoniu_combo = [x for x in zip(imoniu_list, imoniu_list[1:] + imoniu_list[:1])]

    return print('ye')

if __name__ == '__main__':
    main(path="./data/raw_images/Tele2-1.jpg") # VST_0215333_2022_3-1.jpg






#
# ## TODO: nustatyti moketoja ir tiekeja pagal ju realityvias pozicijas
# imones = []
# # imoniu_coords = []
# for ent, cord in zip(results, coords):
#     if ent[1] == 'imone':
#         imones.append([ent, cord])
#         # imoniu_coords.append(cord)
#
# define_moketojas_tiekejas(imoniu_coords[2], imoniu_coords[1], imones[2], imones[1])