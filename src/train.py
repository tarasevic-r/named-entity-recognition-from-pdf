import random

import spacy
from spacy.tokens import DocBin
from tqdm import tqdm

from src.processing.json_to_spacy import convert_json_to_spacy_v2

data_spacy_v2 = convert_json_to_spacy_v2("./data/labeled_data/text_annotations.json")
shuffled_l = random.sample(data_spacy_v2, k=len(data_spacy_v2))
train_data = shuffled_l[:int(len(data_spacy_v2)*0.83)] # first 80% of shuffled list
test_data = shuffled_l[int(len(data_spacy_v2)*0.83):] # last 20% of shuffled list

nlp = spacy.blank("lt") # load a new spacy model
db = DocBin() # create a DocBin object
for text, annot in tqdm(train_data): # data in previous format
    doc = nlp.make_doc(text) # create doc object from text
    ents = []
    for start, end, label in annot["entities"]: # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    try:
        doc.ents = ents # label the text with the ents
        db.add(doc)
    except:
        print(text, annot)
db.to_disk("./data/train_data/train.spacy") # save the docbin object

# train cl
# python -m spacy train config.cfg --output ./output

## test
import spacy

nlp = spacy.load("./output/model-last/")


doc = nlp(sentence) # some test sentence

from spacy import displacy
displacy.render(doc, style=”ent”, jupyter=True)
