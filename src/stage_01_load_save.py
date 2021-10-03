from src.utils.all_utils import read_yaml, create_directory
import argparse
import pandas as pd
import os


def get_data(file_name):
    """
    Read data from a yaml file. 
    """
    data = read_yaml(file_name)

    remote_data_path= data['data_source']
    df = pd.read_csv(remote_data_path, sep= ';')

    # save the dataset in the local directory
    # create path to directory: artifacts/raw_local_dir/data.csv

    artifacts_dir = data['artifacts']['artifacts_dir']
    raw_local_dir = data['artifacts']['raw_local_dir']
    raw_local_file = data['artifacts']['raw_local_file']

    raw_local_dir_path = os.path.join(artifacts_dir, raw_local_dir)

    create_directory(dirs= [raw_local_dir_path])
    raw_local_file_path = os.path.join(raw_local_dir_path, raw_local_file)

    df.to_csv(raw_local_file_path, sep= ',', index= False)


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Load data from a yaml file')
    args.add_argument('--config','-c', default="config\config.yaml")
    parsed_args = args.parse_args()

    get_data(file_name= parsed_args.config)