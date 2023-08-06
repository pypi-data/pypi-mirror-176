import numpy as np
import pandas as pd
import random
import string
import os
from tqdm import tqdm
tqdm.pandas()

from glam.utils import utils


def create_postcode():
    return str(int(np.random.uniform()*10000)).zfill(4)

def create_first_number_suffix():
    return random.choice(string.ascii_lowercase)

def create_second_number(first_number):
    return str(int(first_number) + max(1,int(np.random.exponential(10))))

def create_unit():
    return str(max(1,int(np.random.exponential(10))))

def balance_linz(linz_path, outpath):
    """
    upgrade the LINZ datafile for training purposes by including extra parameters/making parameters more balanced. 
    """

    linz = utils.load_linz(linz_path)
    n_records = len(linz)
    n_features = 5
    feat = iter(range(1,n_features+1))

    # make upgrades
    linz['postcode'] = [utils.choose(option1 = create_postcode) for _ in tqdm(range(n_records), 'adding feature {}/{}: postcode'.format(next(feat),n_features))] 
    linz['first_number_suffix'] = [utils.choose(option1 = create_first_number_suffix) for _ in tqdm(range(n_records), 'adding feature {}/{}: suffix'.format(next(feat),n_features))] 
    linz['unit'] = [utils.choose(option1 = create_unit) for _ in tqdm(range(n_records), 'adding feature {}/{}: unit'.format(next(feat),n_features))] 
    linz['second_number'] = [utils.choose(option1 = lambda : create_second_number(fn)) for fn in tqdm(linz['address_number'].values, 'adding feature {}/{}: second number'.format(next(feat),n_features))] 

    print('adding feature {}/{}: suburb/town/city'.format(next(feat),n_features))
    linz['suburb_town_city'] = (linz['suburb_locality_ascii'].fillna('') + ', ' + linz['town_city_ascii'].fillna(''))
    linz['suburb_town_city'] = linz['suburb_town_city'].str.replace('^, |, $', '', regex=True) # remove leading and trailing commas and spaces

    # write out 
    print('upgrade complete: saving to csv')

    linz = linz[['unit','address_number','first_number_suffix','second_number',
                'full_road_name_ascii','suburb_town_city','postcode']]
    linz.to_csv(outpath, index = False)
