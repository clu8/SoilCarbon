import pandas as pd

import config


ORGC_THRESHOLD = 170

def label_soil_type(profile, layers):
    '''
    -Option 1:
    If depth >80 cm
    Calculate cumulative sum of centimeters where org C percent is > (or equal) 17%
    If this cumulative sum is > (or equal) 40 cm the soil is a Peatland/Histosol.

    -Option 2:
    If depth is between 40 and 80 cm.
    If all individual layers between 0 and 40 cm depth have org C percent > (or equal) 17% the soil is a Peatland/Histosol.

    -If there is less than 40 cm of data, but all layers have org C percent > (or equal) 17% the profile should be thrown out of the dataset.
    '''
    profile_id = profile['profile_id']
    profile_layers = layers[layers['profile_id'] == profile_id]

    if len(profile_layers) == 0:
        return None

    depth = max(profile_layers['bottom'])

    if depth > 80:
        high_orgc_layers = profile_layers[profile_layers['orgc_value_avg'] >= ORGC_THRESHOLD]
        cumulative_high_orgc_cm = sum(high_orgc_layers['bottom'] - high_orgc_layers['top'])
        return 'PeatlandOption1' if cumulative_high_orgc_cm >= 40 else None
    else:
        shallow_layers = profile_layers[profile_layers['top'] < 40].dropna()
        if len(shallow_layers) > 0 and (shallow_layers['orgc_value_avg'] >= ORGC_THRESHOLD).all():
            return 'PeatlandOption2' if depth >= 40 else 'BadData'
        else:
            return None


def main():
    profiles = pd.read_csv(config.profiles_biomes, low_memory=False)
    layers = pd.read_table(config.layers_file, low_memory=False, usecols=config.layers_cols)

    profiles['my_soil_type'] = profiles.apply(lambda profile: label_soil_type(profile, layers), axis=1)

    profiles.to_csv(config.profiles_biomes)

if __name__ == '__main__':
    main()
