import os

import numpy as np
import pandas as pd

data_dir = os.path.join('..', 'WoSIS_2016_July')
attributes_file = os.path.join(data_dir, 'wosis_201607_attributes.txt')
layers_file = os.path.join(data_dir, 'wosis_201607_layers.txt')
profiles_file = os.path.join(data_dir, 'wosis_201607_profiles.txt')

attributes = pd.read_table(attributes_file)
profiles = pd.read_table(profiles_file, low_memory=False)

layers_cols = ['profile_id', 'profile_layer_id', 'top', 'bottom', 'orgc_value_avg']
layers = pd.read_table(layers_file, low_memory=False, usecols=layers_cols)
