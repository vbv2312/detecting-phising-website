import joblib
import FeatureExtraction

# load the pickle file
classifier = joblib.load('MODELS/logistic_model.pkl')


def predict(url):
    # print("HI")
    feature = FeatureExtraction.extractFeatures(url)
    #print(feature)
    prediction = classifier.predict([feature[1:]])
    return (prediction[0])