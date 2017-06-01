import numpy as np
import pandas as pd
from scipy import stats

import config
import data


def drop_same_profile_layers(layers, bad_layers):
    '''
    Given bad_layers, drops all layers in the same profiles from layers and returns the result. 
    '''
    bad_layers_mask = layers['profile_id'].isin(bad_layers['profile_id'])
    print(f'Dropped layers: {sum(bad_layers_mask)}')
    return layers[~bad_layers_mask]

def drop_bad_data(layers, profiles):
    bad_layer_mask = layers['top'].isnull() | layers['bottom'].isnull() | layers['orgc_value_avg'].isnull()
    print(f'Dropping {sum(bad_layer_mask)} layers with null top, bottom, or orgc_value_avg. ')
    layers = layers[~bad_layer_mask]

    print('Finding layers with bad data and dropping those layers and all other layers in the same profile. ')

    bad_layer_mask = layers['top'] < 0
    print(f'Layers with top < 0, and layers in same profiles: {sum(bad_layer_mask)}')
    layers = drop_same_profile_layers(layers, layers[bad_layer_mask])

    bad_layer_mask = layers['orgc_value_avg'] == 0
    print(f'Layers with orgc_value_avg = 0: {sum(bad_layer_mask)}')
    layers = drop_same_profile_layers(layers, layers[bad_layer_mask])

    bad_layer_mask = (layers['top'] == 0) & (layers['bottom'] == 0)
    print(f'Layers with top = 0 & bottom = 0: {sum(bad_layer_mask)}')
    layers = drop_same_profile_layers(layers, layers[bad_layer_mask])

    print('Layers in profiles <40 cm with all orgc > 17%.')
    print(f'Dropped layers: {sum(layers["peatland_manual"] == "BadData")}')
    layers = layers[layers['peatland_manual'] != 'BadData']

    return layers

def add_cols(layers, drop_zeros=True):
    layers.loc[:, 'mid'] = layers[['top', 'bottom']].mean(axis=1)

    layers.loc[:, 'log_mid'] = np.log10(layers.loc[:, 'mid'])
    # layers.loc[:, 'log_bottom'] = np.log10(layers['bottom'])
    layers.loc[:, 'log_orgc_value_avg'] = np.log10(layers.loc[:, 'orgc_value_avg'])
    return layers

def fit_linregress(layers):
    # log-log
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['log_mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.3f} log d + {intercept:.3f}, R^2 = {r_value ** 2:.3f}, stderr = {std_err:.3f}')

    # log-linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['mid'], layers['log_orgc_value_avg'])
    print(f'log C = {slope:.3f} d + {intercept:.3f}, R^2 = {r_value ** 2:.3f}, stderr = {std_err:.3f}')

def fit_linregress_per_biome(layers):
    for biome_id in range(1, 15):
        biome_name = config.biomes_dict[biome_id]
        layers_biome = layers[layers['biome'] == biome_id]
        print(f'Biome: {biome_name}. Fitting models on {len(layers_biome)} layers.')
        if len(layers_biome) > 0:
            fit_linregress(layers_biome)
        else:
            print('No data!')

def fit_models(layers, profiles):
    peatland_mask = layers['soil_type_all'] == 'peatland'
    permafrost_mask = layers['soil_type_all'] == 'permafrost'
    other_soils_mask = ~peatland_mask & ~permafrost_mask

    for mask, soil_type in ((slice(None), 'All soils'),
                            (peatland_mask, 'Peatlands'),
                            (permafrost_mask, 'Permafrost'),
                            (other_soils_mask, 'Other soils')):
        layers_subset = layers[mask]
        print(f'\n====== SOIL TYPE: {soil_type} ======')
        print(f'Fitting models on {len(layers_subset)} layers.')
        fit_linregress(layers_subset)
        fit_linregress_per_biome(layers_subset)

def preprocess(layers, profiles):
    layers = pd.merge(layers, profiles, on='profile_id')
    layers = drop_bad_data(layers, profiles)
    layers = add_cols(layers)
    return layers


attributes, profiles, layers = data.load_data()
print(f'Total layers: {len(layers)}')
print(f'Total profiles: {len(profiles)}')

if __name__ == '__main__':
    layers = preprocess(layers, profiles)
    fit_models(layers, profiles)
