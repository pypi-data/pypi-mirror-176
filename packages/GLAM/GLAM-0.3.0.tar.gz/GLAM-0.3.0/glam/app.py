"""Manages the app flow as it imports and transforms modelling data."""

from typing import List
from glam.app_conf import AppConf
import importlib
import os

def run_app(app_conf: AppConf):
    """Main entry-point to the application."""

    try:
        os.makedirs(app_conf.input_dir, exist_ok = True)
        os.makedirs(app_conf.output_dir, exist_ok = True)
    except:
        pass

    if app_conf.mode == 'design':
        linz = importlib.import_module("glam.{}.linz".format(app_conf.model))
        
        linz.balance_linz(
            os.path.join(app_conf.input_dir,'nz-street-address.csv'), 
            os.path.join(app_conf.output_dir,'balanced_linz.csv')
        )

    if app_conf.mode == 'build':
        dataset = importlib.import_module("glam.{}.dataset".format(app_conf.model))

        dataset.build_dataset(
            os.path.join(app_conf.input_dir,'balanced_linz.csv'), 
            os.path.join(app_conf.output_dir),
            n_records = 0, # use all records available
            val_split = 0.2
        )  

    if app_conf.mode == 'train':
        train = importlib.import_module( "glam.{}.train".format(app_conf.model))
        
        history = train.train_model(
            data_dir = app_conf.input_dir,
            save_dir = app_conf.output_dir,
            log_dir = app_conf.log_dir,
            model_dir = app_conf.model_dir,
            max_epochs = app_conf.max_epochs,
            batch_size = app_conf.batch_size,
        )

    if app_conf.mode == 'index':
        train = importlib.import_module( "glam.{}.train".format(app_conf.model))

    if app_conf.mode == 'predict':
        return 0

    if app_conf.mode == 'geocode': 
        return 0

        
    # invalid mode
    return -1
