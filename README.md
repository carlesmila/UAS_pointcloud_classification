# UAS: Point cloud classification (IFGI project 2020)

## Introduction

This repository contains the code used to perform supervised classification for the UAS project as a part of the work performed by the 3D data team. 
This project was conducted during the summer semester 2020 in IFGI (University of Münster), in which UAV data (RGB + MS) was collected to study
the renaturation process of the river Aa in the segment near the Aa lake in Münster, Germany. The 3D data team analysed 3D data including point clouds 
and digital elevation/terrain models to study a series of morphological characteristics of the river. To do so, a preliminary classification of the point
cloud was required.

## Structure

The code is structured in the following scripts:
* **makefile.py**: Calls the individual parts of the workflow in an ordered manner.
* **prepro_uav.py**: Pre-processes the point cloud training data. It reads and cleans them, and adds additional predictors from rasters.
* **fit_model.py**: Fits a random forest model using scikit-learn and generates a variable importance plot.
* **predict.py**: Reads and cleans all point cloud data for predictions. It generates predictions and writes results to disk.
* **accuracy_sampling.py**: Performs stratified sampling for later accuracy assessment and writes to disk.
* **accuracy_metrics.py**: Computes statistical and graphical summary metrics of model performance.

As an additional script, **tools_uav.py** defines a function which is used repeatedly in the project to read a las file and convert it to a geopandas object (vector).

## Classes

The 9 classes considered in these classification exercise (with classification codes) are as follows:
1. Bare soil
2. Cropland
3. Grassland
4. Road
5. Shadow
6. Shrubland
7. Trees
8. Water
9. Water vegetation.

## Predictors

The following predictors were used for classification:
1. Red
2. Green
3. Blue
4. Altitude
5. Automatic ground classification (LAStools)
6. Local altitude Standard Deviation derived from DSM.

## Algorithm

A Random Forest algorithm (500 trees) with a maximum depth of 5 was used for classification.

## Training samples

Training samples were selected using visual inspection in CloudCompare.

## Accuracy assessment

We used stratified sampling using the classified point cloud to extract 30 points per class for accuracy assessment.

## Disclaimer

The code included in this repository is shown publicly for educational purposes only. Please do not use or distribute without the owner's consent.
None of the data used in the exercise in included because of confidentiality reasons.