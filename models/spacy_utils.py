import spacy
import json

def convert_annotations_to_training_data(file_name):
    fo = open(file_name, "r")
    TRAIN_DATA = []
    lines = fo.readlines()
    #print(len(lines))
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

    return TRAIN_DATA
