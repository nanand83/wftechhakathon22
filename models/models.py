import spacy
from spacy.training import Example
from spacy_utils import convert_annotations_to_training_data
from ethnicolr import pred_wiki_ln, pred_wiki_name
import random
import pandas as pd
import os


class DiversityModel:
    output_base_dir = '/'.join([os.path.dirname(__file__), 'outputs'])
    n_iter = 10
    nlp = None

    def __init__(self, name):
        self.name = name
        self.model_output_dir = '/'.join([self.output_base_dir, name])

    def train_from_annotations(self, annotations_data_file, use_blank_model=True):
        if use_blank_model:
            assert self.nlp is None

        if use_blank_model:
            self.nlp = spacy.blank('en')
            print("Created blank 'en' model")
        else:
            raise "Not supported"

        TRAIN_DATA = convert_annotations_to_training_data(annotations_data_file)

        #set up the pipeline
        if 'ner' not in self.nlp.pipe_names:
            ner = self.nlp.create_pipe('ner')
            self.nlp.add_pipe("ner", last=True)
        else:
            ner = self.nlp.get_pipe('ner')

        for _, annotations in TRAIN_DATA:
            for ent in annotations.get('entities'):
                ner.add_label(ent[2])

        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != 'ner']
        with self.nlp.disable_pipes(*other_pipes):  # only train NER
            optimizer = self.nlp.begin_training()
            for itn in range(self.n_iter):
                random.shuffle(TRAIN_DATA)
                losses = {}
                for raw_text, entity_offsets in TRAIN_DATA:
                    doc = self.nlp.make_doc(raw_text)
                    example = Example.from_dict(doc, entity_offsets)
                    self.nlp.update([example], sgd=optimizer, losses=losses)

                print(losses)

            self.nlp.to_disk(self.output_base_dir + "/" + self.name)

    def predict_single(self, test_data_point):
        if not self.nlp:
            self.nlp = spacy.load(self.model_output_dir)
        
        doc = self.nlp(test_data_point)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        print (entities)
        return entities



class AwardsModel(DiversityModel):
    def __init__(self):
        super().__init__('awards')


class EthnicityOTSModel(DiversityModel):
    def __init__(self):
        super().__init__('ethnicolr_ots')

    def train_from_annotations(self, data):
        raise Exception("Unsupported for Off-the-shelf model")
    
    def predict_batch_by_lastname(self, names, name_col='name'):
        names_list = [{'name' : sanitize(name)} for name in names]
        print (names_list)
        df = pd.DataFrame(names_list)
        return pred_wiki_ln(df, name_col)

def sanitize(name):
    return ''.join([x for x in name if x == ' ' or x.isalnum()])

if __name__ == "__main__":
    a = AwardsModel()
    #a.train_from_annotations('annotations/awards.jsonl')
    #a.predict_single("Top 50 Houston Fastest Growing Woman-Owned Businesses – Houston Business Journal")

    b = EthnicityOTSModel()
    print(b.predict_batch_by_lastname(['Dinesh','Anand','Gokul','Katherine']))
