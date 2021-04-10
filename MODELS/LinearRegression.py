from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.metrics import confusion_matrix
import time
from sklearn.model_selection import train_test_split


def logistic(x_train, x_test, y_train, y_test):
    classifier = LogisticRegression(solver='liblinear')
    classifier.fit(x_train, y_train)

    start = time.time()
    y_predictions = classifier.predict(x_test)
    stop = time.time()

    mat = confusion_matrix(y_test, y_predictions)

    accuracy = (mat[0][0] + mat[1][1]) * 100 / (mat[0][0] + mat[0][1] + mat[1][0] + mat[1][1])

    print(accuracy, (stop - start) * 1000)

    joblib.dump(classifier, 'MODELS/logistic_model.pkl')

    details = "LinearRegression \t" + str(accuracy) + "\t" + str((stop - start) * 1000) + "ms\n"

    f = open("model_details.txt", "a")
    f.write(details)
    f.close()


def models(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    logistic(x_train, x_test, y_train, y_test)
