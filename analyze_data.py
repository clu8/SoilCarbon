import os

import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt

data_dir = os.path.join('..', 'WoSIS_2016_July')
attributes_file = os.path.join(data_dir, 'wosis_201607_attributes.txt')
layers_file = os.path.join(data_dir, 'wosis_201607_layers.txt')
profiles_file = os.path.join(data_dir, 'wosis_201607_profiles.txt')

attributes = pd.read_table(attributes_file)
profiles = pd.read_table(profiles_file, low_memory=False)

layers_cols = ['profile_id', 'profile_layer_id', 'top', 'bottom', 'orgc_value_avg']
layers = pd.read_table(layers_file, low_memory=False, usecols=layers_cols)

# plt.figure()
# plt.scatter(layers.head(5000)['top'], layers.head(5000)['orgc_value_avg'])
# plt.show()

layers['mid'] = layers[['top', 'bottom']].mean(axis=1)
layers['log_mid'] = np.log10(layers['mid'])
layers['log_orgc_value_avg'] = np.log10(layers['orgc_value_avg'])

