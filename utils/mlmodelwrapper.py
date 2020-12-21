#%%
import threading
from datetime import datetime
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# import sklearn classification models
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

from sklearn.utils import all_estimators
from sklearn.model_selection import train_test_split

# TODO: use different hyperparameters according to data or try out a few settings and find best of it.
# models
models = {
    "Nearest Neighbors": KNeighborsClassifier(),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(),
    "Neural Net": MLPClassifier(),
    "AdaBoost": AdaBoostClassifier(),
    "Naive Bayes": GaussianNB(),
    "QDA": QuadraticDiscriminantAnalysis(),
    "Linear SVM": SVC(kernel="linear", C=0.025),
    "RBF SVM": SVC(gamma=2, C=1),
    "Gaussian Process": GaussianProcessClassifier(1.0 * RBF(1.0)),
}

classifier_names = [
    "Nearest Neighbors",
    "Decision Tree",
    "Random Forest",
    "Neural Net",
    "AdaBoost",
    "Naive Bayes",
    "QDA",
    "Linear SVM",
    "RBF SVM",
    "Gaussian Process",
]

RANDOM_SEED = 0


class MLModelWrapper:
    def __init__(self, X_np, y_np):
        self.train_X, self.test_X, self.train_y, self.test_y = train_test_split(
            X_np, y_np, test_size=0.25, random_state=RANDOM_SEED
        )

    # filter_type can be one of the type ['classifier', 'regressor', 'cluster', 'transformer']
    def quick_test(self, filter_type="classifier", save=True):
        print("*Quick test for multiple classification models!")
        threads = []
        for name, clf_class in all_estimators(filter_type):
            print(f"*start training: {name} model.")
            try:
                clf = clf_class()
                thread = TrainModelThread(
                    self.train_X,
                    self.train_y,
                    self.test_X,
                    self.test_y,
                    clf,
                    name,
                    save,
                )
                threads.append(thread)
                thread.start()
            except:
                print(f"*Failed to initialize model: {name}.")

        for thread in threads:
            thread.join()
        print("*Training of all classification models are finished!")


class TrainModelThread(threading.Thread):
    def __init__(self, train_X, train_y, test_X, test_y, clf, name=None, save=True):
        threading.Thread.__init__(self)
        self.train_X = train_X
        self.train_y = train_y
        self.test_X = test_X
        self.test_y = test_y
        self.clf = clf
        self.name = name
        self.save = save

    def run(self):
        self.clf.fit(self.train_X, self.train_y)
        y_pred = self.clf.predict(self.test_X)
        report = classification_report(self.test_y, y_pred)
        if self.name != None:
            print(f"Method: {self.name}")
        print(report)
        if self.save:
            print("*Append result to ML_Classifiers_Report.txt")
            with open("ML_Classifiers_Report.txt", "a") as ofile:
                if self.name != None:
                    ofile.write(f"Method: {self.name}\n")
                ofile.write(f"finished time: {datetime.now()}\n")
                ofile.write(report)
                ofile.write("-" * 20 + "\n")
        print("-" * 20)
