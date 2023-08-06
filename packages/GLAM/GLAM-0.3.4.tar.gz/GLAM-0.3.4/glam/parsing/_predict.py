import tensorflow as tf
import numpy as np
import re

from glam.parsing import _dataset
from glam.utils import lookups, tqdm_predict_callback

def load_model(path):
    return tf.keras.models.load_model(path)

def predict_one_inference(address, model, probs = False):

    pred = predict_inference(address, model, string_labels = True, probs=probs)

    for x in zip(address,pred):
        print(x)


def predict_inference(addresses, model, string_labels = False, probs = False):
    
    if type(addresses) == str:
        addresses = [addresses]

    #encode and pad address input
    encoded_addresses = [tf.constant(_dataset.vocab_lookup(addy)) for addy in addresses]
    encoded_addresses = tf.keras.preprocessing.sequence.pad_sequences(encoded_addresses,padding='post')

    #make prediction and convert to probs
    pred = tf.keras.layers.Softmax()(model.predict(encoded_addresses))
    prob = np.max(pred,axis=2)[0]
    labels = np.argmax(pred,axis=2)[0]

    if string_labels:
        labels = [_dataset.labels_list[i] for i in labels]

    if probs:
         return list(zip(labels,prob))

    return labels

def parse_addresses(addresses, model, post_process, batch_size = 256):
    """
    Parse raw address strings and return labelled predictions

    Inputs:
        addresses: list of address strings to be parsed
        model: model to use when making predictions. If none is supplied the default pretrained model will be used
        post_process: whether to apply postprocessing to the parsed addresses or not. Default true
    Outputs:
        list of parsed addresses in dictionary format
    """

    # if a single address was passed, convert it into a list
    if type(addresses) == str:
        addresses = [addresses]

    # create padded list of addresses
    encoded_addresses = [tf.constant(_dataset.vocab_lookup(addy)) for addy in addresses]
    encoded_addresses = tf.keras.preprocessing.sequence.pad_sequences(encoded_addresses,padding='post')

    cb = tqdm_predict_callback.TQDMPredictCallback(unit_scale=batch_size, desc = 'Parsing addresses', position=0, leave=True)

    # pred = model.predict(encoded_addresses, callbacks = [cb], batch_size = batch_size)
    pred = model.predict(encoded_addresses, callbacks = [], batch_size = batch_size)
    result = np.argmax(pred,axis=2)

    def make_mappings(addy,res,post_process):
        mappings = dict()
        for char, class_id in zip(addy.upper(), res):
            if class_id == 0:
                continue
            cls = _dataset.labels_list[class_id]
            mappings[cls] = mappings.get(cls, "") + char

        if post_process:
            mappings = post_process_mappings(mappings)
        return mappings

    #convert predictions to dictionary format
    return [make_mappings(addy,res,post_process) for addy, res in zip(addresses, result)]
        
def post_process_mappings(mappings):

    if 'street_name' in mappings:
            mappings['street_name'] = normalise_street_type(mappings['street_name'])
    if 'first_number' in mappings:
        mappings['first_number'] = normalise_first_number(mappings['first_number'])
    if 'unit' in mappings:
        mappings['unit'] = normalise_first_number(mappings['unit'])
    if 'level' in mappings:
        mappings['level'] = normalise_level(mappings['level'])
    if 'postcode' in mappings:
        mappings['postcode'] = normalise_post_code(mappings['postcode'])

    mappings = {k: remove_illegal_chars(v) for k, v in mappings.items() if v is not None}
    if ('street_name' not in mappings) or ('first_number' not in mappings):
        mappings = None

    return mappings


def normalise_street_type(street_name):
    split_text = street_name.split()
    for i, word in enumerate(split_text):
        clean_word = re.sub(r'[ ,.\-]','',word)
        if clean_word in lookups.street_abbreviations:
            return ' '.join(split_text[:i] + [lookups.street_abbreviations[clean_word]] + split_text[i+1:])
    
    return street_name

def normalise_post_code(postcode):
    postcode = re.sub(r"[a-zA-Z,.\- ]", "", postcode)
    if len(postcode) != 4:
        return None
    return postcode

def normalise_unit(unit):
        numbers = re.sub(r"[a-zA-Z,.\- ]", "", unit)
        if len(numbers) > 0:
            return numbers
        
        for word in unit.lower().split():
            if word in lookups.ordinal_words:
                return str(lookups.ordinal_words.index(word)+1)
            if word in lookups.cardinal_words:
                return str(lookups.cardinal_words.index(word)+1)
        
        return unit

def normalise_level(level):
    numbers = re.sub(r"[a-zA-Z,.\- ]", "", level)
    if len(numbers) > 0:
        return numbers
    
    for word in level.lower().split():
        if word in lookups.ordinal_words:
            return str(lookups.ordinal_words.index(word)+1)
        if word in lookups.cardinal_words:
            return str(lookups.cardinal_words.index(word)+1)

    return level

def normalise_first_number(first_number):
    first_number = re.sub(r"[^0-9]", "", first_number)
    if len(first_number) == 0:
        return None
    return first_number


def remove_illegal_chars(string):
    return re.sub('[^A-Za-z0-9 ,]+', '', string)

    