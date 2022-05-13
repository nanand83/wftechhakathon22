import json
import random
from pathlib import Path
import spacy
from spacy.training import Example

filename = 'awards'
fo = open(filename+".jsonl", "r")
TRAIN_DATA = []
lines = fo.readlines()
print(len(lines))
for line in lines:
    line = json.loads(line)
    if "labels" in line:
        line["entities"] = line.pop("labels")
    elif "label" in line:
        line["entities"] = line.pop("label")
    else:
        line["entities"] = []


    tmp_ents = []



    for e in line["entities"]:
        if e[2] in ['diversity']:
            #tmp_ents.append("(" + str(e[0]) + "," + str(e[1]) + ",'" + str(e[2])+ "')")
            tmp_ents.append((e[0],e[1], e[2]))
            line["entities"] = tmp_ents
            #print((line["data"], {'entities': line["entities"]}))

    TRAIN_DATA.append((line["data"], {'entities': line["entities"]}))


print("[INFO] Stored the spacy training data and  filename is {}".format("spacy_training".replace('json', 'txt')))

model = None
output_dir=Path(".")
n_iter=100

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')
    print("Created blank 'en' model")

#set up the pipeline

if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for raw_text, entity_offsets in TRAIN_DATA:
            doc = nlp.make_doc(raw_text)
            example = Example.from_dict(doc, entity_offsets)
            nlp.update([example], sgd=optimizer)
        print(losses)
    nlp.to_disk("output/"+filename)

doc = nlp("Top 50 Houston Fastest Growing Woman-Owned Businesses – Houston Business Journal.")
print("Entities", [(ent.text, ent.label_) for ent in doc.ents])