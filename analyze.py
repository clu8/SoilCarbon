import numpy as np
import pandas as pd
from scipy import stats

import config


def load_data(biome=True):
    print('Reading data...')

    attributes = pd.read_table(config.attributes_file)
    if biome:
        profiles = pd.read_csv(config.profiles_biomes, low_memory=False)
    else:
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

def get_profiles_per_soil_type(profiles):
    '''
    Peatland soil:
    Histosol in cfao_major_group OR Histosol in cwrb_reference_soil_group OR Histosol in cstx_order_name
    Permafrost soil:
    Gelic in cfao_soil_unit OR Cryosol in cwrb_reference_group OR Gelisol in cstx_order_name.
    '''
    peatland_mask = (profiles['cfao_major_group'] == 'Histosols') \
        | (profiles['cwrb_reference_soil_group'] == 'Histosols') \
                    | (profiles['cstx_order_name'] == 'Histosol')
    print(f'Found {sum(peatland_mask)} peatland profiles with CFAO/CWRB/CSTX labels.')

    permafrost_mask = (profiles['cfao_soil_unit'] == 'Gelic') \
        | (profiles['cwrb_reference_soil_group'] == 'Cryosols') \
        | (profiles['cstx_order_name'] == 'Gelisol')
    print(f'Found {sum(permafrost_mask)} permafrost profiles with CFAO/CWRB/CSTX labels.')

def fit_linregress(layers):
    # log-log
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['log_mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.4f} log d + {intercept:.4f}, R^2 = {r_value ** 2:.4f}, stderr = {std_err:.4f}')

    # log-linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.4f} d + {intercept:.4f}, R^2 = {r_value ** 2:.4f}, stderr = {std_err:.4f}')

def fit_linregress_per_biome(layers):
    for biome in range(1, 15):
        layers_biome = layers[layers['biome'] == biome]
        print(f'Biome: {biome}. Fitting models on {len(layers_biome)} data points.')
        if len(layers_biome) > 0:
            fit_linregress(layers_biome)
        else:
            print('No data!')

def fit_models():
    print('\n=== ALL SOILS ===')
    print(f'Fitting models on {len(layers)} data points.')
    fit_linregress(layers)
    fit_linregress_per_biome(layers)

    print('\n=== HISTOSOLS ===')
    histosols = layers[layers['cstx_order_name'] == 'Histosol']
    print(f'Fitting models on {len(histosols)} data points.')
    fit_linregress(histosols)
    fit_linregress_per_biome(histosols)

    print('\n=== GELISOLS ===')
    gelisols = layers[layers['cstx_order_name'] == 'Gelisol']
    print(f'Fitting models on {len(gelisols)} data points.')
    fit_linregress(gelisols)
    fit_linregress_per_biome(gelisols)

    print('\n=== OTHER SOILS (incl. no data) ===')
    others = layers[(layers['cstx_order_name'] != 'Histosol') & (layers['cstx_order_name'] != 'Gelisol')]
    print(f'Fitting models on {len(others)} data points.')
    fit_linregress(others)
    fit_linregress_per_biome(others)


attributes, profiles, layers = load_data()
print(f'Total data points: {len(layers)}')
print(f'Total profiles: {len(profiles)}')
print(f'Data points with orgc_value_avg = 0: {sum(layers["orgc_value_avg"] == 0)}')
layers = drop_bad_data(layers, profiles)
layers = add_preprocessed_cols(layers)
layers = pd.merge(layers, profiles, on='profile_id')

if __name__ == '__main__':
    fit_models()
