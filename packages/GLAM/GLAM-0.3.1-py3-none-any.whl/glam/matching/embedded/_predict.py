from distutils.archive_util import make_archive
import os
from scipy.spatial import cKDTree
import pandas as pd
import numpy as np
from tqdm import tqdm

from glam.matching.embedded._model import make_embeddings

def lookup_addresses(addresses, linz, trees, batch_size = 64):
    # embed addresses
    parsed_addresses = pd.DataFrame([x if x is not None else {} for x in addresses]).fillna('None')

    parsed_addresses['embedding'] = parsed_addresses.apply(make_embeddings, axis = 1)
    parsed_addresses['embedding_dim'] = parsed_addresses['embedding'].apply(len)
    parsed_addresses['batch'] = parsed_addresses.groupby('embedding_dim')['street_name'].rank(method='first') // batch_size
    # parsed_addresses['batch'] = 1

    # group addresses
    grouped = parsed_addresses.groupby(['embedding_dim', 'batch'])
    n = len(grouped)
    N = len(addresses)

    matches = [zip(embeddings.index,query_tree(embeddings['embedding'], trees[embedding_dim])) for (embedding_dim, batch), embeddings in tqdm(grouped, unit_scale=N/n, desc = 'Matching addresses')]

    matches = (
        pd.DataFrame(
            [(id, match, dist) for query in matches for id,(dist,match) in query], 
            columns = ['id', 'match', 'embedding_distance']
            )
            .sort_values('id')
            .set_index('id', drop=True)
    )

    return_cols = ['unit_value','address_number','address_number_suffix','address_number_high','full_road_name_ascii','suburb_locality_ascii','town_city_ascii','shape_X','shape_Y','embedding_distance']
    df = matches.merge(linz, left_on='match', how='left', right_index=True)[return_cols].to_dict('records')
    return df

def lookup_addresses_not(addresses, linz, trees, batch_size = 256):

    # embed addresses
    parsed_addresses = pd.DataFrame([x if x is not None else {} for x in addresses]).fillna('None')

    parsed_addresses['embedding'] = parsed_addresses.apply(make_embeddings, axis = 1)
    parsed_addresses['embedding_dim'] = parsed_addresses['embedding'].apply(len)

    # group addresses
    grouped = parsed_addresses.groupby(['embedding_dim'])
    n = len(grouped)
    N = len(addresses)
    
    matches = [zip(df.index, query_tree(df['embedding'], trees[embedding_dim])) for embedding_dim, df in tqdm(grouped, unit_scale=N/n, desc = 'Matching addresses')]

    matches = (
        pd.DataFrame(
            [(id, match, dist) for query in matches for id,(dist,match) in query], 
            columns = ['id', 'match', 'embedding_distance']
            )
            .sort_values('id')
            .set_index('id', drop=True)
    )

    return_cols = ['unit_value','address_number','address_number_suffix','address_number_high','full_road_name_ascii','suburb_locality_ascii','town_city_ascii','shape_X','shape_Y','embedding_distance']
    df = matches.merge(linz, left_on='match', how='left', right_index=True)[return_cols].to_dict('records')
    return df

def lookup_addresses_old(addresses, linz, trees):

    # embed addresses
    parsed_addresses = pd.DataFrame([x if x is not None else {} for x in addresses]).fillna('None')

    parsed_addresses['embedding'] = parsed_addresses.apply(make_embeddings, axis = 1)
    parsed_addresses['embedding_dim'] = parsed_addresses['embedding'].apply(len)

    # group addresses
    matches = [zip(embeddings.index,query_tree(embeddings['embedding'], trees[embedding_dim])) for embedding_dim, embeddings in parsed_addresses.groupby(['embedding_dim'])]
    matches = (
        pd.DataFrame(
            [(id, match, dist) for query in matches for id,(dist,match) in query], 
            columns = ['id', 'match', 'embedding_distance']
            )
            .sort_values('id')
            .set_index('id', drop=True)
    )

    return_cols = ['unit_value','address_number','address_number_suffix','address_number_high','full_road_name_ascii','suburb_locality_ascii','town_city_ascii','shape_X','shape_Y','embedding_distance']
    df = matches.merge(linz, left_on='match', how='left', right_index=True)[return_cols].to_dict('records')
    return df


def query_tree(embeddings, tree):
    dist, idx = tree.query(embeddings.to_list())
    return zip(dist,idx)



