from rapidfuzz import fuzz, process
import numpy as np
import pandas as pd
from tqdm import tqdm

import gc


def lookup_addresses(addresses,linz,speed_performance_balance = 0):

    weights = {
    'unit_value_score' : 1,
    'address_number_score' : 80,
    'address_number_suffix_score' : 1,
    'address_number_high_score' : 1,
    'full_road_name_ascii_score' : 100,
    'suburb_town_city_score': 50,
    'postcode_score' : 80,
    }
    
    return_cols = ['unit_value','address_number','address_number_suffix','address_number_high','full_road_name_ascii','suburb_locality_ascii','town_city_ascii','postcode','shape_X','shape_Y','match_score']
    matched_addresses = []

    # matched_addresses = Parallel(n_jobs=4,backend = 'multiprocessing')(delayed(matching.lookup_address_rapidfuzz)(x,linz,weights,return_cols,speed_performance_balance) for x in tqdm(addresses))
    for i,x in enumerate(tqdm(addresses, smoothing = 0.05, mininterval=1, colour = 'green')):
        matched_addresses.append(lookup_address_rapidfuzz(x,linz,weights,return_cols,confidence=speed_performance_balance))
        if i % 1000 == 0:
            gc.collect()

    gc.collect()
    return matched_addresses


def lookup_address_rapidfuzz(addy,linz,weights,return_cols,confidence):
    """
    Takes a parsed address and finds the best match in the linz dataset

    Inputs:
        addy: search address in parsed dictionary format 
        linz: pandas df of linz addresses
    Outputs:
        dictionary of address components with latitute and longitude
    """

    if addy is None:
        return None

    search_area = []
    score_cols = []

    if 'postcode' in addy:
        search_area = reduce_search_space(linz, 'postcode_int', int(addy['postcode']), search_area = search_area, matcher = None)

    if 'first_number' in addy:
        search_area = reduce_search_space(linz, 'address_number_int', int(addy['first_number']), search_area=search_area, matcher = None)

    # if exact matching failed, try again with fuzzy matching on postcode
    if len(search_area) == 0:
        search_area = []
        if 'first_number' in addy:
            search_area = reduce_search_space(linz, 'address_number_int', int(addy['first_number']), search_area=search_area, matcher = None)
        if 'postcode' in addy:
            search_area = reduce_search_space(linz, 'postcode', addy['postcode'], search_area = search_area, matcher = fuzz.ratio, confidence=0)
            score_cols.append('postcode_score')

    if 'street_name' in addy:
        search_area = reduce_search_space(linz, 'full_road_name_ascii',addy['street_name'], search_area=search_area, matcher = fuzz.ratio, confidence=confidence)
        score_cols.append('full_road_name_ascii_score')

    if 'suburb_town_city' in addy:
        search_area = reduce_search_space(linz, 'suburb_town_city',addy['suburb_town_city'], search_area=search_area, matcher = fuzz.partial_ratio, confidence = confidence)
        score_cols.append('suburb_town_city_score')

    # unit
    search_area = reduce_search_space(linz, 'unit_value',addy.get('unit',''), search_area=search_area, matcher = fuzz.ratio, confidence = 0)
    score_cols.append('unit_value_score')

    # first number suffix
    search_area = reduce_search_space(linz, 'address_number_suffix',addy.get('first_number_suffix',''), search_area=search_area, matcher = fuzz.ratio, confidence = 0)
    score_cols.append('address_number_suffix_score')

    # second number
    # search_area = reduce_search_space(linz, 'address_number_high',addy.get('second_number',''), search_area=search_area, matcher = fuzz.ratio, confidence = 0)
    # score_cols.append('address_number_high_score')

    if len(search_area) == 0:
        return None

    return conclude_search(search_area, weights, score_cols, return_cols)

def conclude_search(search_area, weights, score_cols, return_cols):
    search_area['match_score'] = np.sum([weights[col]*search_area[col] for col in score_cols],axis=0)/sum([weights[col] for col in score_cols])
    mappings = search_area.loc[search_area['match_score'].idxmax()][return_cols].to_dict()
    return  {k: v for k, v in mappings.items() if v != ''}

def reduce_search_space(linz, search_col, search_term, search_area, matcher=fuzz.ratio, confidence = 20):
    """
    helper function for address lookup to iteratively reduce search space in LINZ dataset
    """

    if matcher is None: # exact match
        if len(search_area) == 0:
            search_area = linz[linz[search_col].values == search_term].copy()
        else:
            search_area = search_area[search_area[search_col].values == search_term]
    else: # fuzzy match
        if len(search_area) == 0:
            search_area = linz.copy()
        res = process.extract(search_term,search_area[search_col].str.upper(), scorer = matcher, score_cutoff=confidence, workers = -1, limit=len(search_area))
        search_area = search_area.loc[[x[2] for x in res]]
        search_area[search_col + '_score'] = [x[1] for x in res]
    return search_area


def get_matches_df(sparse_matrix, A, B, top=100):
    non_zeros = sparse_matrix.nonzero()

    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]

    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size

    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similairity = np.zeros(nr_matches)

    for index in range(0, nr_matches):
        left_side[index] = A[sparserows[index]]
        right_side[index] = B[sparsecols[index]]
        similairity[index] = sparse_matrix.data[index]

    return pd.DataFrame({'left_side': left_side,
                         'right_side': right_side,
                         'similairity': similairity})

def join_address(addy):
    parts = ''
    
    if 'unit' in addy:
        parts += addy['unit'] + '/'

    parts += addy.get('first_number','')
    parts += addy.get('first_number_suffix','')

    parts += ' ' + addy.get('street_name','')
    
    if 'suburb_town_city' in addy:
        parts += ', ' + addy.get('suburb_town_city','')
        
    if 'postcode' in addy:
        parts += ', ' + addy.get('postcode','')

    return parts