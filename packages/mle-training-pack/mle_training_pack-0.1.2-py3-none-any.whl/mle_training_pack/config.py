import argparse
import logging
import logging.config
import os

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

default_input_path = "mle_training/data/input"
default_rawdata_path = "mle_training/data/raw"
default_input_data_path = "mle_training/data/input"
default_output_data_path = "mle_training/data/output"

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
# HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

LOGGING_DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(message)s"},
    },
    "root": {"level": "DEBUG"},
}


def configure_logger(
    logger=None, cfg=None, log_file=None, console=True, log_level="DEBUG"
):
    """Function to setup configurations of logger through function.

    The individual arguments of `log_file`, `console`, `log_level` will overwrite the ones in cfg.

    Parameters
    ----------
            logger:
                    Predefined logger object if present. If None a ew logger object will be created from root.
            cfg: dict()
                    Configuration of the logging to be implemented by default
            log_file: str
                    Path to the log file for logs to be stored
            console: bool
                    To include a console handler(logs printing in console)
            log_level: str
                    One of `["INFO","DEBUG","WARNING","ERROR","CRITICAL"]`
                    default - `"DEBUG"`

    Returns
    -------
    logging.Logger
    """
    if not cfg:
        logging.config.dictConfig(LOGGING_DEFAULT_CONFIG)
    else:
        logging.config.dictConfig(cfg)

    logger = logger or logging.getLogger()

    if log_file or console:
        for hdlr in logger.handlers:
            logger.removeHandler(hdlr)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(getattr(logging, log_level))
            logger.addHandler(fh)

        if console:
            sh = logging.StreamHandler()
            sh.setLevel(getattr(logging, log_level))
            logger.addHandler(sh)

    return logger


def parser_args():
    """Parses user arguments

    Returns
    -------
    tuple
        List of user defined arguments parsed and assigned to individual variables
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--log_level", help="Mention log level")
    parser.add_argument("--log_path", help="paste path to log file")
    parser.add_argument(
        "--no_console_log", action="store_true", help="Not to print log to console"
    )
    parser.add_argument("--raw_data_op", help="paste path to raw data output files")
    parser.add_argument(
        "--processed_data_ip", help="paste path to processed data input files"
    )
    parser.add_argument("--model_op", help="paste path to model output")
    parser.add_argument("--model_ip", help="paste path to model input")
    parser.add_argument("--test_data_ip", help="paste path to Test data input")
    parser.add_argument("--test_data_op", help="paste path to Test data output files")

    args = parser.parse_args()

    if args.log_level:
        log_level = args.log_level
    else:
        log_level = "DEBUG"

    console_print = True
    if args.no_console_log is True:
        console_print = False

    if args.log_path is not None:
        log_path = os.path.join(args.log_path, "logfile.log")
        logger = configure_logger(
            log_file=log_path, console=console_print, log_level=log_level
        )
    else:
        logger = configure_logger(console=console_print, log_level=log_level)

    if args.raw_data_op:
        save_path = args.raw_data_op
    else:
        save_path = default_input_path

    if args.processed_data_ip:
        train_path_x = os.path.join(args.processed_data_ip, "train_housing_x.csv")
        train_path_y = os.path.join(args.processed_data_ip, "train_housing_y.csv")
    else:
        train_path_x = os.path.join(default_input_data_path, "train_housing_x.csv")
        train_path_y = os.path.join(default_input_data_path, "train_housing_y.csv")

    if args.model_op:
        output_path = os.path.join(args.model_op, "rf_model.pkl")
    else:
        output_path = os.path.join(default_input_data_path, "rf_model.pkl")

    if args.test_data_ip:
        test_path_x = os.path.join(args.test_data_ip, "test_housing_x.csv")
        test_path_y = os.path.join(args.test_data_ip, "test_housing_y.csv")
    else:
        test_path_x = os.path.join(default_input_data_path, "test_housing_x.csv")
        test_path_y = os.path.join(default_input_data_path, "test_housing_y.csv")

    if args.model_ip:
        model_path = os.path.join(args.model_ip, "rf_model.pkl")
    else:
        model_path = os.path.join(default_input_data_path, "rf_model.pkl")

    if args.test_data_op:
        predictions_file_path = os.path.join(args.test_data_op, "predictions.csv")
    else:
        predictions_file_path = os.path.join(
            default_output_data_path, "predictions.csv"
        )

    return (
        save_path,
        train_path_x,
        train_path_y,
        output_path,
        test_path_x,
        test_path_y,
        model_path,
        predictions_file_path,
        logger,
    )


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
        os.chmod(path, 0o0770)
    return


rooms_ix, bedrooms_ix, population_ix, households_ix = 3, 4, 5, 6


class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    def __init__(self, add_bedrooms_per_room=True):  # no *args or **kargs
        self.add_bedrooms_per_room = add_bedrooms_per_room

    def fit(self, X, y=None):
        return self  # nothing else to do

    def transform(self, X):
        rooms_per_household = X[:, rooms_ix] / X[:, households_ix]
        population_per_household = X[:, population_ix] / X[:, households_ix]
        if self.add_bedrooms_per_room:
            bedrooms_per_room = X[:, bedrooms_ix] / X[:, rooms_ix]
            return np.c_[
                X, rooms_per_household, population_per_household, bedrooms_per_room
            ]

        else:
            return np.c_[X, rooms_per_household, population_per_household]
