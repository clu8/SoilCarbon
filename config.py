import os

data_dir = os.path.join('..', 'WoSIS_2016_July')
attributes_file = os.path.join(data_dir, 'wosis_201607_attributes.txt')
layers_file = os.path.join(data_dir, 'wosis_201607_layers.txt')
profiles_file = os.path.join(data_dir, 'wosis_201607_profiles.txt')

shapefile_path = '../official_teow/wwf_terr_ecos'

profiles_biomes = os.path.join(data_dir, 'wosis_201607_profiles_biomes.csv')