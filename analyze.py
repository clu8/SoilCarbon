import os

import numpy as np
import pandas as pd
from scipy import stats
# import matplotlib.pyplot as plt

data_dir = os.path.join('..', 'WoSIS_2016_July')
attributes_file = os.path.join(data_dir, 'wosis_201607_attributes.txt')
layers_file = os.path.join(data_dir, 'wosis_201607_layers.txt')
profiles_file = os.path.join(data_dir, 'wosis_201607_profiles.txt')


def load_data():
    print('Reading data...')

    attributes = pd.read_table(attributes_file)
    profiles = pd.read_table(profiles_file, low_memory=False)

    layers_cols = ['profile_id', 'profile_layer_id', 'top', 'bottom', 'orgc_value_avg']
    layers = pd.read_table(layers_file, low_memory=False, usecols=layers_cols)
    
    layers.dropna(inplace=True)

    # TODO check if this is valid
    layers = layers[layers['orgc_value_avg'] != 0]
    layers = layers[layers['bottom'] != 0]

    print('Done reading data!')

    return attributes, profiles, layers

def visualize_layers():
    plt.figure()
    plt.scatter(layers.head(5000)['top'], layers.head(5000)['orgc_value_avg'])
    plt.show()

def add_preprocessed_cols():
    layers['mid'] = layers[['top', 'bottom']].mean(axis=1)
    # layers['log_mid'] = np.log10(layers['mid'])
    layers['log_bottom'] = np.log10(layers['bottom'])
    layers['log_orgc_value_avg'] = np.log10(layers['orgc_value_avg'])

def fit_linregress():
    # log-log
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['log_bottom'], layers['log_orgc_value_avg'])
    print(slope, intercept, r_value ** 2, std_err)

    # log-log
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['bottom'], layers['log_orgc_value_avg'])
    print(slope, intercept, r_value ** 2, std_err)

attributes, profiles, layers = load_data()
add_preprocessed_cols()
fit_linregress()