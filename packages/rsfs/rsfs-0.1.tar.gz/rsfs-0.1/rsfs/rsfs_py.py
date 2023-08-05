import numpy
import numpy.matlib
import time
import math

from sklearn.model_selection import train_test_split

from rsfs import clf
from scipy.stats import norm
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def RSFS(train_data, test_data, label_train, label_test, parameters):
    """
    Main function where the RSFS logic is written

    Args:
        train_data (numpy.ndarray): This matrix contains the train data.
        test_data (numpy.ndarray): This matrix contains the test data.
        label_train (numpy.ndarray): This array contains the labels of the train data.
        label_test (numpy.ndarray): This array contains the labels of the test data. This is used to get accuracy of
                                    classifier for full dataset and the reduced dataset.
        parameters (dict): Dictionary of all RSFS parameters. They are as follows:
            Verbose: Displays the output of execution if set to 1.
            RSFS (dict):
                maxiters (int): An iteration limit for hard cutoff of the logic.

                Dummy feats (int): This value is generally equal to the number of features in the dataset.

                delta (double): This value controls the acceptable variation limit within which the algorithm is said to be
                        converged.

                cutoff (double): This is the cutoff value which decides how "relevant" the features should be to the dataset for
                        them to be selected in the featureset. Generally the default value is 0.99

                Threshold (int): This value states the sampling rate of the algorithm i.e, "How many iterations later
                            should the checking be done to see if the algorithm is converged?"

                fn (str): Two possible values: 'sqrt' or '10log'. This determines the number of features that will be
                 randomly selected per iteration.

                    'sqrt' selects sqrt of total number of features, randomly in each iteration while creating the random
                    subset

                    '10log' selects the 10* log of total number of features, randomly in each iteration while creating
                    the random subset.

                Classifier (str): There are 4 possible values for this parameter.

                    'KNN' - This selects the KNearestNeigbours classifier from scikit-learn library.
                    'SVM' - This selects the SupportVectorClassifier from scikit-learn library.
                    'GNB' - This selects the Gaussian Naive Bayes classifier from the scikit-learn library.
                    'RF' - This selects the Random Forest Classifier from the scikit-learn library.

                Classifier Properties (dict): This dictionary contains the kwargs that will be sent to the classifier
                 object that is created from the 'Classifier' property. These values must be recognizable by the
                 scikit-learn library else an error will be thrown.


    Returns:
        (dict):
            F_RSFS (int): The feature numbers of the dataset which are important to the dataset.
            W_RSFS (int): The numeric value of the relevance of the corresponding feature.
            iteration (int): The number of iterations taken by the algorithm before convergence.

    Example:
        Parameters = {

        'RSFS': {

            'Classifier': 'KNN',

            'Classifier Properties': {

                'n_neighbors': 3,

                'weights': 'distance'

            },

            'Dummy feats': 100,

            'delta': 0.05,

            'maxiters': 300000,

            'fn': 'sqrt',

            'cutoff': 0.99,

            'Threshold': 1000,

        },

        'Verbose': 1
    }
    """
    max_iters = parameters['RSFS']['maxiters']
    n_dummyfeats = parameters['RSFS']['Dummy feats']
    max_delta = parameters['RSFS']['delta']
    verbose = parameters['Verbose']
    cutoff = parameters['RSFS']['cutoff']
    Threshold = parameters['RSFS']['Threshold']

    label_test = label_test.astype('int')
    label_train = label_train.astype('int')

    N_classes = len(numpy.unique(label_train))
    number_of_features = numpy.size(train_data, axis=1)
    relevance = numpy.zeros((number_of_features,))
    dummy_relevance = numpy.zeros((n_dummyfeats,))

    train_data = preprocessing.scale(train_data)
    test_data = preprocessing.scale(test_data)

    if parameters['RSFS']['fn'] == 'sqrt':
        feats_to_take = round(math.sqrt(number_of_features))
        # feats_to_take = feats_to_take.astype('int')
        dummy_feats_to_take = round(math.sqrt(n_dummyfeats))
        # dummy_feats_to_take = dummy_feats_to_take.astype('int')
    if parameters['RSFS']['fn'] == '10log':
        feats_to_take = round(10 * math.log10(number_of_features))
        # feats_to_take = feats_to_take.astype('int')
        dummy_feats_to_take = round(10 * math.log10(n_dummyfeats))
        # dummy_feats_to_take = dummy_feats_to_take.astype('int')

    feat_N = numpy.zeros(max_iters)

    totcorrect = numpy.zeros(N_classes)
    totwrong = numpy.zeros(N_classes)

    iteration = 1
    deltaval = math.inf

    probs = numpy.zeros(numpy.shape(relevance))
    while iteration <= max_iters and deltaval > max_delta:
        feature_indices = numpy.floor(number_of_features * numpy.random.rand(1, feats_to_take))
        feature_indices = feature_indices.astype('int')

        class_hypos = clf.classifier_2(train_data[:, numpy.resize(feature_indices, (numpy.size(feature_indices),))],
                                       test_data[:, numpy.resize(feature_indices, (numpy.size(feature_indices),))],
                                       label_train,
                                       parameters)

        correct = numpy.zeros(N_classes)
        wrong = numpy.zeros(N_classes)

        for j in list(numpy.arange(0, numpy.size(label_test))):
            if label_test[j] == class_hypos[j]:
                correct[label_test[j] - 1] = correct[label_test[j] - 1] + 1
            else:
                wrong[label_test[j] - 1] = wrong[label_test[j] - 1] + 1

        totcorrect = totcorrect + correct
        totwrong = totwrong + wrong

        performance_criterion = numpy.mean(numpy.array(correct) * 100 / (numpy.array(correct) + numpy.array(wrong)))
        expected_criterion_value = numpy.mean(
            numpy.array(totcorrect) * 100 / (numpy.array(totcorrect) + numpy.array(totwrong)))

        target = performance_criterion - expected_criterion_value
        pos = feature_indices
        relevance[pos] += target

        dummy_indices = numpy.floor(n_dummyfeats * numpy.random.rand(1, dummy_feats_to_take))
        dummy_indices = dummy_indices.astype('int')
        target = dummy_relevance[dummy_indices] + performance_criterion - expected_criterion_value
        pos = dummy_indices
        for x, y in zip(pos, target):
            dummy_relevance[x] = y

        probs = norm.cdf(relevance, loc=numpy.mean(dummy_relevance), scale=numpy.std(dummy_relevance))
        feat_N[iteration] = numpy.size(numpy.where(probs > cutoff))
        if iteration % Threshold == 0:
            deltaval = numpy.std(feat_N[iteration - (Threshold - 1):iteration]) / numpy.mean(
                feat_N[iteration - (Threshold - 1):iteration])
            if verbose == 1:
                print('RSFS: ', feat_N[iteration], 'features chosen so far (iteration: ', iteration, '/', max_iters,
                      '). Delta: ', deltaval)

        iteration = iteration + 1

    S = numpy.where(probs > cutoff)
    W = relevance[S]
    return {'F_RSFS': S, 'W_RSFS': W, 'iteration': iteration}


