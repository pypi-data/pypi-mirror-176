"""Module for application configuration."""

# https://stackoverflow.com/a/33533514
from __future__ import annotations

import argparse
import os

class AppConf:
    """Class for all application configuration."""

    def __init__(
        self,
        model: str,
        mode: str,
        input_dir : str, 
        output_dir : str,
        log_dir : str,
        model_dir : str,
        batch_size : str,
        max_epochs : str,
    ):
    
        """Initalise app conf."""
        self.model = model
        self.mode = mode
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.log_dir = log_dir
        self.model_dir = model_dir
        self.batch_size = int(batch_size)
        self.max_epochs = int(max_epochs)

    def argv_to_app_conf(args: list[str]) -> AppConf:
        """Parse the command-line arguments into an instance of AppConf."""
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "model", help="which model to train. One of: \{parser, matcher\}")
        parser.add_argument(
            "mode", help="What to do with the model. One of: \{build, train, predict\}")
        parser.add_argument(
            "input_dir", help="directory for data")
        parser.add_argument(
            "output_dir", help="directory to save outputs in")
        parser.add_argument(
            "--log_dir", help="directory to store logging info", default = 'logs')
        parser.add_argument(
            '--model_dir', help = 'specify model for predictions, or use if starting training from existing model ', default = '')
        parser.add_argument(
            '--batch_size', help = 'batch size to use for training/predicting', default = '256')
        parser.add_argument(
            '--max_epochs', help = 'Maximum number of epochs to run when training', default = '50')

        args, unknown = parser.parse_known_args(args)

        return AppConf(
            args.model,
            args.mode,
            args.input_dir,
            args.output_dir,
            args.log_dir,
            args.model_dir,
            args.batch_size,
            args.max_epochs
        )

