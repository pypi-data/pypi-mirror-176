import tensorflow as tf
import pandas as pd
import numpy as np
import string, re
import os
import random
from tqdm import tqdm
tqdm.pandas()

from glam.utils import lookups, typo
from glam.utils.utils import choose

from glam.parser.dataset import labels_list, labels, join_str_and_labels

labels_list = [
    'blank',
    'building_name',  
    'level',
    'unit', 
    'first_number',  
    'first_number_suffix',
    'second_number',    
    'street_name',  
    'suburb_town_city',
    'postcode',
]


def generate_unit(s): 
    return labels(s,'unit')

def generate_first_number(s):
    return labels(s,'first_number')

def generate_first_number_suffix(s):
    return labels(s,'first_number_suffix')

def generate_second_number(s):
    return labels(s,'second_number')

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

    return labels(s,'street_name')

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

    s = choose(lambda : typo.generate_typo(words), lambda : words)

    return labels(s,'suburb_town_city')

def generate_postcode(s):
    return labels(s,'postcode')


def build_address_and_labels(unit = '',first_number = '',  first_number_suffix = '',second_number = '',    street_name = '',  suburb = '',town_city = '',postcode = ''):

    head = []
    if len(unit) > 0:
        head.append(unit) 
    if len(unit) > 0 and len(first_number) > 0:
        if len(unit[0])>0 and len(first_number[0])>0:
            head.append( labels('/','blank'))
        
    head.append(first_number)
    head.append(first_number_suffix)

    if len(second_number) > 0 and len(head) > 0:
        head.append(labels('-','blanks')) 
    elif len(second_number) > 0:
        head.append(second_number)

    head = join_str_and_labels(head, sep='')

    addy = [head, street_name,suburb, town_city, postcode]
    addy = join_str_and_labels([part for part in addy if len(part) > 0])

    return addy


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
    unit = generate_unit(record['unit'])
    first_number = generate_first_number(record['address_number'])
    first_number_suffix = generate_first_number_suffix(record['first_number_suffix'])
    second_number = '' #generate_second_number(record['second_number'])
    street = generate_street_name(record['full_road_name_ascii'])
    suburb_town_city = generate_suburb_town_city(record['suburb_town_city'])
    postcode = generate_postcode(record['postcode'])

    # organise numbers up front
    if len(unit[0]) > 0:
        head = join_str_and_labels([unit, labels('/','blank'), first_number, first_number_suffix],sep='')
    else:
        head = join_str_and_labels([first_number, first_number_suffix],sep='')

                                    
    # usually include street numbers
    if np.random.uniform() <= 0.80:
        parts.append(head)

    # always include the street
    parts.append(street)

    if np.random.uniform() <= 0.50:
        parts.append(suburb_town_city)
    if np.random.uniform() <= 0.50:
        parts.append(postcode)
    
    address = join_str_and_labels(parts)

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

    return build_address_and_labels(
        unit =                     labels(components['unit'],'unit'),
        first_number =             labels(components['address_number'],  'first_number'),
        first_number_suffix =      labels(components['first_number_suffix'],'first_number_suffix'),
        street_name =              labels(components['full_road_name_ascii'],  'street_name'),
        suburb =                   labels(components['suburb_town_city'],'suburb_town_city'),
        postcode =                 labels(components['postcode'],'postcode'),
    )

    
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
        return build_address_and_labels(
            unit =                     labels(x['unit'],'unit'),
            first_number =             labels(x['address_number'],'first_number'),
            first_number_suffix =      labels(x['first_number_suffix'],'first_number_suffix'),
            # second_number =          labels(x['second_number'],'second_number'),
            street_name =              labels(x['full_road_name_ascii'],'street_name'),
            suburb =                   labels(x['suburb_town_city'],'suburb_town_city'),
            postcode =                 labels(x['postcode'],'postcode'),
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

    return samp

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