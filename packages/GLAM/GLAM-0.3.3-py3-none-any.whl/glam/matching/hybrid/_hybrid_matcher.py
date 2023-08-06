import os

from glam.matching._base_matcher import BaseMatcher

class HybridMatcher(BaseMatcher):

    def __init__(self, data_dir):
        self.type = 'HybridMatcher'
        self.data_dir = data_dir

    def build_dependencies(self, overwrite = False):
        pass

    def load_dependencies(self, build):
        pass

    def match_addresses(self, addresses, build_dependencies = False):
        raise ValueError('Not implemented')