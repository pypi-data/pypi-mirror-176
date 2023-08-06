import tensorflow as tf
import string

from glam.matching import _siamese

def build_embedding_model():

    rnn_size = 64
    char_embedding_dim = 8
    dropout = 0.2
    embeddings = 128

    vocab = list(string.digits + string.ascii_lowercase + string.punctuation + string.whitespace)

    input_layer = tf.keras.Input(
        shape = (1),
        dtype = tf.string
    )
    encode_layer = tf.keras.layers.TextVectorization(
        # standardize = 'lower',
        split='character',
        vocabulary = vocab
    )
    embed_layer = tf.keras.layers.Embedding(
        len(vocab)+1, 
        char_embedding_dim, 
        mask_zero = True
    )
    lstm_layer1 = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(
        rnn_size, 
        recurrent_dropout = dropout,
        kernel_initializer = 'glorot_normal',
        return_sequences=True),
        name = 'LSTM1'
    )
    lstm_layer2 = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(
        rnn_size, 
        recurrent_dropout = dropout,
        kernel_initializer = 'glorot_normal',
        return_sequences=False),
        name = 'LSTM2'
    )
    output_layer = tf.keras.layers.Dense(
        embeddings, 
        # activation = 'sigmoid'
    )

    model = tf.keras.models.Sequential([
        input_layer,
        encode_layer,
        embed_layer,
        lstm_layer1,
        lstm_layer2,
        output_layer,
    ])

    return model



def build_siamese_model(embedding_model):
    anchor_input =   tf.keras.layers.Input(name="anchor", shape=(1,), dtype = tf.string)
    positive_input = tf.keras.layers.Input(name="positive", shape=(1,), dtype = tf.string)
    negative_input = tf.keras.layers.Input(name="negative", shape=(1,), dtype = tf.string)

    distances = _siamese.DistanceLayer()(
        embedding_model(anchor_input),
        embedding_model(positive_input),
        embedding_model(negative_input),
    )

    siamese_network = tf.keras.Model(
        inputs=[anchor_input, positive_input, negative_input], outputs=distances
    )

    siamese_model = _siamese.SiameseModel(siamese_network, margin = 2)
    siamese_model.compile(optimizer=tf.keras.optimizers.Adam(0.001))

    return siamese_model