import tensorflow as tf
import pandas as pd
import numpy as np
from scipy.spatial import KDTree
import string, re
import os
import random
from tqdm import tqdm
tqdm.pandas()

from glam.utils import lookups, typo
from glam.utils.utils import choose, build_address
from glam.matcher import predict


def generate_unit(s): 
    return s

def generate_first_number(s):
    return s

def generate_first_number_suffix(s):
    return s

def generate_second_number(s):
    return s

def generate_street_name(s):

    if len(s) == 0:
        return s

    # abbreviate street suffix
    def abbreviate_street(s):
        for k in lookups.street_abbreviations_reversed.keys():
            if k.lower() in s.lower():
                s = re.sub(k+'$',lookups.street_abbreviations_reversed[k],s,flags = re.IGNORECASE)
                continue
        return s

    s = choose(lambda : abbreviate_street(s), lambda : s)
    s = choose(lambda : typo.generate_typo(s), lambda : s)

    return s

def generate_suburb_town_city(s):
    
    def remove_vowels(s):
        return re.sub(r'[aeiou]','',s,flags=re.IGNORECASE)

    words = s.split(' ')

    new_word = []
    for word in words:
        new_word.append(choose(lambda : remove_vowels(word), lambda : word, chance1 = 0.05))
    
    words = ' '.join(new_word)

    if np.random.uniform() < 0.6:
        words.replace(',','')

    return choose(lambda : typo.generate_typo(words), lambda : words)

def generate_postcode(s):
    return s


def synthesise_positive_address(record):
    '''
    creates randomish address string with labels based on a linz record encoded from vocab and labels list
    
    Inputs:
        record: a row from the linz dataset
    Outputs:
        encoded address and labels
    '''

    parts = []
    to_shuffle = []

    # gather all the parts
    # unit = generate_unit(record['unit'])
    first_number = generate_first_number(record['address_number'])
    # first_number_suffix = generate_first_number_suffix(record['first_number_suffix'])
    # second_number = '' #generate_second_number(record['second_number'])
    street = generate_street_name(record['full_road_name_ascii'])
    suburb_town_city = generate_suburb_town_city(record['suburb_town_city'])
    postcode = generate_postcode(record['postcode'])

    # # organise numbers up front
    # if len(unit) > 0:
    #     head = unit + '/' + first_number + first_number_suffix
    # elif len(second_number) > 0:
    #     head = first_number + first_number_suffix + '-' + second_number
    # else:
    #     head = first_number + first_number_suffix
                           
    # # usually include street numbers
    # if np.random.uniform() <= 0.80:
    #     parts.append(head)

    if np.random.uniform() <= 0.90:
        parts.append(first_number)

    # always include the street
    parts.append(street)

    if np.random.uniform() <= 0.50:
        parts += [suburb_town_city]
    if np.random.uniform() <= 0.50:
        parts += [postcode]
    
    address = ' '.join(parts).lower()

    return address

def synthesise_negative_address(record):
    
    # how many components to break
    address_features = ['unit','address_number','first_number_suffix','full_road_name_ascii','suburb_town_city','postcode']
    n = min(
        int(np.random.exponential(1)) + 1,
        len(address_features)
    )

    to_break = random.sample(address_features,n)

    compulsory = ['address_number','full_road_name_ascii','suburb_town_city']

    if len(set(to_break).intersection(set(compulsory))) == 0:
        to_break.append(random.choice(compulsory))

    components = {}
    for feature in address_features:
        components[feature] = record['wrong_'+feature] if feature in to_break else record[feature]

    return build_address(
        # unit = components['unit'],
        first_number = components['address_number'],  
        # first_number_suffix = components['first_number_suffix'],
        street_name = components['full_road_name_ascii'],  
        suburb = components['suburb_town_city'],
        postcode = components['postcode'],
    )

