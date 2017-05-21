'''
Script for tagging each profile with biomes using TEOW shapefile data. 

Run this first. 
'''

import pandas as pd
import shapely.geometry as geometry

import config
from teow import Teow


def get_biome(t, profile):
    lat, lon = profile['latitude'], profile['longitude']

    for region in t.regions:
        point = geometry.Point(lon, lat)
        if region.contains(point):
            return int(float(region.record[t.record_field_to_idx['BIOME']]))

def main():
    t = Teow()
    profiles = pd.read_table(config.profiles_file, low_memory=False)
    profiles['biome'] = profiles.apply(lambda profile: get_biome(t, profile), axis=1)
    profiles.to_csv(config.profiles_file_labeled)

if __name__ == '__main__':
    main()