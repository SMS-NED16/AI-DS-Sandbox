from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from preprocessing import extract_features
from collections import Counter
import numpy as np

def do_ml(ticker):
	"""Trains three different classifiers and returns their classification accuracy
	for the """
	# Extract features and labels
	X, y, df = extract_features(ticker)
	y.reshape(len(y), )

	# Train test split - 0.75/0.25
	# X is pct change data for all companies, including company represented by `ticker`
	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.25)


	# Create, train, and test a KNN classifier
	# (clf_kn, confidence_kn, predictions_kn) = do_ml_kn(ticker, X_train, y_train, X_test, y_test)

	# Voting Classifier (three different types)	
	clf = VotingClassifier([
		('lsvc', svm.LinearSVC()), 
		('KNN', neighbors.KNeighborsClassifier()),
		('rfor', RandomForestClassifier())])

	clf.fit(X_train, y_train)
	confidence = clf.score(X_test, y_test)
	print('Accuracy: ', confidence)
	predictions = clf.predict(X_test)
	print("Prediction Spread: ", Counter(predictions))

	return confidence

do_ml('BAC')

"""End note: We created a voting classifier, which takes three different types of classifiers 
and makes a final predicted label based on the predictions made by each individual classifier. 
So, for instance, if 2/3 classifiers predict 1 for a label while the remaining predicts 0, 
the actual predicted label will be 1. 

Using these classifiers, we are able to achieve an accuracy of 39% - 43% when trying to predict
whether we should buy, sell, or hold a specific stock. What this means is that we're able
to predict correctly when to buy, hold, or sell the stock for a specific company 39% - 43% of the 
time.""" 