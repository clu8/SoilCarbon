import shapefile
import shapely.geometry as geometry

import config


class Region(object):
    def __init__(self, shape, record):
        self.shape = shape
        self.polygon = geometry.shape(shape)
        self.record = record

    def contains(self, point):
        return self.polygon.contains(point)

class Teow(object):
    def __init__(self):
        self.sf = shapefile.Reader(config.shapefile_path)
        self.regions = [Region(shape, record) for shape, record in zip(self.sf.shapes(), self.sf.records())]
        self.record_field_to_idx = {field[0]: i for i, field in enumerate(self.sf.fields[1:])}