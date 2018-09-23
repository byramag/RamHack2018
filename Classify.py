import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm

iris = datasets.load_iris()

X_train, X_test, y_train, y_test = train_test_split( iris.data, iris.target, test_size=0.1, random_state=0 )

classifier = Utils.get_classifier("Naive Bayes").fit(X_train, y_train)
NBscores = classifier.score(X_test, y_test)

classifier = Utils.get_classifier("Decision Tree").fit(X_train, y_train)
RFscores = classifier.score(X_test, y_test)

classifier = Utils.get_classifier("SVM").fit(X_train, y_train)
SVMscores = classifier.score(X_test, y_test)