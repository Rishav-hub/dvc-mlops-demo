from numpy.lib.shape_base import split
from src.utils.all_utils import read_yaml, create_directory, save_local_df
import argparse
import pandas as pd
import os
from sklearn.model_selection import train_test_split


def split_and_savedata(file_name, param_path):
    """
    Split the dataframe into train and test data and save it to the local directory
    """
    data = read_yaml(file_name)
    params = read_yaml(param_path)


    # save the dataset in the local directory
    # create path to directory: artifacts/raw_local_dir/data.csv

    artifacts_dir = data['artifacts']['artifacts_dir']
    raw_local_dir = data['artifacts']['raw_local_dir']
    raw_local_file = data['artifacts']['raw_local_file']

    raw_local_file_path = os.path.join(artifacts_dir, raw_local_dir, raw_local_file)

    df = pd.read_csv(raw_local_file_path)
    
    split_ratio = params['base']['test_size']
    random_state = params['base']['random_state']
    train, test = train_test_split(df, test_size= split_ratio, random_state= random_state)

    split_data_dir= data['artifacts']['split_data_dir']
    train_data_filename= data['artifacts']['train']
    test_data_filename= data['artifacts']['test']


    create_directory([os.path.join(artifacts_dir, split_data_dir)])

    train_data_path = os.path.join(artifacts_dir, split_data_dir, train_data_filename)
    test_data_path = os.path.join(artifacts_dir, split_data_dir, test_data_filename)

    for data, data_path in zip([train, test], [train_data_path, test_data_path]):
        save_local_df(data, data_path)





if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Load data from a yaml file')
    args.add_argument('--config','-c', default="config\config.yaml")
    args.add_argument('--params','-p', default="params.yaml")

    parsed_args = args.parse_args()

    split_and_savedata(file_name= parsed_args.config, param_path= parsed_args.params) 