from src.processing.ocr_image import extract_text_from_contour, get_contour_center

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


def which_is_on_the_top(c1, c2):
    difference = np.subtract(c1, c2)
    return difference


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


def get_text_from_contour(contours, gray, image, nlp) -> [list, list]:
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

    return results, coords