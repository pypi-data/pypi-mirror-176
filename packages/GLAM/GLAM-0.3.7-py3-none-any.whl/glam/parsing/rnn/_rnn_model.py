from datetime import datetime
import tensorflow as tf
import os

from glam.parsing._dataset import vocab, n_labels
from glam.parsing import _train


def build_training_model():

    embedding_dim = 8
    rnn_size = 128
    dense_dim = 32
    dropout = 0.2
    
    address = tf.keras.Input((None,),name='address_ints',dtype=tf.int32)
    embedder = tf.keras.layers.Embedding(len(vocab)+1, embedding_dim, mask_zero=True, embeddings_initializer = tf.keras.initializers.GlorotNormal)
    rnn_layer1 = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(rnn_size, return_sequences=True, stateful=False, recurrent_dropout = dropout), name = 'LSTM1')
    rnn_layer2 = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(rnn_size, return_sequences=True, stateful=False, recurrent_dropout = dropout), name = 'LSTM2')
    dense_layer = tf.keras.layers.Dense(dense_dim,name='dense')
    output_layer = tf.keras.layers.Dense(n_labels,name='logits')

    # address_embeddings = embedder(address)
    # hidden_layer1 = rnn_layer1(address_embeddings)
    # logits = output_layer(hidden_output)

    model = tf.keras.models.Sequential([
        address,
        embedder,
        rnn_layer1,
        rnn_layer2,
        dense_layer,
        output_layer,
    ])
    
    return model


def train_model(data_dir, save_dir, log_dir, model_dir, max_epochs, batch_size):
    """
    train a tf model on specified training data. If a model is passed, its structure and weights will be used, otherwise a new model is made with input params
    """
    
    # load in the training data

    # Create a dictionary describing the features.
    description = {
        'x': tf.io.FixedLenSequenceFeature([], tf.int64, allow_missing = True),
        'y': tf.io.FixedLenSequenceFeature([], tf.int64, allow_missing = True)
    }

    train_ds = _train.read_ds(os.path.join(data_dir,'train.tfrecord'),description, batch_size).map(lambda x: (x['x'], x['y']))
    val_ds = _train.read_ds(os.path.join(data_dir, 'val.tfrecord'),description, batch_size).map(lambda x: (x['x'], x['y']))

    callbacks_path = os.path.join(log_dir,'callbacks')
    if not os.path.exists(callbacks_path): os.makedirs(callbacks_path)
    callbacks = _train.create_callbacks(callbacks_path)
    # class_weights = make_class_weights()

    try:
        model = tf.keras.models.load_model(model_dir)
        print('loaded model successfully')
    except:
        print('No model provided. Building new one')
        model = build_training_model()
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True,reduction=tf.keras.losses.Reduction.SUM)
        optimiser = tf.keras.optimizers.Nadam()
        model.compile(optimizer=optimiser, loss=loss, metrics = [tf.keras.metrics.SparseCategoricalAccuracy()])
    
    history = model.fit(
        train_ds, 
        validation_data = val_ds, 
        callbacks = callbacks, 
        epochs = max_epochs,
        # class_weight = class_weights
    )

    os.makedirs(save_dir, exist_ok = True)
    print('saving model to ' + save_dir)
    model.save(save_dir)

    return history