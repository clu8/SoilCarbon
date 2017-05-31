'''
Script for adding columns to layers for cumulative fits.
'''

import pandas as pd
import numpy as np

import config
import data


def layer_density(layer):
    if not np.isnan(layer['bdfi_value_avg']):
        return layer['bdfi_value_avg'] * layer['orgc_value_avg']
    else:
        pass

def main():
    _, profiles, layers = data.load_data(exclude_profiles_cols=False, exclude_layers_cols=False)
    
    layers['orgc_density'] = layers.apply(lambda layer: layer_density(layer))

    layers.to_csv(config.layers_file_cumulative)

if __name__ == '__main__':
    main()
