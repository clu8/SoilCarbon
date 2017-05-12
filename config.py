import os

data_dir = os.path.join('..', 'WoSIS_2016_July')
attributes_file = os.path.join(data_dir, 'wosis_201607_attributes.txt')
layers_file = os.path.join(data_dir, 'wosis_201607_layers.txt')
profiles_file = os.path.join(data_dir, 'wosis_201607_profiles.txt')
profiles_biomes = os.path.join(data_dir, 'wosis_201607_profiles_biomes.csv')

layers_cols = ['profile_id', 'profile_layer_id', 'top', 'bottom', 'orgc_value_avg']

shapefile_path = '../official_teow/wwf_terr_ecos'


biomes_dict = {
    1: 'Tropical and Subtropical Moist Broadleaf Forests',
    2: 'Tropical and Subtropical Dry Broadleaf Forests',
    3: 'Tropical and Subtropical Coniferous Forests',
    4: 'Temperate Broadleaf and Mixed Forests',
    5: 'Temperate Coniferous Forests',
    6: 'Boreal Forests/Taiga',
    7: 'Tropical and subtropical grasslands, savannas, and shrublands',
    8: 'Temperate Grasslands, Savannas, Shrublands',
    9: 'Flooded Grasslands and Savannas',
    10: 'Montane Grasslands and Shrublands',
    11: 'Tundra',
    12: 'Mediterranean Forests, Woodlands, and Scrub',
    13: 'Deserts and Xeric Shrublands',
    14: 'Mangroves',
    98: 'Lakes',
    99: 'Rock and Ice'
}