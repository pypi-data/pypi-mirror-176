import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm

X, y = datasets.load_iris(return_X_y=True)
print(type(X),type(y))
print(X.shape, y.shape)
print(X)
print(y)