import os
import tarfile

# import numpy as np
# import pandas as pd
from six.moves import urllib

from mle_training_pack.config import *


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=default_rawdata_path):
    """The function extracts the raw data and saves it in a local path

    Parameters
    ----------
            housing_url : str
                            The URL from where the data is extracted, by default HOUSING_URL
            housing_path : str
                            Local path where the raw data needs to be saved, by default default_rawdata_path
    """
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()
    # logger.info("Raw Data extracted and stored locally")


# def load_housing_data(housing_path=default_rawdata_path):
#     """Loads raw data from local path

#     Parameters
#     ----------
#     housing_path : str
#                     Local path where the raw data is saved, by default default_rawdata_path

#     Returns
#     -------
#         df
#         Raw data
#     """
#     csv_path = os.path.join(housing_path, "housing.csv")
#     os.makedirs(housing_path, exist_ok=True)
#     return pd.read_csv(csv_path)


# def data_processing(housing, save_path, logger):
#     """Raw data is processed and cleaned

#     Parameters
#     ----------
#             housing : df
#                         Raw data set
#             save_path : str
#                         Path where the processed data gets stored
#             logger : object
#                         Logging.logger
#     """

#     train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

#     housing["income_cat"] = pd.cut(
#         housing["median_income"],
#         bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
#         labels=[1, 2, 3, 4, 5],
#     )

#     split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
#     for train_index, test_index in split.split(housing, housing["income_cat"]):
#         strat_train_set = housing.loc[train_index]
#         strat_test_set = housing.loc[test_index]

#     strat_train_set.drop("income_cat", axis=1, inplace=True)

#     housing = strat_train_set.copy()

#     housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
#     housing["bedrooms_per_room"] = housing["total_bedrooms"] / housing["total_rooms"]
#     housing["population_per_household"] = housing["population"] / housing["households"]

#     housing = strat_train_set.drop(
#         "median_house_value", axis=1
#     )  # drop labels for training set
#     housing_labels = strat_train_set["median_house_value"].copy()

#     imputer = SimpleImputer(strategy="median")

#     housing_num = housing.drop("ocean_proximity", axis=1)

#     imputer.fit(housing_num)
#     X = imputer.transform(housing_num)

#     housing_tr = pd.DataFrame(X, columns=housing_num.columns, index=housing.index)
#     housing_tr["rooms_per_household"] = (
#         housing_tr["total_rooms"] / housing_tr["households"]
#     )
#     housing_tr["bedrooms_per_room"] = (
#         housing_tr["total_bedrooms"] / housing_tr["total_rooms"]
#     )
#     housing_tr["population_per_household"] = (
#         housing_tr["population"] / housing_tr["households"]
#     )

#     housing_cat = housing[["ocean_proximity"]]
#     housing_prepared = housing_tr.join(pd.get_dummies(housing_cat, drop_first=True))

#     strat_test_set.drop("income_cat", axis=1, inplace=True)

#     X_test = strat_test_set.drop("median_house_value", axis=1)
#     y_test = strat_test_set["median_house_value"].copy()

#     X_test_num = X_test.drop("ocean_proximity", axis=1)
#     X_test_prepared = imputer.transform(X_test_num)
#     X_test_prepared = pd.DataFrame(
#         X_test_prepared, columns=X_test_num.columns, index=X_test.index
#     )
#     X_test_prepared["rooms_per_household"] = (
#         X_test_prepared["total_rooms"] / X_test_prepared["households"]
#     )
#     X_test_prepared["bedrooms_per_room"] = (
#         X_test_prepared["total_bedrooms"] / X_test_prepared["total_rooms"]
#     )
#     X_test_prepared["population_per_household"] = (
#         X_test_prepared["population"] / X_test_prepared["households"]
#     )

#     X_test_cat = X_test[["ocean_proximity"]]
#     X_test_prepared = X_test_prepared.join(pd.get_dummies(X_test_cat, drop_first=True))

#     train_path_x = os.path.join(save_path, "train_housing_x.csv")
#     train_path_y = os.path.join(save_path, "train_housing_y.csv")
#     test_path_x = os.path.join(save_path, "test_housing_x.csv")
#     test_path_y = os.path.join(save_path, "test_housing_y.csv")

#     os.makedirs(save_path, exist_ok=True)

#     housing_prepared.to_csv(train_path_x)
#     housing_labels.to_csv(train_path_y)
#     X_test_prepared.to_csv(test_path_x)
#     y_test.to_csv(test_path_y)

#     logger.info("Input Datasets Created & Saved")


def main():
    all_paths = parser_args()
    save_path = all_paths[0]
    # logger = all_paths[8]
    mkdirs(save_path)
    mkdirs(default_rawdata_path)
    fetch_housing_data(HOUSING_URL, default_rawdata_path)
    # housing = load_housing_data(default_rawdata_path)
    # data_processing(housing, save_path, logger)


if __name__ == "__main__":
    main()