def Compare_RSFS(Feature_train, Feature_test, label_train, label_test, Parameters):
    """
    This function is a wrap around method of RSFS() function. Using this method, accuracy of the original dataset and
    the reduced dataset can be compared.

    Args:
        Feature_train (numpy.ndarray): This matrix contains the train data.
        Feature_test (numpy.ndarray): This matrix contains the test data.
        label_train (numpy.ndarray): This array contains the labels of the train data.
        label_test (numpy.ndarray): This array contains the labels of the test data. This is used to get accuracy of
                                    classifier for full dataset and the reduced dataset.
        Parameters (dict): This parameter dictionary will be passed on to the RSFS function. Check the documentation in that
                                    function


    Returns:
        (dict):
            Orig (dict): This part of the dictionary contains the statistics of execution that are obtained on the full dataset

                Accuracy (double): This value lies between 0 and 100.

                F1 score (double): This value lies between 0 and 100. If the number of labels is more than 2, the
                                    weighted average of F1 score will be returned.

                Features (int): Number of features in the given dataset.

                Time (int): Time taken by the classifier for classification task.

            RSFS (dict): This part of the dictionary contains the statistics of execution that are obtained on the
                        reduced dataset

                Accuracy (double): This value lies between 0 and 100.
                F1 Score (double): This value lies between 0 and 100.
                Time (double): Time taken by the RSFS function to execute the algorithm.
                Iteration (int): Number of iterations taken by the RSFS algorithm for convergence.
                Feats (List): List of feature numbers from the dataset which are most accurately represent the dataset.
                Weights (List): The corresponding values of relevance/importance of the features.

    This function need not be used always while using RSFS. This function only gives an idea about how the data is going
    to perform if RSFS is used. Once the flow of execution is finalized, the data can directly be sent to RSFS() for
    dimensionality reduction.

    Example:
        Parameters = {

        'RSFS': {

            'Classifier': 'KNN',

            'Classifier Properties': {

                'n_neighbors': 3,

                'weights': 'distance'

            },

            'Dummy feats': 100,

            'delta': 0.05,

            'maxiters': 300000,

            'fn': 'sqrt',

            'cutoff': 0.99,

            'Threshold': 1000,

        },

        'Classifier': 'KNN',

        'Classifier Properties':
        {
            'n_neighbors': 3
        },

        'Verbose': 1
    }
    """
    t1 = time.time()
    Res = RSFS(Feature_train, Feature_test, label_train, label_test, Parameters)
    t2 = time.time()
    F_RSFS = Res['F_RSFS']
    W_RSFS = Res['W_RSFS']
    iteration = Res['iteration']
    RSFS_time = t2 - t1

    t1 = time.time()
    hypos_orig = clf.classifier_1(Feature_train, Feature_test, label_train, Parameters)
    Original_Accuracy = accuracy_score(hypos_orig, label_test) * 100
    t2 = time.time()
    Orig_time = t2 - t1

    if Parameters['Verbose'] == 1:
        print('Original :', numpy.size(Feature_train, axis=1), 'features: ', Original_Accuracy, '% correct.')

    hypos_RSFS = clf.classifier_1(Feature_train[:, numpy.resize(F_RSFS, (numpy.size(F_RSFS),))],
                                  Feature_test[:, numpy.resize(F_RSFS, (numpy.size(F_RSFS),))], label_train, Parameters)
    RSFS_Accuracy = accuracy_score(hypos_RSFS, label_test) * 100
    if len(numpy.unique(label_test)) > 2:
        RSFS_F1 = f1_score(hypos_RSFS, label_test, average='weighted') * 100
        Original_F1 = f1_score(hypos_orig, label_test, average='weighted') * 100
    else:
        RSFS_F1 = f1_score(hypos_RSFS, label_test) * 100
        Original_F1 = f1_score(hypos_orig, label_test) * 100

    if Parameters['Verbose'] == 1:
        print('RSFS feature set (', numpy.size(F_RSFS), ' features):', RSFS_Accuracy, '% correct')

    Result = {
        'Orig': {
            'Accuracy': Original_Accuracy,
            'F1 score': Original_F1,
            'Features': numpy.size(Feature_train, axis=1),
            'Time': Orig_time
        },
        'RSFS': {
            'Accuracy': RSFS_Accuracy,
            'F1 score': RSFS_F1,
            'Time': RSFS_time,
            'Iteration': iteration,
            'Feats': F_RSFS,
            'Weights': W_RSFS,
        }
    }
    return Result

if __name__ == '__main__':
    Data = numpy.loadtxt(open(str('../Isolet.csv'), "rb"), delimiter=",", skiprows=1)
    labels = Data[:, -1]
    Data = Data[:, :-1]
    train, test, train_labels, test_labels = train_test_split(
        Data, labels, test_size=0.33, random_state=42, stratify=labels)
    data_train = train
    data_test = test
    label_train = train_labels
    label_test = test_labels
    Parameters = {
        'RSFS': {
            'Classifier': 'KNN',
            'Classifier Properties': {
                'n_neighbors': 3,
                'weights': 'distance'
            },
            'Dummy feats': 100,
            'delta': 0.05,
            'maxiters': 300000,
            'fn': 'sqrt',
            'cutoff': 0.99,
            'Threshold': 1000,
        },
        'Verbose': 1
    }
    print(RSFS(train,test,train_labels,test_labels,Parameters))