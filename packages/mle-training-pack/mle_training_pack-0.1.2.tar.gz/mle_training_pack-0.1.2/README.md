# Median housing value prediction

The housing data can be downloaded from https://raw.githubusercontent.com/ageron/handson-ml/master/. The script has codes to download the data. We have modelled the median house value on given housing data. 

The following model has been used: 

 - Random Forest

## Steps performed
 - We prepare and clean the data. We check and impute for missing values.
 - Features are generated and the variables are checked for correlation.
 - Multiple sampling techinuqies are evaluated. The data set is split into train and test.
 - All the above said modelling techniques are tried and evaluated. The final metric used to evaluate is mean squared error.


# Installation
# from pyp
pip install mle_training_pack 
# from .whl file
pip install mle_training_pack-0.1.1-py3-none-any.whl

## To excute the script
# Raw data Output Path
extract_data --raw_data_op <>


# Processed data Input Path
extract_data --processed_data_ip <>

# Path for trained model to be stored
train_model --model_op <>

# Path to load stored model for scoring
score_test --model_ip <>

# Path to load scoring dataset
score_test --test_data_ip <>

# Path to save model predictions
score_test --test_data_op <>
