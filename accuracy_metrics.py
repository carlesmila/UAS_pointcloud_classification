##############################################################################
#                             Accuracy metrics                               #                         #      
##############################################################################


import geopandas as gpd
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pylab as plt
import sklearn.metrics as mtrcs
import numpy as np

# Read data
acc = gpd.read_file('acc_assessment.shp')
predicted = acc['ground'].to_list()
actual = acc['true'].to_list()
predicted = [int(i) for i in predicted] 

# Accuracy
print("Overall accuracy (test data)")
print(mtrcs.accuracy_score(actual, predicted))
# 77%

# Confusion matrix
print("Confusion matrices (test data)")
confmat = confusion_matrix(predicted, actual)
labels = ['barren', 'cropland', 'grassland', 'road', 'shadow', 
          'shrubland', 'trees', 'water', 'water veg.']
plt.figure(figsize = [6, 5])
g = sns.heatmap(confmat, linewidth=0.5, annot=True, cmap='viridis')
g.set_xticklabels(labels, rotation = 90)
g.set_yticklabels(labels, rotation = 0)
plt.title('Confusion matrix')
plt.xlabel('Reference (actual)')
plt.ylabel('Map (predicted)')
# plt.savefig('conf_matrix.png', dpi = 300, bbox_inches='tight')
plt.close()

# Producer confusion matrix (standardised by column)
prodmat = confmat/ confmat.sum(axis=0)
prodacc = prodmat.round(2).diagonal()

# User confusion matrix (standardised by row)
usermat = confmat/ 30
useracc = usermat.round(2).diagonal()

# Visualization
accs_viz =  np.stack((prodacc, useracc))

plt.figure(figsize = [8, 3])
plt.title('Detailed producer and user accuracy')
g = sns.heatmap(accs_viz, linewidth=0.5, annot=True, cmap='viridis')
g.set_xticklabels(labels, rotation = 90)
g.set_yticklabels(['Producer', 'User'], verticalalignment='center')
# plt.savefig('accuracies.png', dpi = 300, bbox_inches='tight')
plt.close()