def generate_followup_dataset(balanced_linz, outdir, n_records = 0, val_split = 0.2, model = 'default_model'):    

        # load in the balanced linz dataset
    linz = pd.read_csv(balanced_linz, dtype=str).fillna('')

    # sample from linz dataset
    if n_records == 0:
        samp = linz
    else:
        samp = linz.sample(n_records)

    def apply_build_anchor_address(x):
        return build_address(
            # unit = x['unit'],
            first_number = x['address_number'],
            # first_number_suffix = x['first_number_suffix'],
            # second_number = x['second_number'],
            street_name = x['full_road_name_ascii'],
            suburb = x['suburb_town_city'],
            postcode = x['postcode']
        )

    # anchor is now the search term
    print('Generating anchor addresses...')
    samp['anchor'] = samp.progress_apply(synthesise_positive_address, axis = 1)

    # true address is the positive case
    print('Generating positive addresses...')
    samp['positive'] = samp.progress_apply(apply_build_anchor_address, axis = 1)

    # current best match is the negative address
    print('Generating negative addresses...')

    samp['positive_embeddings'] = predict.compute_embeddings(samp['positive'], model=model)
    samp['anchor_embeddings'] = predict.compute_embeddings(samp['anchor'], model=model)
    kdt = KDTree(samp['positive_embeddings'].to_list())

    _ , samp['ids'] = kdt.query(samp['anchor_embeddings'].to_list())
    samp['negative'] = samp.iloc[samp['ids']]['positive'].to_list()
    samp = samp[samp['positive'] != samp['negative']]

     # apply test/val split
    val = samp.sample(int(val_split*len(samp)))
    train = samp.drop(val.index)

    def process_triplets(df):
        anchors = df['anchor'].str.lower().to_list()
        positives = df['positive'].str.lower().to_list()
        negatives = df['negative'].str.lower().to_list()
        return zip(anchors, positives, negatives)

    def write_ds(ds, path):
        with tf.io.TFRecordWriter(path) as file_writer:
            for anchor,positive,negative in ds:
                record_bytes = tf.train.Example(
                    features=tf.train.Features(feature={
                    "anchor"  : tf.train.Feature(bytes_list=tf.train.BytesList(value=[anchor.encode()])),
                    "positive": tf.train.Feature(bytes_list=tf.train.BytesList(value=[positive.encode()])),
                    "negative": tf.train.Feature(bytes_list=tf.train.BytesList(value=[negative.encode()])),
                })).SerializeToString()

                file_writer.write(record_bytes)

    # pad encoded addresses and labels
    val = process_triplets(val)
    train = process_triplets(train)

    # write datasets to tfrecords file
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    train_path = os.path.join(outdir, 'train.tfrecord')
    val_path = os.path.join(outdir, 'val.tfrecord')

    print('writing train set to tfrecord file as ' + train_path)
    write_ds(train,path = train_path)
    print('writing validation set to tfrecord file at ' + val_path)
    write_ds(val,path = val_path)
    print('complete')

    return samp

    
    
def build_dataset(balanced_linz, outdir, n_records = 0, val_split = 0.2):    
    """
    Generates training and validation tfrecord files from balanced linz csv which must be created beforehand
    Inputs:
        n_records:         the number of total (training + validation) rows to create from the balanced linz dataset. defaults to length of linz dataset
        val_split:         the portion of training data to withhold for validation set
        path:              the path to store the produced training and validation sets
    Outputs:
        return:            returns None. Saves training and validation tfrecord files to specified path
    """

    # load in the balanced linz dataset
    linz = pd.read_csv(balanced_linz, dtype=str).fillna('')

    # sample from linz dataset
    if n_records == 0:
        samp = linz
    else:
        samp = linz.sample(n_records)

    def apply_build_anchor_address(x):
        return build_address(
            # unit = x['unit'],
            first_number = x['address_number'],
            # first_number_suffix = x['first_number_suffix'],
            # second_number = x['second_number'],
            street_name = x['full_road_name_ascii'],
            suburb = x['suburb_town_city'],
            postcode = x['postcode']
        )

    # make triplets with some randomness 
    print('Generating anchor addresses...')
    samp['anchor'] = samp.progress_apply(apply_build_anchor_address, axis = 1)

    print('Generating positive addresses...')
    samp['positive'] = samp.progress_apply(synthesise_positive_address, axis = 1)

    print('Generating negative addresses...')

    for feature in ['unit','address_number','first_number_suffix','full_road_name_ascii','suburb_town_city','postcode']:
        samp['wrong_' + feature] = np.random.permutation(samp[feature].values)

    samp['negative'] = samp.progress_apply(lambda x: synthesise_negative_address(x), axis = 1)

    # apply test/val split
    val = samp.sample(int(val_split*len(samp)))
    train = samp.drop(val.index)

    def process_triplets(df):
        anchors = df['anchor'].str.lower().to_list()
        positives = df['positive'].str.lower().to_list()
        negatives = df['negative'].str.lower().to_list()
        return zip(anchors, positives, negatives)

    def write_ds(ds, path):
        with tf.io.TFRecordWriter(path) as file_writer:
            for anchor,positive,negative in ds:
                record_bytes = tf.train.Example(
                    features=tf.train.Features(feature={
                    "anchor"  : tf.train.Feature(bytes_list=tf.train.BytesList(value=[anchor.encode()])),
                    "positive": tf.train.Feature(bytes_list=tf.train.BytesList(value=[positive.encode()])),
                    "negative": tf.train.Feature(bytes_list=tf.train.BytesList(value=[negative.encode()])),
                })).SerializeToString()

                file_writer.write(record_bytes)

    # pad encoded addresses and labels
    val = process_triplets(val)
    train = process_triplets(train)

    # write datasets to tfrecords file
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    train_path = os.path.join(outdir, 'train.tfrecord')
    val_path = os.path.join(outdir, 'val.tfrecord')

    print('writing train set to tfrecord file as ' + train_path)
    write_ds(train,path = train_path)
    print('writing validation set to tfrecord file at ' + val_path)
    write_ds(val,path = val_path)
    print('complete')
