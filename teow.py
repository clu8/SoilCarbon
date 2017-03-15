import shapefile

shapefile_path = '../official_teow/wwf_terr_ecos'

class Teow(object):
    def __init__(self):
        sf = shapefile.Reader(shapefile_path)
        