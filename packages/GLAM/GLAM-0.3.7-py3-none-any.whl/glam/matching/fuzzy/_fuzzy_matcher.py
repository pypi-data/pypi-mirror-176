import os

from glam.matching._base_matcher import BaseMatcher
from glam.matching.fuzzy import _predict, _linz
from glam.utils import utils

class FuzzyMatcher(BaseMatcher):

    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.type = 'FuzzyMatcher'
        self.lookup_linz = None
        self._requires_parser = True

        utils.check_package_dependency('rapidfuzz','1.7.1')

    def build_dependencies(self, overwrite = False):
        raw_linz_path = os.path.join(self.data_dir,'nz-street-address.csv')
        data_path = os.path.join(self.data_dir,'matching',self.type)
        upgraded_linz_path = os.path.join(data_path,'linz_upgraded.csv')

        if os.path.isfile(upgraded_linz_path) and not overwrite:
            print('Dependency already exists. Pass overwrite = True to rebuild')
            
        else:
            print('Building dependencies...')
            _linz.upgrade_linz(
                raw_linz_path,
                os.path.join(self.data_dir,'PNF'),
                upgraded_linz_path
            )

    def load_dependencies(self, build):
        
        data_path = os.path.join(self.data_dir,'matching',self.type)
        upgraded_linz_path = os.path.join(data_path,'linz_upgraded.csv')

        if not os.path.isfile(upgraded_linz_path) and build:
            self.build_dependencies()
            
        if self.lookup_linz is None:
            print('Loading matcher dependencies...')
            self.lookup_linz = _linz.load_linz(upgraded_linz_path)

    def match_addresses(self, addresses, build_dependencies = False):
        
        if self.lookup_linz is None:
            self.load_dependencies(build_dependencies)

        addresses = _predict.lookup_addresses(addresses, self.lookup_linz)
        return addresses
