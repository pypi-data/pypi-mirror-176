import os
from glob import glob
import pickle
import warnings

from glam.matching._base_matcher import BaseMatcher
from glam.matching.embedded import _predict, _linz
from glam.utils import utils

class EmbeddedMatcher(BaseMatcher):

    def __init__(self, data_dir):
        super().__init__(data_dir)

        self.data_path = os.path.join(self.data_dir,'matching','EmbeddedMatcher')
        self.type = 'Embedded'
        self.trees = []
        self.linz = None

        utils.check_package_dependency('scipy')

    def build_dependencies(self, overwrite = False):
        raw_linz_path = os.path.join(self.data_dir,'nz-street-address.csv')
        tree_check = os.path.join(self.data_path, 'tree0.pkl')

        if os.path.isfile(tree_check) and not overwrite:
            print('Dependency already exists. Pass overwrite = True to rebuild')
            
        else:
            pc_path = os.path.join(self.data_dir,'PNF')
            if not os.path.exists(pc_path): 
                warnings.warn(f'PNF file not found at {pc_path}')
                pc_path = None

            os.makedirs(self.data_path, exist_ok=True)
            print('Building dependencies...')
            _linz.upgrade_linz(
                raw_linz_path,
                self.data_path,
                pc_path
            )

    def load_dependencies(self, build):

        linz_path = os.path.join(self.data_dir,'nz-street-address.csv')
        tree_check = os.path.join(self.data_path, 'tree0.pkl')

        if not os.path.isfile(tree_check) and build:
            self.build_dependencies()

        print('Loading matcher dependencies...')
        if self.linz is None:
            print('  Loading LINZ file')
            self.linz = utils.load_linz(linz_path)
            
        if len(self.trees) == 0:
            print('  Loading search trees')
            files = glob(
                os.path.join(self.data_path,'tree*.pkl')
            )
            self.trees = {0:None}
            for tree_path in files:
                with open(tree_path, 'rb') as f:
                    tree = pickle.load(f)
                
                self.trees[tree.m] = tree

    def match_addresses(self, addresses, build_dependencies = False):
        
        if len(self.trees) == 0 or self.linz is None:
            self.load_dependencies(build_dependencies)

        addresses = _predict.lookup_addresses(addresses, self.linz, self.trees)
        return addresses
