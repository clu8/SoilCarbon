'''
SCript for labeling raw profiles data with flags for our peatlands/permafrost labels and outputting as CSV. 

Run after running label_biomes.py and label_peatlands.py. 
'''

import config
import data


def get_soil_type_masks(profiles):
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

    peatland_option_1_mask = profiles['peatland_manual'] == 'PeatlandOption1'
    print(f'Found {sum(peatland_option_1_mask)} peatland profiles with option 1.')
    print(f'{sum(peatland_option_1_mask & peatland_mask)} overlap with CFAO/CWRB/CSTX labels.')

    peatland_option_2_mask = profiles['peatland_manual'] == 'PeatlandOption2'
    print(f'Found {sum(peatland_option_2_mask)} peatland profiles with option 2.')
    print(f'{sum(peatland_option_2_mask & peatland_mask)} overlap with CFAO/CWRB/CSTX labels.')

    peatland_mask |= peatland_option_1_mask
    peatland_mask |= peatland_option_2_mask
    peatland_mask &= ~(profiles['peatland_manual'] == 'BadData')
    print(f'Total peatland profiles: {sum(peatland_mask)}')

    permafrost_mask = (profiles['cfao_soil_unit'] == 'Gelic') \
        | (profiles['cwrb_reference_soil_group'] == 'Cryosols') \
        | (profiles['cstx_order_name'] == 'Gelisol')
    print(f'Found {sum(permafrost_mask)} permafrost profiles with CFAO/CWRB/CSTX labels.')

    permafrost_mask &= ~(profiles['peatland_manual'] == 'BadData')
    print(f'Total permafrost profiles: {sum(permafrost_mask)}')

    return peatland_mask, permafrost_mask

_, profiles, _ = data.load_data(exclude_profiles_cols=False)
peatland_mask, permafrost_mask = get_soil_type_masks(profiles)

profiles.loc[peatland_mask, 'soil_type_all'] = 'peatland'
profiles.loc[permafrost_mask, 'soil_type_all'] = 'permafrost'

profiles.to_csv(config.profiles_file_labeled, encoding='utf-8')
