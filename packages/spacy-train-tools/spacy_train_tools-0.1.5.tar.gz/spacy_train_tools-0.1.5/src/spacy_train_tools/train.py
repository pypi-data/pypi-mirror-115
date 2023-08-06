import logging
import os
import tempfile
from pathlib import Path
from uuid import uuid1

from py_profiler import profiler, profiling_service

from .command_line import run_command_line
from .utils import convert_to_spacy_doc_file


@profiler("train_spacy_model")
def train_spacy_model(
        config_file: str,
        vector_file: str,
        train_file: str,
        dev_file: str,
        output_folder: str
):

    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_train_file = f'{temp_dir}/{uuid1()}.spacy'
        tmp_dev_file = f'{temp_dir}/{uuid1()}.spacy'
        tmp_train_file = convert_to_spacy_doc_file(
            train_file,
            tmp_train_file,
            dataset_size=None,
            case_insensitive=True,
            remove_accent=False
        )

        tmp_dev_file = convert_to_spacy_doc_file(
            dev_file,
            tmp_dev_file,
            dataset_size=None,
            case_insensitive=True,
            remove_accent=False
        )

        run_command_line([
            'python3',
            '-m',
            'spacy',
            'train',
            config_file,
            '--output',
            output_folder,
            '--paths.train', tmp_train_file,
            '--paths.dev', tmp_dev_file,
            '--paths.vectors', vector_file
        ])

    logging.info(profiling_service.as_table())
    logging.info(f'Output model: {output_folder}')
