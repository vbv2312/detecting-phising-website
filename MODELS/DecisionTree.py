from sklearn.tree import DecisionTreeClassifier
import joblib
from sklearn.metrics import confusion_matrix
import time
from sklearn.model_selection import train_test_split

def d_tree(x_train, x_test, y_train, y_test):
    # instantiate the model
    tree = DecisionTreeClassifier(max_depth=12)
    # fit the model
    tree.fit(x_train, y_train)
    # time
    start = time.time()
    y_predictions = tree.predict(x_test)
    stop = time.time()
    mat = confusion_matrix(y_test, y_predictions)
    accuracy = (mat[0][0] + mat[1][1]) * 100 / (mat[0][0] + mat[0][1] + mat[1][0] + mat[1][1])
    joblib.dump(tree, 'MODELS/decision_tree_model.pkl')
    details = "DecisionTree \t" + str(accuracy) + "\t" + str((stop - start) * 1000) + "ms\n"
    f = open("model_details.txt", "a")
    f.write(details)
    f.close()


def model(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    d_tree(x_train, x_test, y_train, y_test)