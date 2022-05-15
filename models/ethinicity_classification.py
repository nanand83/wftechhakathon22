import pickle
import os

base_dir = os.path.dirname(__file__)
classifier = pickle.load(open(base_dir+'/race/race_model.sav', 'rb'))
cv = pickle.load(open(base_dir+'/data/corpus.sav', 'rb'))

def identifyEthinicity(name, verbose=False):
    name = cv.transform([name]).toarray()
    predval = classifier.predict(name)
    predprob = classifier.predict_proba(name)
    #print('Race: '+predval[0])
    classes = classifier.classes_
    if verbose:
        print('Confidences...')
        for i in range(len(classes)):
   	        print(f'{classes[i]}: {predprob[0][i]*100}%')

    return predval[0]


if __name__ == "__main__":
    print(identifyEthinicity('Walter Chiang'))
