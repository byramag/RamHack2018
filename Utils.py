from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import sklearn.metrics as skl_metrics


import random
import copy

class Utils:
   
    def get_classifier(self, name):
        if name == "Decision Tree":
            return tree.DecisionTreeClassifier(criterion = "entropy", random_state = 1)
        elif name == "Naive Bayes":
            return GaussianNB()
        elif name == "SVM":
            return SVC(C = 10)
        else:
            print("Unknown classifier name provided!")
            return None
     
    
     
    
    def get_accuracy(self, y_true, y_pred):
        return skl_metrics.accuracy_score(y_true, y_pred)*100
    
    def get_fmeasure(self, y_true, y_pred):
        return skl_metrics.f1_score(y_true, y_pred, average = 'macro') * 100
   
    def get_precision(self, y_true, y_pred):
        return skl_metrics.precision_score(y_true, y_pred, average = 'macro') * 100
    
    def get_recall(self, y_true, y_pred):
        return skl_metrics.recall_score(y_true, y_pred, average='macro') * 100

    def get_sensitivity_tc(self, y_true, y_pred):
        return imb_metrics.sensitivity_score(y_true, y_pred, average = 'binary') * 100

    def get_specificity_tc(self, y_true, y_pred):
        return imb_metrics.specificity_score(y_true, y_pred, average = 'binary') * 100
    
     