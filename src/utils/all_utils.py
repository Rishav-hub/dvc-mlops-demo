import yaml
import os

def read_yaml(path_to_yaml: str) -> dict:
    """
    Reads a yaml file and returns a dictionary
    """
    with open(path_to_yaml, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)

def create_directory(dirs: list):
    """
    Creates a directory if it does not exist
    """
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Directory is created at {dir_path}")

def save_local_df(data, data_path, index= False):
    """
    Saves a dataframe to a local file
    """
    data.to_csv(data_path, index=index)
    print(f"Dataframe is saved to {data_path}")
