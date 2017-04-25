import numpy as np
import pandas as pd
from scipy import stats

import config


def load_data():
    print('Reading data...')

    attributes = pd.read_table(config.attributes_file)
    profiles = pd.read_table(config.profiles_file, low_memory=False)

    layers_cols = ['profile_id', 'profile_layer_id', 'top', 'bottom', 'orgc_value_avg']
    layers = pd.read_table(config.layers_file, low_memory=False, usecols=layers_cols)
    
    layers.dropna(inplace=True)

    print('Done reading data!')

    return attributes, profiles, layers

def visualize_layers(layers):
    plt.figure()
    plt.scatter(layers.head(5000)['top'], layers.head(5000)['orgc_value_avg'])
    plt.show()

def drop_same_profile_layers(layers, profiles, bad_layers, verbose=True):
    '''
    Given bad_layers, drops all layers in the same profiles from layers and returns the result. 
    '''
    bad_profiles = pd.merge(profiles, bad_layers, on='profile_id')
    bad_profile_layers = pd.merge(layers, bad_profiles, on='profile_id')
    if verbose:
        print(f'Dropped layers: {len(bad_profile_layers)}')
    return layers[~layers['profile_id'].isin(bad_profiles['profile_id'])]


def drop_bad_data(layers, profiles):
    print('Dropping layers with top < 0, and layers in same profiles.')
    layers = drop_same_profile_layers(layers, profiles, layers[layers['top'] < 0])

    print('Dropping layers with orgc_value_avg = 0, and layers in same profiles.')
    layers = drop_same_profile_layers(layers, profiles, layers[layers['orgc_value_avg'] == 0])

    print('Dropping layers with top = 0 & bottom = 0, and layers in same profiles.')
    layers = drop_same_profile_layers(layers, profiles, layers[(layers['top'] == 0) & (layers['bottom'] == 0)])

    return layers

def add_preprocessed_cols(layers, drop_zeros=True):
    layers.loc[:, 'mid'] = layers[['top', 'bottom']].mean(axis=1)

    layers.loc[:, 'log_mid'] = np.log10(layers.loc[:, 'mid'])
    # layers.loc[:, 'log_bottom'] = np.log10(layers['bottom'])
    layers.loc[:, 'log_orgc_value_avg'] = np.log10(layers.loc[:, 'orgc_value_avg'])
    return layers

def fit_linregress(layers):
    # log-log
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['log_mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.4f} log d + {intercept:.4f}, R^2 = {r_value ** 2:.4f}, stderr = {std_err:.4f}')

    # log-linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.4f} d + {intercept:.4f}, R^2 = {r_value ** 2:.4f}, stderr = {std_err:.4f}')

attributes, profiles, layers = load_data()
print(f'Total data points: {len(layers)}')
print(f'Total profiles: {len(profiles)}')
print(f'Data points with orgc_value_avg = 0: {sum(layers["orgc_value_avg"] == 0)}')
layers = drop_bad_data(layers, profiles)
layers = add_preprocessed_cols(layers)
print(f'Fitting models on {len(layers)} data points.')
fit_linregress(layers)