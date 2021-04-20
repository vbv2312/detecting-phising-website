import joblib
import FeatureExtraction

# load the pickle file
classifier1 = joblib.load('MODELS/logistic_model.pkl')
classifier2 = joblib.load('MODELS/logistic_model.pkl')


def predict(url):
    # print("HI")
    feature = FeatureExtraction.extractFeatures(url)
    #print(feature)
    prediction1 = classifier1.predict([feature[1:]])
    prediction2 = classifier1.predict([feature[1:]])
    return (prediction1[0],prediction2[0])