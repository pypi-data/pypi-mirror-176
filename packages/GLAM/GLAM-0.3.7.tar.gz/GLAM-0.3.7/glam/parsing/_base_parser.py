import tensorflow as tf
import os

from glam.parsing import _linz, _dataset, _predict


class BaseParser():

    def __init__(self, model):
        self.type = None
        self.model_path = None
        self.model = None

    def __repr__(self):
        return self.type

    def load_model(self):

        print('Loading parser dependencies...')
        try:
            return _predict.load_model(self.model_path)
        except:
            for m in sorted(os.listdir(self.model_path), reverse=True):
                try:
                    print(f'Trying to load {m}')
                    model =  _predict.load_model(os.path.join(self.model_path,m))
                    print(f'Success')
                    return model
                except:
                    print('Failed')
        
        print('Failed to load model')


    def make_training_data(self, data_dir, n_records = 0, val_split = 0.2):
        raw_linz_path = os.path.join(data_dir,'nz-street-address.csv')
        data_path = os.path.join(data_dir,'parsing')
        balanced_linz_path = os.path.join(data_path,'linz_balanced.csv')

        os.makedirs(data_path, exist_ok=True)
        if not os.path.isfile(balanced_linz_path):
            print('Balanced LINZ file not found. Creating...')
            _linz.balance_linz(raw_linz_path, balanced_linz_path)
        else:
            print('Using existing balanced LINZ file')

        _dataset.build_dataset(balanced_linz_path, data_path, n_records, val_split)

    def parse_addresses(self, addresses, post_process = True):
        if self.model is None:
            self.model = self.load_model()

        addresses = _predict.parse_addresses(
            addresses, 
            self.model,
            post_process=post_process
        )
        return addresses

    def find_training_data(self, data_dir):

        def check_train_val(dir):
            train = os.path.isfile(
                os.path.join(dir,'train.tfrecord')
            )
            val = os.path.isfile(
                os.path.join(dir,'val.tfrecord')
            ) 
            return (train and val)

        search_places = [
            os.path.join(data_dir,'parsing',self.type),
            os.path.join(data_dir,'parsing')
        ]

        for place in search_places:
            if check_train_val(place):
                return place
        
        raise ValueError('Training data not found.')

