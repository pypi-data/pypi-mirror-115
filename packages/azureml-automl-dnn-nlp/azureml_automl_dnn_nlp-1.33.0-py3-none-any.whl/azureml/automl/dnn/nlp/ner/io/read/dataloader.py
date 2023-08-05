# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains dataloader functions for NER."""

import logging
import os
from shutil import copyfile
from typing import List, Optional, Tuple

from torch.utils.data import Dataset
from transformers.tokenization_utils_base import PreTrainedTokenizerBase

from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.dnn.nlp.common.constants import NERModelParameters
from azureml.automl.dnn.nlp.common.data_utils import download_file_dataset
from azureml.automl.dnn.nlp.ner.io.read.dataset_wrapper import DatasetWrapper
from azureml.automl.dnn.nlp.ner.utils import Split
from azureml.core.workspace import Workspace

_logger = logging.getLogger(__name__)


def load_dataset(
        workspace: Workspace,
        data_dir: str,
        output_dir: str,
        labels_filename: str,
        tokenizer: PreTrainedTokenizerBase,
        dataset_id: str,
        validation_dataset_id: Optional[str],
) -> Tuple[Dataset, Dataset, List[str]]:
    """
    Save checkpoint to outputs directory.

    :param workspace: workspace where dataset is stored in blob
    :param data_dir: directory where data should be downloaded
    :param output_dir: directory where output files of the training should be saved
    :param labels_filename: file storing unique labels from train and validation data
    :param tokenizer: pretrained bert tokenizer
    :param dataset_id: Unique identifier to fetch dataset from datastore
    :param validation_dataset_id: Unique identifier to fetch validation dataset from datastore
    """

    # Validate dataset ids
    Contract.assert_true(
        dataset_id != validation_dataset_id,
        "validation_dataset_id",
        reference_code=ReferenceCodes._NER_DUPLICATE_DATASET_ID,
        log_safe=True
    )

    # Load datasets from FileDataset
    train_ds_filename = download_file_dataset(
        dataset_id,
        "Train Dataset",
        workspace,
        data_dir
    )

    validation_ds_filename = None
    eval_dataset = None
    if validation_dataset_id:
        validation_ds_filename = download_file_dataset(
            validation_dataset_id,
            "Validation Dataset",
            workspace,
            data_dir
        )

    # Get unique labels
    label_list = _get_label_list(data_dir, train_ds_filename)

    # Save label to refer during inference time
    _save_labels(data_dir, output_dir, labels_filename, label_list)

    # Load Dataset
    train_dataset = DatasetWrapper(
        data_dir=data_dir,
        dataset_file=train_ds_filename,
        tokenizer=tokenizer,
        labels=label_list,
        model_type="bert",
        max_seq_length=NERModelParameters.MAX_SEQ_LENGTH,
        mode=Split.train,
    )

    if validation_dataset_id:
        eval_dataset = DatasetWrapper(
            data_dir=data_dir,
            dataset_file=validation_ds_filename,
            tokenizer=tokenizer,
            labels=label_list,
            model_type="bert",
            max_seq_length=NERModelParameters.MAX_SEQ_LENGTH,
            mode=Split.dev,
        )

    return train_dataset, eval_dataset, label_list


def _get_label_list(
        data_dir: str,
        train_ds_filename: str
) -> List[str]:
    """
    Get unique labels
    :param data_dir: directory where train and validation datasets are
    :param output_dir: directory where labels file should be saved
    :param train_ds_filename: train dataset filename
    :param validation_ds_filename: validation dataset filename
    :param labels_filename: output labels filename
    :return:
    """
    # Get the unique label list
    unique_labels = set()
    with open(os.path.join(data_dir, train_ds_filename), 'r') as f:
        for line in f:
            if line != "" and line != "\n":
                unique_labels.add(line.split()[-1])
    label_list = list(unique_labels)
    label_list.sort()

    return label_list


def _save_labels(
        data_dir: str,
        output_dir: str,
        labels_filename: str,
        label_list: List[str]
) -> None:
    """
    Save labels to output folder
    :param data_dir: directory where train and validation datasets are
    :param output_dir: directory where labels file should be saved
    :param labels_filename: output labels filename
    :param label_list: unique label list to save
    :return:
    """
    labels_data_path = os.path.join(data_dir, labels_filename)
    labels_output_path = os.path.join(output_dir, labels_filename)
    with open(os.path.join(data_dir, labels_filename), 'w') as f:
        for item in label_list:
            f.write("%s\n" % item)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    copyfile(labels_data_path, labels_output_path)
