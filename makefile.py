#############################################################################
#                  Makefile point cloud classification                      #
#############################################################################

# Pre-processing
exec(open('prepro_uav.py').read())
 
# Model fitting
exec(open('fit_model.py').read())

# Prediction
exec(open('predict.py').read())

# Accuracy sampling
exec(open('accuracy_sampling.py').read())

# Accuracy metrics
exec(open('accuracy_metrics.py').read())