#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
"""
Created on Fri Nov 30 20:05:47 2018

@author: jaywalker
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:45:46 2018

@author: jaywalker
"""

import sys
import csv
import io
import math
import random
import pickle

import numpy
import matplotlib.pyplot as plt
from sklearn.learning_curve import learning_curve
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score

#SCale features. Uses default scaling provided by sklearn.
def scaleFeatures(listOfRows):
    return preprocessing.scale(listOfRows)

#Loads a CSV file in to memory as a list of lists.
#filename: the CSV file to load
#omitHeader: Drop or include the first row of the CSV in the returned lists.
def loadCSV(filename, omitHeader=False):
    with io.open(filename, encoding="ISO-8859-1") as tsvFile:
        csvReader = csv.reader(tsvFile, delimiter='\t', quotechar='\"')
        rowList = [list(row) for row in csvReader]
        
        if (omitHeader):
            rowList.pop(0)
            
        return rowList
            
#Input a vector of reals and ouput a one-hot vector indicating the max element
def maxVector(inVector):
    maxIndex = 0
    maxValue = -999999
    for i in range(0, len(inVector)):
        if inVector[i] > maxValue:
            maxIndex = i
            maxValue = inVector[i]
            
    for i in range(0, len(inVector)):
        if i == maxIndex:
            inVector[i] = 1
        else:
            inVector[i] = 0
            
    return inVector
 
#Trains a classifier on data in X with labels Y using nFolds for cross validation. Also plots a learning curve. 
#Returns a 2-element list of classifier accuracy and f1-score values.
#X: training data
#Y: labels for training data
#classifier: SkLearn classifier object such as MLPClassifier, etc. 
#nFolds: number of folds to use for cross validation.    
def foldTrainTest(X, Y, classifier, nFolds=10):
    kf = KFold(n_splits=nFolds) #maybe try the shuffle param on the activity recognition stuff?
    correct = 0
    outOf = 0
    f1Subtotal = 0
    for train_index, test_index in kf.split(X):
        Xtrain, Xtest = X[train_index], X[test_index]
        Ytrain, Ytest = Y[train_index], Y[test_index]
        
        #checking to make sure test and train sets are disjoint
        #print("train indices: " + str(train_index))
        #print("test indices: " + str(test_index))
        
        outOf += len(Ytest) #average accuracy will be calculated as (correct / outOf)
        classifier.fit(Xtrain, Ytrain)

        response = classifier.predict(Xtest)
        f1Subtotal += f1_score(Ytest, response, average='micro')
        for i in range(0,len(Xtest)):
            if response[i] == Ytest[i]:
                correct += 1
    
    plotLearningCurve(classifier, classifier.__class__.__name__, X, Y)#, cv=kf.split(X))
    
    return [correct / outOf, f1Subtotal / nFolds]

#Set up MLP classifier and train it using the foldTrainTest function.
#X: training examples
#Y: labels
#nFolds: number of folds to use for cross validation
def testMLPC(X, Y, nFolds=10):
    #construct the neural network 
    numFeatures = len(X[0])
    #architectureTuple = (numFeatures, int(math.floor((3/4)*numFeatures)), int(math.floor((1/2)*numFeatures)))
    #architectureTuple = (numFeatures, int(math.floor((3/4)*numFeatures)), int(math.floor((1/2)*numFeatures)), int(math.floor((1/4)*numFeatures)))
    architectureTuple = (numFeatures, numFeatures)
    #architectureTuple = (numFeatures)
    #architectureTuple = (numFeatures * 2, numFeatures, int(math.floor((3/4)*numFeatures)), int(math.floor((1/2)*numFeatures)), int(math.floor((1/4)*numFeatures)))
    print("Hidden layer sizes: " + str(architectureTuple))
    mlp = MLPClassifier(activation='relu', hidden_layer_sizes=architectureTuple, max_iter=200)
    accuracy, f1 = foldTrainTest(X, Y, mlp, nFolds)
    print("MLPC Accuracy (" + str(nFolds) + "-fold):" + str(accuracy) + ", F1-Score: " + str(f1))

#this function is essentially verbatim from: http://scikit-learn.org/0.15/auto_examples/plot_learning_curve.html
def plotLearningCurve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=numpy.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and traning learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : integer, cross-validation generator, optional
        If an integer is passed, it is the number of folds (defaults to 3).
        Specific cross-validation objects can be passed, see
        sklearn.cross_validation module for the list of possible objects

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = numpy.mean(train_scores, axis=1)
    train_scores_std = numpy.std(train_scores, axis=1)
    test_scores_mean = numpy.mean(test_scores, axis=1)
    test_scores_std = numpy.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt

#Loads a file passed by argument to use for classification
def main(argv):
    X = loadCSV(argv[1], omitHeader=False) #load the un-scaled data set with classificatioins

    #first off, shuffle the order so the classes are interspersed
    #use a predefined seed so that we get the same results repeatedly
    #AND avoid a bug where the KFold classifier doesn't get one of each class later in this script
    random.Random(1).shuffle(X)
    
    #extract classifications from X
    Y = []
    for row in X:
        Y.append(row[len(row) - 1])
        
    #print(Y)
    
    #remove classifications and timestamps from X
    for i in range(0,len(X)):
        X[i] = X[i][:-3]
        
    #print(X)
    Xprepared = scaleFeatures(X)
    
    #print(Y)
    Y = numpy.asarray(Y)
    
    testMLPC(Xprepared, Y)
    #testLogisticRegression(Xprepared, Y)
    #testDecisionTree(Xprepared, Y)

if __name__ == "__main__":
    main(sys.argv)