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

    print('Done reading data!')

    return attributes, profiles, layers

def visualize_layers(layers):
    plt.figure()
    plt.scatter(layers.head(5000)['top'], layers.head(5000)['orgc_value_avg'])
    plt.show()

def drop_bad_data(layers, profiles):
    bad_layers = layers[layers['top'] < 0]
    bad_profiles = pd.merge(profiles, bad_layers, on='profile_id')
    bad_profile_layers = pd.merge(layers, bad_profiles, on='profile_id')

    bad_profiles.to_csv('bad_profiles.csv')
    bad_profile_layers.to_csv('bad_layers.csv')

    return layers[~layers['profile_id'].isin(bad_profiles['profile_id'])]

def add_preprocessed_cols(layers, drop_zeros=True):
    layers.loc[:, 'mid'] = layers[['top', 'bottom']].mean(axis=1)

    print('{} layers with mid = 0'.format(len(layers[layers['mid'] == 0])))
    print('{} layers with top = 0 & bottom = 0'.format(len(layers[(layers['top'] == 0) & (layers['bottom'] == 0)])))
    print('{} layers with orgc_value_avg = 0'.format(len(layers[layers['orgc_value_avg'] == 0])))

    if drop_zeros:
        layers = layers[layers['mid'] > 0]
        layers = layers[layers['orgc_value_avg'] != 0]

    layers.loc[:, 'log_mid'] = np.log10(layers['mid'])
    layers.loc[:, 'log_bottom'] = np.log10(layers['bottom'])
    layers.loc[:, 'log_orgc_value_avg'] = np.log10(layers['orgc_value_avg'])
    return layers


def fit_linregress(layers):
    # log-log
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['log_mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.4f} log d + {intercept:.4f}, R^2 = {r_value ** 2:.4f}, stderr = {std_err:.4f}')

    # log-linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.4f} d + {intercept:.4f}, R^2 = {r_value ** 2:.4f}, stderr = {std_err:.4f}')

attributes, profiles, layers = load_data()
layers = drop_bad_data(layers, profiles)
layers = add_preprocessed_cols(layers)
fit_linregress(layers)