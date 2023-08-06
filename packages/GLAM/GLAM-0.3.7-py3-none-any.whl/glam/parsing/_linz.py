import numpy as np
import pandas as pd
import random
import string
from tqdm import tqdm
tqdm.pandas()

from glam.utils import utils

def create_building_name(max_words = 4, min_word_length = 2, max_word_length = 10):

    building_name = ''
    # generate up to max words for building name (with decreasing probability)
    for i in range(1,max_words):
        if np.random.uniform() <= 1/i**2:
            building_name +=  ''.join([random.choice(string.ascii_lowercase) for x in range(np.random.randint(min_word_length,max_word_length))]) + ' '

    return building_name

def create_level_number(weights = [0.7,0.3], levels = [10,100]):

    r = np.random.uniform()

    for i in range(len(weights)):
        w = sum(weights[:i])
        if r >= w:
            return str(int(np.random.randint(levels[i])))

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

    print(f"  Loading raw LINZ file from: {linz_path}")
    linz = utils.load_linz(linz_path)
    n_records = len(linz)
    n_features = 7
    feat = iter(range(1,n_features+1))

    # make upgrades
    linz['building_name'] = [utils.choose(option1 = create_building_name) for _ in tqdm(range(n_records), '  adding feature {}/{}: building name'.format(next(feat),n_features))]
    linz['level_number'] = [utils.choose(option1 = create_level_number) for _ in tqdm(range(n_records), '  adding feature {}/{}: level number'.format(next(feat),n_features))]
    linz['postcode'] = [utils.choose(option1 = create_postcode) for _ in tqdm(range(n_records), '  adding feature {}/{}: postcode'.format(next(feat),n_features))] 
    linz['first_number_suffix'] = [utils.choose(option1 = create_first_number_suffix) for _ in tqdm(range(n_records), '  adding feature {}/{}: suffix'.format(next(feat),n_features))] 
    linz['unit'] = [utils.choose(option1 = create_unit) for _ in tqdm(range(n_records), '  adding feature {}/{}: unit'.format(next(feat),n_features))] 
    linz['second_number'] = [utils.choose(option1 = lambda : create_second_number(fn)) for fn in tqdm(linz['address_number'].values, '  adding feature {}/{}: second number'.format(next(feat),n_features))] 

    print('  adding feature {}/{}: suburb/town/city'.format(next(feat),n_features))
    linz['suburb_town_city'] = (linz['suburb_locality_ascii'].fillna('') + ', ' + linz['town_city_ascii'].fillna(''))
    linz['suburb_town_city'] = linz['suburb_town_city'].str.replace('^, |, $', '', regex=True) # remove leading and trailing commas and spaces

    # write out 
    print('  LINZ balancing complete. Saving...')

    linz = linz[['building_name','level_number','unit','address_number','first_number_suffix','second_number',
                'full_road_name_ascii','suburb_town_city','full_address_ascii','shape_X','shape_Y','postcode']]

    linz.to_csv(outpath, index = False)


