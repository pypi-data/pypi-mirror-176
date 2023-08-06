import tensorflow as tf
import pandas as pd
import numpy as np
import os

from traitlets import default
from glam.utils import TQDMPredictCallback
# from sklearn.metrics.pairwise import cosine_similarity

def load_model(model):
    path = os.path.join(os.path.dirname(__file__), 'models') 
    return tf.keras.models.load_model(os.path.join(path,model))

def compute_embeddings(addresses, model = 'default_model', batch_size = 1024):
    
    embedder = load_model(model)
    return embedder.predict([[addy] for addy in addresses], batch_size = batch_size, callbacks = [TQDMPredictCallback.TQDMPredictCallback()]).tolist()


# def chunker(from_embeddings, to_embeddings, batch_size):
#     for i in range(0, len(from_embeddings), batch_size):
#         yield cosine_similarity(to_embeddings, from_embeddings[i:i+batch_size]).argmax(axis=0)


# def match_embeddings(from_embeddings, to_embeddings, batch_size = 128):      
#     from_embeddings = list(from_embeddings)
#     to_embeddings = list(to_embeddings)

#     results = np.concatenate([batch for batch in chunker(from_embeddings,to_embeddings,batch_size)])
#     return results
    



