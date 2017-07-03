import pandas as pd
import numpy as np
from scipy import stats

from analyze_utils import preprocess
from profile_cumulative import validate_profile
import config
import data


def add_cols(layers):
    layers['log_bottom'] = np.log10(layers['bottom'])
    layers['height'] = layers['bottom'] - layers['top']
    layers['orgc_density'] = layers.apply(lambda layer: layer_density(layer), axis=1)
    layers['orgc_area_density'] = layers['height'] * layers['orgc_density']

    return layers

def layer_density(layer):
    '''
    Calculates C stocks (density) per layer in g/dm^3
    using BDFI when available, or an approximation using BDWS. 
    '''
    if not np.isnan(layer['bdfi_value_avg']):
        return layer['bdfi_value_avg'] * layer['orgc_value_avg']
    else:
    # elif not (np.isnan(layer['bdws_value_avg']) or np.isnan(layer['cfgr_value_avg']) or np.isnan(layer['cfvo_value_avg'])):
        bdfi = layer['bdws_value_avg'] * (1 - layer['cfgr_value_avg'] / 100) / (1 - layer['cfvo_value_avg'] / 100)
        return bdfi * layer['orgc_value_avg']

def fit_linregress(layers):
    # log-log
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['log_bottom'], layers['log_orgc_cumulative'])
    print(f'log Y = {slope:.3f} log d + {intercept:.3f}, R^2 = {r_value ** 2:.3f}, stderr = {std_err:.3f}')

    # log-linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['bottom'], layers['log_orgc_cumulative'])
    print(f'log Y = {slope:.3f} d + {intercept:.3f}, R^2 = {r_value ** 2:.3f}, stderr = {std_err:.3f}')

    # linear-linear
    slope, intercept, r_value, p_value, std_err = stats.linregress(layers['bottom'], layers['orgc_cumulative'])
    print(f'Y = {slope:.3f} d + {intercept:.3f}, R^2 = {r_value ** 2:.3f}, stderr = {std_err:.3f}')

def fit_linregress_per_biome(layers):
    for biome_id in range(1, 15):
        biome_name = config.biomes_dict[biome_id]
        layers_biome = layers[layers['biome'] == biome_id]
        print(f'Biome: {biome_name}. Fitting models on {len(layers_biome)} data points (cumulative).')
        if len(layers_biome) > 0:
            fit_linregress(layers_biome)
        else:
            print('No data!')

def fit_models(layers):
    peatland_mask = layers['soil_type_all'] == 'peatland'
    permafrost_mask = layers['soil_type_all'] == 'permafrost'
    other_soils_mask = ~peatland_mask & ~permafrost_mask

    for mask, soil_type in ((slice(None), 'All soils'),
                            (peatland_mask, 'Peatlands'),
                            (permafrost_mask, 'Permafrost'),
                            (other_soils_mask, 'Other soils')):
        layers_subset = layers[mask]
        print(f'\n====== SOIL TYPE: {soil_type} ======')
        print(f'Fitting models on {len(layers_subset)} data points (cumulative).')
        fit_linregress(layers_subset)
        fit_linregress_per_biome(layers_subset)

def prepare_data():
    _, profiles, layers = data.load_data()

    layers = preprocess(layers, profiles)
    layers = add_cols(layers)
    layers = layers[layers['height'] > 0]

    layers_by_profile = []
    for profile_id in profiles['profile_id']:
        profile_layers = layers[layers['profile_id'] == profile_id].sort_values('top')

        if validate_profile(profile_layers):
            profile_layers['orgc_cumulative'] = profile_layers['orgc_area_density'].cumsum()
            layers_by_profile.append(profile_layers)

    layers_cum = pd.concat(layers_by_profile)
    layers_cum['log_orgc_cumulative'] = np.log10(layers_cum['orgc_cumulative'])
    layers_cum.to_csv(config.layers_file_cumulative)
    return layers_cum


if __name__ == '__main__':
    layers_cum = prepare_data()
    # layers_cum = pd.read_csv(config.layers_file_cumulative)

    fit_models(layers_cum)
