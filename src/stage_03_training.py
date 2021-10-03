from numpy.lib.shape_base import split
from src.utils.all_utils import read_yaml, create_directory, save_local_df
import argparse
import pandas as pd
import os
from sklearn.linear_model import ElasticNet
import joblib


def training_data(file_name, param_path):
    """
    Split the dataframe into train and test data and save it to the local directory
    """
    data = read_yaml(file_name)
    params = read_yaml(param_path)


    # save the dataset in the local directory
    # create path to directory: artifacts/raw_local_dir/data.csv

    artifacts_dir = data['artifacts']['artifacts_dir']

    split_data_dir= data['artifacts']['split_data_dir']
    train_data_filename= data['artifacts']['train']

    train_data_path = os.path.join(artifacts_dir, split_data_dir, train_data_filename)

    train_data = pd.read_csv(train_data_path)
    # Train data

    train_y = train_data['quality']
    train_x = train_data.drop(['quality'], axis=1)

    alpha= params['model_params']['ElasticNet']['alpha']
    l1_ratio= params['model_params']['ElasticNet']['l1_ratio']

    random_state= params['base']['random_state']

    lr = ElasticNet(alpha= alpha, l1_ratio= l1_ratio, random_state= random_state)
    lr.fit(train_x, train_y)
    

    # save the model in the local directory
    model_dir = data["artifacts"]["model_dir"]
    model_filename = data["artifacts"]["model_filename"]

    model_dir = os.path.join(artifacts_dir, model_dir)

    create_directory([model_dir])

    model_path = os.path.join(model_dir, model_filename)

    joblib.dump(lr, model_path)





    print('Training Completed!!!!')








if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Load data from a yaml file')
    args.add_argument('--config','-c', default="config\config.yaml")
    args.add_argument('--params','-p', default="params.yaml")

    parsed_args = args.parse_args()

    training_data(file_name= parsed_args.config, param_path= parsed_args.params) 