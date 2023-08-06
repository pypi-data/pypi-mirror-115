import os
import pickle

import numpy as np
import pandas as pd

# from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from mle_training_pack.config import *


def load_housing_data(housing_path=default_rawdata_path):
    """Loads raw data from local path

    Parameters
    ----------
    housing_path : str
                    Local path where the raw data is saved, by default default_rawdata_path

    Returns
    -------
        df
        Raw data
    """
    csv_path = os.path.join(housing_path, "housing.csv")
    os.makedirs(housing_path, exist_ok=True)
    return pd.read_csv(csv_path)


def data_processing_and_modelling(housing, save_path, output_path, logger):
    """Raw data is processed and cleaned

    Parameters
    ----------
            housing : df
                        Raw data set
            save_path : str
                        Path where the processed data gets stored
            output_path : str
                        Path where the model object gets stored
            logger : object
                        Logging.logger
    """

    housing["income_cat"] = pd.cut(
        housing["median_income"],
        bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
        labels=[1, 2, 3, 4, 5],
    )

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(housing, housing["income_cat"]):
        strat_train_set = housing.loc[train_index]
        strat_test_set = housing.loc[test_index]
    strat_train_set.drop("income_cat", axis=1, inplace=True)
    strat_test_set.drop("income_cat", axis=1, inplace=True)

    # housing_num = housing.drop("ocean_proximity", axis=1)

    # housing = strat_train_set.copy()

    x_train = strat_train_set.drop(
        "median_house_value", axis=1
    )  # drop labels for training set
    y_train = strat_train_set["median_house_value"].copy()

    housing_num = x_train.drop("ocean_proximity", axis=1)
    num_attribs = list(housing_num)
    cat_attribs = ["ocean_proximity"]

    num_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("attribs_adder", CombinedAttributesAdder()),
        ]
    )

    preprocessing_pipeline = ColumnTransformer(
        [
            ("num", num_pipeline, num_attribs),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_attribs),
        ]
    )

    prepare_select_and_predict_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessing_pipeline),
            ("regressor", RandomForestRegressor(random_state=42)),
        ]
    )

    param_grid = [
        # try 12 (3×4) combinations of hyperparameters
        {
            "regressor__n_estimators": [3, 10, 30],
            "regressor__max_features": [2, 4, 6, 8],
        },
        # then try 6 (2×3) combinations with bootstrap set as False
        {
            "regressor__bootstrap": [False],
            "regressor__n_estimators": [3, 10],
            "regressor__max_features": [2, 3, 4],
        },
    ]

    # train across 5 folds, that's a total of (12+6)*5=90 rounds of training
    grid_search = GridSearchCV(
        prepare_select_and_predict_pipeline,
        param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        return_train_score=True,
    )
    grid_search.fit(x_train, y_train)

    rf_fit = grid_search.fit(x_train, y_train.values.ravel())
    feature_importances = rf_fit.best_estimator_._final_estimator.feature_importances_

    sorted(zip(feature_importances, x_train.columns), reverse=True)

    final_model = grid_search.best_estimator_

    pickle.dump(final_model, open(output_path, "wb"))

    logger.info("Model Creation done")

    x_test = strat_test_set.drop(
        "median_house_value", axis=1
    )  # drop labels for training set
    y_test = strat_test_set["median_house_value"].copy()

    # preprocessing_pipeline.fit(x_train)
    # x_test_prepared = preprocessing_pipeline.transform(x_test)

    train_path_x = os.path.join(save_path, "train_housing_x.csv")
    train_path_y = os.path.join(save_path, "train_housing_y.csv")
    test_path_x = os.path.join(save_path, "test_housing_x.csv")
    test_path_y = os.path.join(save_path, "test_housing_y.csv")

    os.makedirs(save_path, exist_ok=True)

    x_train.to_csv(train_path_x)
    y_train.to_csv(train_path_y)
    x_test.to_csv(test_path_x)
    y_test.to_csv(test_path_y)

    logger.info("Input Datasets Created & Saved")


def main():
    all_paths = parser_args()
    save_path = all_paths[0]
    output_path = all_paths[3]
    logger = all_paths[8]
    mkdirs(default_rawdata_path)
    housing = load_housing_data(default_rawdata_path)
    data_processing_and_modelling(housing, save_path, output_path, logger)
    # model_train(train_path_x, train_path_y, output_path, logger)


if __name__ == "__main__":
    main()
