import joblib
import FeatureExtraction

# load the pickle file
classifier1 = joblib.load('MODELS/logistic_model.pkl')
classifier2 = joblib.load('MODELS/svm.pkl')
classifier3 = joblib.load('MODELS/decision_tree_model.pkl')


def predict(url):
    # print("HI")
    feature = FeatureExtraction.main(url)
    print(url, feature)
    prediction1 = classifier1.predict(feature)
    prediction2 = classifier2.predict(feature)
    prediction3 = classifier3.predict(feature)

    return (prediction1[0],prediction2[0],prediction3[0])
