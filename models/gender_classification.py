import pickle
import os

base_dir = os.path.dirname(__file__)
classifier = pickle.load(open(base_dir+'/gender/gender_model2.sav', 'rb'))
cv = pickle.load(open(base_dir+'/data/corpus.sav', 'rb'))


def getGender(name, verbose=False):
    name = cv.transform([name]).toarray()
    predval = classifier.predict(name)
    predprob = classifier.predict_proba(name)

    if verbose:
        print('Gender: ' + predval[0])
        if predval[0] == 'm':
            print(f'Confidence : {predprob[0][1] * 100}%')
        else:
            print(f'Confidence : {predprob[0][0] * 100}%')

    return predval[0]


if __name__ == "__main__":
    print(getGender('David Miller'))
