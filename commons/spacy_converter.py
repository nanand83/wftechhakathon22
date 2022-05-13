import json
import spacy
import random
from pathlib import Path
import random
from pathlib import Path
import spacy
from tqdm import tqdm

fo = open("admin.jsonl", "r")
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
        for text, annotations in tqdm(TRAIN_DATA):
            nlp.update(
                [text],
                [annotations],
                drop=0.5,
                sgd=optimizer,
                losses=losses)
        print(losses)