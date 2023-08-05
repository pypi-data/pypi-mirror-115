# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Constants for the package."""

from enum import Enum


class SystemSettings:
    """System settings."""
    NAMESPACE = 'azureml.automl.dnn.nlp'
    LOG_FILENAME = 'azureml_automl_nlp.log'
    LOG_FOLDER = 'logs'


class OutputLiterals:
    """Directory and file names for artifacts."""
    NER_MODEL_FILE_NAME = 'pytorch_model.bin'
    MULTILABEL_MODEL_FILE_NAME = 'model.pt'
    VECTORIZER_FILE_NAME = 'vectorizer.pkl'
    CHECKPOINT_FILE_NAME = 'checkpoint'
    TOKENIZER_FILE_NAME = 'tokenizer_config.json'
    CONFIG_FILE_NAME = 'config.json'
    OUTPUT_DIR = './outputs'
    SCORE_SCRIPT = 'score_script.py'
    SCORE_SCRIPT_MULTICLASS = 'score_script_multiclass.py'
    TRAINING_ARGS = 'training_args.bin'
    LABELS_FILE = 'labels.txt'
    LABEL_LIST_FILENAME = 'label_list.npy'


class DataLiterals:
    """Directory and file names for artifacts."""
    NER_DATA_DIR = 'ner_data'


class ScoringLiterals:
    """String names for scoring settings"""
    RUN_ID = 'run_id'
    EXPERIMENT_NAME = 'experiment_name'
    OUTPUT_FILE = 'output_file'
    ROOT_DIR = 'root_dir'
    BATCH_SIZE = 'batch_size'
    INPUT_DATASET_ID = 'input_dataset_id'
    LABEL_COLUMN_NAME = 'label_column_name'
    LOG_OUTPUT_FILE_INFO = 'log_output_file_info'
    ENABLE_DATAPOINT_ID_OUTPUT = 'enable_datapoint_id_output'


class LoggingLiterals:
    """Literals that help logging and correlating different training runs."""
    PROJECT_ID = 'project_id'
    VERSION_NUMBER = 'version_number'
    TASK_TYPE = 'task_type'


class NERModelParameters:
    """Default model parameters for NER"""
    MAX_SEQ_LENGTH = 128
    MODEL_NAME = "bert-base-cased"
    NUM_TRAIN_EPOCHS = 3
    OVERWRITE_CACHE = False
    PER_DEVICE_TRAIN_BATCH_SIZE = 32
    SAVE_STEPS = 750
    TASK_NAME = "ner"


class Warnings:
    """Warning strings."""
    CPU_DEVICE_WARNING = "The device being used for training is 'cpu'. Training can be slow and may lead to " \
                         "out of memory errors. Please switch to a compute with gpu devices. " \
                         "If you are already running on a compute with gpu devices, please check to make sure " \
                         "your nvidia drivers are compatible with torch version {}."


class Split(Enum):
    """Split Enum Class."""
    train = "train"
    dev = "dev"
    test = "test"
