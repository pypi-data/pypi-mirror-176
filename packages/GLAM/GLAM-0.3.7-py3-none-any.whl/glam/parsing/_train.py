import tensorflow as tf
tf.autograph.set_verbosity(0)
import os
import datetime

from glam.parsing import _dataset

def read_ds(path, description, batch_size):

    raw_dataset = tf.data.TFRecordDataset(path)

    def _parse_raw_data(example):
        # Parse the input tf.train.Example proto using the dictionary above.
        return tf.io.parse_single_example(example, description)

    ds = raw_dataset.map(_parse_raw_data)
    ds = ds.batch(batch_size = batch_size)
    return ds

def create_callbacks(callback_dir):
    callbacks = []

    # save the best model so far
    callbacks.append(
        tf.keras.callbacks.ModelCheckpoint(
            filepath= os.path.join(callback_dir,'checkpoint'),
            save_weights_only=False,
            monitor='val_loss',
            mode='min',
            save_best_only=True
        )
    )

    callbacks.append(
        tf.keras.callbacks.EarlyStopping(
            monitor='loss', 
            patience=3
        )
    )

    callbacks.append(
        tf.keras.callbacks.TensorBoard(
            log_dir = callback_dir, 
            histogram_freq = 1,
            update_freq=500
        )
    )

    return callbacks

def make_class_weights():

    class_weights = { 
        0 : 0.1, # 'blank',
        1 : 5,   #'building_name',  
        2 : 5,   #'level',
        3 : 5,   #'unit', 
        4 : 5,   #'first_number',  
        5 : 5,   #'first_number_suffix',
        6 : 5,   #'second_number',    
        7 : 1,   #'street_name',  
        8 : 1,   #'suburb_town_city',
        9 : 1,   #'postcode',
    }

    class_weights = {x : class_weights.get(x,0) for x in range(150)}
