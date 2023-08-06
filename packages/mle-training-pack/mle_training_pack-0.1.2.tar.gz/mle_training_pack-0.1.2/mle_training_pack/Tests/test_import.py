from mle_training_pack.config import *
from mle_training_pack.ingest_data import fetch_housing_data
from mle_training_pack.train import load_housing_data

default_rawdata_path_test = "test_data/"
os.makedirs(default_rawdata_path_test, exist_ok=True)


def test_housing_data():
    """
    Test to check the number of columns in the input
    """
    fetch_housing_data(HOUSING_URL, default_rawdata_path_test)
    p = load_housing_data(default_rawdata_path_test)
    assert len(p.columns) == 10


def test_col_names():
    """
    Test to check the presence of all required column names in the input
    """
    fetch_housing_data(HOUSING_URL, default_rawdata_path_test)
    p = load_housing_data(default_rawdata_path_test)

    base_cols = [
        "longitude",
        "latitude",
        "housing_median_age",
        "total_rooms",
        "total_bedrooms",
        "population",
        "households",
        "median_income",
        "median_house_value",
        "ocean_proximity",
    ]

    a = set(base_cols)
    b = set(p.columns.values)

    assert a == b


def test_col_type_check():
    """
    Test to check the data types of all columns in the input
    """
    fetch_housing_data(HOUSING_URL, default_rawdata_path_test)
    p = load_housing_data(default_rawdata_path_test)

    col_types = [
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "float64",
        "O",
    ]
    assert p.dtypes.values.tolist() == col_types
