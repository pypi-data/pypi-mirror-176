import os
from datetime import datetime

from glam.parsing._base_parser import BaseParser
from glam.parsing import _train
from glam.parsing.rnn import _rnn_model

class RNNParser(BaseParser):
    
    def __init__(self, model='default_model'):
        self.type = 'RNN'
        self.model_path = os.path.join(
            os.path.dirname(__file__),
            model
        )

        self.model = None
        if os.path.isdir(self.model_path):
            self.model = self.load_model()
        else:
            os.makedirs(self.model_path)

    def train_model(self, data_dir, log_dir, max_epochs = 100, batch_size = 128):

        training_data = self.find_training_data(data_dir)

        _rnn_model.train_model(
            data_dir = training_data,
            save_dir = os.path.join(
                self.model_path,
                datetime.now().strftime(r'%y%m%d-%H')
                ),
            log_dir = log_dir,
            model_dir = self.model_path,
            max_epochs = max_epochs,
            batch_size = batch_size
            )

    
