import pickle

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

from mle_training_pack.config import *


def test_model(test_path_x, test_path_y, model_path, predictions_file_path, logger):
    """Test Data is loaded and scored using a predefined model

    Parameters
    ----------
            test_path_x : str
                            Input path of IDV's of data to be scored
            test_path_y : str
                            Input path of DV of data to be scored for comparison
            model_path : str
                            Input path for model
            predictions_file_path : str
                            Output path for predictions to be saved
            logger : object
                            Logger.logging
    """

    X_test_prepared = pd.read_csv(test_path_x, index_col=0)
    y_test = pd.read_csv(test_path_y, index_col=0)

    final_model = pickle.load(open(model_path, "rb"))
    print(list(X_test_prepared))
    print(list(y_test))
    final_predictions = final_model.predict(X_test_prepared)
    final_mse = mean_squared_error(y_test, final_predictions)
    final_rmse = np.sqrt(final_mse)

    logger.info("Model Predictions Done")
    logger.info("RMSE of the Test Data - " + str(np.round(final_rmse, 2)))

    pd.DataFrame(final_predictions).to_csv(predictions_file_path)

    logger.info("File Saved")


def main():
    all_paths = parser_args()
    test_path_x = all_paths[4]
    test_path_y = all_paths[5]
    model_path = all_paths[6]
    predictions_file_path = all_paths[7]
    mkdirs(default_output_data_path)
    logger = all_paths[8]
    test_model(test_path_x, test_path_y, model_path, predictions_file_path, logger)


if __name__ == "__main__":
    main()
