import joblib
import FeatureExtraction
import sys

# load the pickle file
classifier = joblib.load('../MODELS/logistic_model.pkl')


def predict(url):
    # print("HI")
    feature = FeatureExtraction.extractFeatures(url)
    print(feature)
    prediction = classifier.predict([feature[1:]])
    print(prediction[0])
    return (prediction[0])


if __name__ == "__main__":
    print("h1")
    f = open("data/answer.txt", "w")
    f.write(str(predict(sys.argv[1])))
