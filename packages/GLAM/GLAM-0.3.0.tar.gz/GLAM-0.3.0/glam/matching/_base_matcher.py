import os

from glam.matching import _siamese

class BaseMatcher():
    
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self._requires_parser = True

    def __repr__(self):
        return self.type

    def build_dependencies(self):
        pass

