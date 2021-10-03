from numpy.lib.shape_base import split
from src.utils.all_utils import read_yaml, create_directory, save_reports
import argparse
import pandas as pd
import os
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import numpy as np

def evaluate_metrices(actual_values, predicted_values):
    """
    Evaluate the model using the metrics
    """
    rmse = np.sqrt(mean_squared_error(actual_values, predicted_values))
    mae = mean_absolute_error(actual_values, predicted_values)
    r2 = r2_score(actual_values, predicted_values)
    return rmse, mae, r2

def evaluate(file_name, param_path):
    """
    Split the dataframe into train and test data and save it to the local directory
    """
    data = read_yaml(file_name)
    params = read_yaml(param_path)


    # save the dataset in the local directory
    # create path to directory: artifacts/raw_local_dir/data.csv

    artifacts_dir = data['artifacts']['artifacts_dir']

    split_data_dir= data['artifacts']['split_data_dir']
    test_data_filename= data['artifacts']['test']

    test_data_path = os.path.join(artifacts_dir, split_data_dir, test_data_filename)

    # read the test data
    test_data = pd.read_csv(test_data_path)
    test_y = test_data["quality"]
    test_x = test_data.drop("quality", axis=1)
    

    # Model Directory
    model_dir = data["artifacts"]["model_dir"]
    model_filename = data["artifacts"]["model_filename"]
    model_path = os.path.join(artifacts_dir, model_dir, model_filename)

    lr = joblib.load(model_path)
    print('Model Loaded!!!!')

    # Predict the test data
    predicted_values = lr.predict(test_x)
    rmse, mae, r2 = evaluate_metrices(test_y, predicted_values)

    scores_dir = data["artifacts"]["report_dir"]
    scores_filename = data["artifacts"]["scores"]

    scores_dir_path = os.path.join(artifacts_dir, scores_dir)
    create_directory([scores_dir_path])

    scores_filepath = os.path.join(scores_dir_path, scores_filename)

    scores = {
        "rmse": rmse,
        "mae": mae,
        "r2": r2
        }
    
    save_reports(scores, scores_filepath)

    print("Evaluation Completed !!!!")


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Load data from a yaml file')
    args.add_argument('--config','-c', default="config\config.yaml")
    args.add_argument('--params','-p', default="params.yaml")

    parsed_args = args.parse_args()

    evaluate(file_name= parsed_args.config, param_path= parsed_args.params) 