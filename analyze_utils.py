import pandas as pd


def convert_units(layers):
    layers['bottom'] /= 100 # cm to m TODO check if it's cm
    layers['top'] /= 100 # cm to m TODO check if it's cm
    layers['orgc_value_avg'] /= 1000 # g/kg to percent
    layers['bdfi_value_avg'] *= 1000 # kg/dm^3 to kg/m^3
    layers['bdws_value_avg'] *= 1000 # kg/dm^3 to kg/m^3
    return layers

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

    bad_layer_mask = (layers['top'] < 0) | (layers['bottom'] <= 0)
    print(f'Layers with top < 0 or bottom <= 0, and layers in same profiles: {sum(bad_layer_mask)}')
    layers = drop_same_profile_layers(layers, layers[bad_layer_mask])

    bad_layer_mask = layers['orgc_value_avg'] == 0
    print(f'Layers with orgc_value_avg = 0: {sum(bad_layer_mask)}')
    layers = drop_same_profile_layers(layers, layers[bad_layer_mask])

    print('Layers in profiles <40 cm with all orgc > 17%.')
    print(f'Dropped layers: {sum(layers["peatland_manual"] == "BadData")}')
    layers = layers[layers['peatland_manual'] != 'BadData']

    return layers

def preprocess(layers, profiles):
    layers = convert_units(layers)
    layers = pd.merge(layers, profiles, on='profile_id')
    layers = drop_bad_data(layers, profiles)
    return layers
