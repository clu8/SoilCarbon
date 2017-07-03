import pandas as pd

import config


def load_data(exclude_profiles_cols=True, exclude_layers_cols=True):
    attributes = pd.read_table(config.attributes_file)
    profiles = pd.read_csv(config.profiles_file_labeled, low_memory=False, usecols=config.profiles_cols if exclude_profiles_cols else None)
    layers = pd.read_table(config.layers_file, low_memory=False, usecols=config.layers_cols if exclude_layers_cols else None)

    return attributes, profiles, layers
