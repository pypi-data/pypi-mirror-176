from base64 import encode
import tensorflow as tf
tf.autograph.set_verbosity(0)
import os
import datetime
import string

from glam.matcher import siamese

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
            # log_dir = os.path.join(callback_dir,'tensorboard'), 
            log_dir = callback_dir,
            histogram_freq = 1,
            update_freq='batch'
        )
    )

    callbacks.append(
        tf.keras.callbacks.CSVLogger(
            filename = os.path.join(callback_dir,'log.csv'), 
        )
    )

    return callbacks


def train_model(data_dir, save_dir=None, log_dir=None, model_dir = '', max_epochs = 100, batch_size = 128):
    """
    train a tf model on specified training data. If a model is passed, its structure and weights will be used, otherwise a new model is made with input params
    """
    
    # load in the training data

    # Create a dictionary describing the features.
    description = {
        'anchor': tf.io.FixedLenSequenceFeature([], tf.string, allow_missing=True),
        'positive': tf.io.FixedLenSequenceFeature([], tf.string, allow_missing=True),
        'negative': tf.io.FixedLenSequenceFeature([], tf.string, allow_missing=True)
    }

    train_ds = read_ds(
        os.path.join(data_dir,'train.tfrecord'),
        description, 
        batch_size
    ).map(lambda x: (x['anchor'], x['positive'], x['negative']))

    val_ds = read_ds(
        os.path.join(data_dir, 'val.tfrecord'),
        description, 
        batch_size
    ).map(lambda x: (x['anchor'], x['positive'], x['negative']))

    callbacks_path = os.path.join(log_dir,'callbacks')
    if not os.path.exists(callbacks_path): os.makedirs(callbacks_path)
    callbacks = create_callbacks(callbacks_path)

    embedding_model = build_embedding_model()
    siamese_model = build_siamese_model(embedding_model)

    # horrendous hack
    for x in train_ds:
        _ = siamese_model(x)
        break

    print('model dir:', model_dir)

    if len(model_dir) > 0:
        print('loading weights from: ' + model_dir)
        loaded = tf.keras.models.load_model(model_dir)
        embedding_model.set_weights(loaded.get_weights())
    # elif siamese_model_dir is not None:
    #     loaded = tf.keras.models.load_model(siamese_model_dir)
    #     siamese_model.set_weights(loaded.get_weights())
  
    history = siamese_model.fit(
        train_ds, 
        validation_data = val_ds, 
        callbacks = callbacks, 
        epochs = max_epochs,
    )

    if save_dir is None:
        save_dir = os.path.join('glam','matcher','models',datetime.datetime.now().strftime(r'%y%m%d-%H'))

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir)
    print('saving model to ' + save_path)
    embedding_model.save(save_path)

    return history 


