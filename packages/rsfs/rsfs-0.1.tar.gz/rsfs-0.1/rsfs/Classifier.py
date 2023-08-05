import sys
import logging
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier


def classifier_1(Feature_train, Feature_test, label_train, Parameters):
    """
    This function is called from the Compare_RSFS(). This function will perform classification task for the entire
     dataset.
    Args:
        Feature_train (numpy.ndarray)
        Feature_test (numpy.ndarray)
        label_train (numpy.ndarray)
        Parameters (dict)

    Returns:
        (list): Predicted labels of the test data.
    """
    if Parameters['Classifier'] == 'KNN':
        Clf = KNeighborsClassifier(**Parameters['Classifier Properties'])
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    elif Parameters['Classifier'] == 'SVM':
        Clf = SVC(**Parameters['Classifier Properties'])
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    elif Parameters['Classifier'] == 'GNB':
        Clf = GaussianNB()
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    elif Parameters['Classifier'] == 'RF':
        Clf = RandomForestClassifier(**Parameters['Classifier properties'])
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    else:
        if Parameters['Verbose'] == 1:
            print('Classifier not found. Exiting...')
        logging.log(logging.ERROR,'Classifier is not found. Exiting...')
        sys.exit(1)


def classifier_2(Feature_train, Feature_test, label_train, Parameters):
    """
        This function is called from the Compare_RSFS(). This function will
         perform classification task for the entire dataset.
        Args:
            Feature_train (numpy.ndarray)
            Feature_test (numpy.ndarray)
            label_train (numpy.ndarray)
            Parameters (dict)

        Returns:
            (list): Predicted labels of the test data.
        """
    if Parameters['RSFS']['Classifier'] == 'KNN':
        Clf = KNeighborsClassifier(**Parameters['RSFS']['Classifier Properties'])
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    elif Parameters['RSFS']['Classifier'] == 'SVM':
        Clf = SVC(**Parameters['RSFS']['Classifier Properties'])
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    elif Parameters['RSFS']['Classifier'] == 'GNB':
        Clf = GaussianNB()
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    elif Parameters['RSFS']['Classifier'] == 'RF':
        Clf = RandomForestClassifier(**Parameters['RSFS']['Classifier properties'])
        Clf.fit(Feature_train, label_train)
        hypos = Clf.predict(Feature_test)
        return hypos
    else:
        if Parameters['Verbose'] == 1:
            print('Classifier not found. Exiting...')
        logging.log(logging.ERROR, 'Classifier is not found. Exiting...')
        sys.exit(1)