##############################################################################
#                 Fit RF model for point cloud classification                #
##############################################################################

import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics as mtrcs
import matplotlib.pyplot as plt

# Tracking message
print("Fitting model...")

# Extract features and labels
prednames = ['z', 'red', 'green', 'blue', 'ground', 'dsm_sd9']
X = training.loc[:, prednames]
y = training.loc[:, ['class']].values.ravel()
training['class'].value_counts()

# Define model with 500 decision trees
rf = RandomForestClassifier(n_estimators = 500, random_state = 0,
                            max_depth = 5, max_features = 'sqrt')

# Train the model on training data
rf.fit(X, y)

# Use the forest's predict method on the test data
preds = rf.predict(X)

# Accuracy
print("Overall accuracy (training data)")
print(mtrcs.accuracy_score(y, preds))

# Feature importance metrics
print("Variable importance")
importances = rf.feature_importances_
std = np.std([tree.feature_importances_ for tree in rf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]
plt.figure(figsize = [6, 4])
plt.title("Feature importances")
plt.bar(range(X.shape[1]), importances[indices],
        color="r", yerr=std[indices], align="center")
plt.xticks(range(X.shape[1]), [x for y, x in sorted(zip(indices, prednames))])
plt.xlim([-1, X.shape[1]])
# plt.savefig('var_importance.png', dpi = 300, bbox_inches='tight')


# Clean
del X, importances, indices, prednames, preds, std, training, y