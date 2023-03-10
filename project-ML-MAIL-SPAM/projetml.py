# -*- coding: utf-8 -*-
"""ProjetML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fTiNKBcM5NFeRwgW5yfQ-rbxwnceX55q
"""

#import the dataset
dataset = pd.read_csv('emails.csv')

#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV

dataset.head()

dataset.drop(columns='Email No.', inplace=True)

print(dataset.keys())

dataset.isnull().any().sum()

dataset.describe()

dataset.Prediction.unique()

sns.displot(dataset['Prediction'],kde=False)

"""selection"""

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, -1].values
X.shape

X_new = SelectKBest(chi2, k=2).fit_transform(X, y)
X_new.shape

"""Pretraitement"""

from sklearn.model_selection import train_test_split

X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, -1].values
X.shape

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=101)

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=120, criterion='entropy')
model=rf.fit(X_train,y_train)

from sklearn.metrics import plot_confusion_matrix,classification_report,plot_precision_recall_curve,plot_roc_curve
from sklearn.metrics import accuracy_score

pred = model.predict(X_test)
print("Accuracy Score of Random Forest Classifier : ", accuracy_score(y_test,pred))
plot_confusion_matrix(model,X_test,y_test)
plot_precision_recall_curve(model,X_test,y_test)
plot_roc_curve(model,X_test,y_test)

estimator = model.estimators_[5]
from sklearn.tree import export_graphviz
export_graphviz(estimator, out_file='tree.dot',
                rounded = True, proportion = False, 
                precision = 2, filled = True)
from subprocess import call
call(['dot', '-Tpng', 'tree.dot', '-o', 'tree.png', '-Gdpi=600'])
from IPython.display import Image
Image(filename = 'tree.png')

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=4 , metric='minkowski')
model_knn= knn.fit(X_train,y_train)

pred_knn  = model_knn.predict(X_test)
print("Accuracy Score of KNN Classifier : ", accuracy_score(y_test,pred_knn))
plot_confusion_matrix(model_knn,X_test,y_test)
plot_precision_recall_curve(model_knn,X_test,y_test)
plot_roc_curve(model_knn,X_test,y_test)

rf_params = {'max_depth': range(12, 24, 3), 'min_samples_split': range(3, 13, 2)}
rf_search = GridSearchCV(rf, rf_params, scoring='average_precision', cv=4)
grid_rf=rf_search.fit(X_train, y_train)

print(grid_rf.param_grid)
print(grid_rf.score)

pred_grid= grid_rf.predict(X_test)
print("Accuracy Score of Random Forest Classifier with GridSearch : ", accuracy_score(y_test,pred_grid))
plot_confusion_matrix(grid_rf,X_test,y_test)
plot_precision_recall_curve(grid_rf,X_test,y_test)
plot_roc_curve(grid_rf,X_test,y_test)

k_range = list(range(1, 31))

param_grid = {'n_neighbors' : k_range,'metric':['minkowski','euclidean']}
  
# defining parameter range
grid = GridSearchCV(knn, param_grid, cv=4, scoring='accuracy', return_train_score=False,verbose=1)
  
# fitting the model for grid search
grid_search=grid.fit(X_train, y_train)

print(grid_search.param_grid)
print(grid_search.score)

grid_knn = grid_search.predict(X_test)
print("Accuracy Score of KNN with GridSearch : ", accuracy_score(y_test,grid_knn))
print(classification_report(grid_knn,y_test))
plot_confusion_matrix(grid_search,X_test,y_test)
plot_precision_recall_curve(grid_search,X_test,y_test)
plot_roc_curve(grid_search,X_test,y_test)