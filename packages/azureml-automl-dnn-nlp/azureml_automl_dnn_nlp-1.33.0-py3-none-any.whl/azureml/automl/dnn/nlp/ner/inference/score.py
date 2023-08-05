# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Scoring functions that can load a serialized model and predict."""

import logging
import os
import time
from typing import Tuple

from transformers import (
    AutoConfig,
    AutoModelForTokenClassification,
    AutoTokenizer,
    Trainer,
)

from azureml.automl.dnn.nlp.common.constants import NERModelParameters, OutputLiterals
from azureml.automl.dnn.nlp.common.data_utils import download_file_dataset
from azureml.automl.dnn.nlp.common.utils import get_run_by_id
from azureml.automl.dnn.nlp.ner.ner_tasks import write_predictions_to_file
from azureml.automl.dnn.nlp.ner.io.read.dataset_wrapper import DatasetWrapper
from azureml.automl.dnn.nlp.ner.token_classification_metrics import TokenClassificationMetrics
from azureml.automl.dnn.nlp.ner.utils import get_labels, Split
from azureml.core.run import Run

logger = logging.getLogger(__name__)


def _download_file(
        run: Run,
        log_friendly_file_name,
        path,
        file_name
) -> None:
    logger.info("Start downloading {} artifact".format(log_friendly_file_name))
    run.download_file(os.path.join(path, file_name), output_file_path=file_name)
    logger.info("Finished downloading CONFIG artifact")


def _load_training_artifacts(
        run: Run,
        artifacts_dir: str
) -> Tuple[AutoModelForTokenClassification, AutoTokenizer, AutoConfig]:
    """Load the training artifacts.

    :param run: run context of the run that produced the model
    :param artifacts_dir: artifacts directory
    :return: returns the model, tokenizer and config from the model's training
    """
    logger.info("Start fetching model from artifacts")

    _download_file(run, "CONFIG", artifacts_dir, OutputLiterals.CONFIG_FILE_NAME)
    _download_file(run, "MODEL", artifacts_dir, OutputLiterals.NER_MODEL_FILE_NAME)
    _download_file(run, "TRAINING_ARGS", artifacts_dir, OutputLiterals.TRAINING_ARGS)
    _download_file(run, "LABELS", artifacts_dir, OutputLiterals.LABELS_FILE)

    config = AutoConfig.from_pretrained(OutputLiterals.CONFIG_FILE_NAME)
    # TODO: use tokenizer config
    tokenizer = AutoTokenizer.from_pretrained(NERModelParameters.MODEL_NAME)
    model = AutoModelForTokenClassification.from_pretrained(OutputLiterals.NER_MODEL_FILE_NAME, config=config)

    logger.info("Training artifacts restored successfully")
    return model, tokenizer, config


def score(
        run_id: str,
        input_dataset_id: str,
        data_dir: str,
        output_dir: str,
        batch_size: int = 8
) -> None:
    """
    Generate predictions from input files.

    :param run_id: azureml run id
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :param data_dir: path to data file
    :param output_dir: path to output file
    :param batch_size: batch size for prediction
    """
    logger.info("Starting inference for run {} batch_size: {}".format(run_id, batch_size))

    logger.info("Get run context")
    run = get_run_by_id(run_id)
    model, tokenizer, config = _load_training_artifacts(run, output_dir)

    # Get Test Dataset object
    logger.info("Load file dataset")
    test_file = download_file_dataset(input_dataset_id, "Test Dataset", run.experiment.workspace, data_dir)

    # Init for NER task class, labels and metrics
    logger.info("Initialize Trainer")
    labels = get_labels(OutputLiterals.LABELS_FILE)
    token_classification_metrics = TokenClassificationMetrics(labels)
    # from HF code - modified
    trainer = Trainer(
        model=model,
        # TODO: unable to use training_args on 'cpu' device
        # args=training_args,
        compute_metrics=token_classification_metrics.compute_metrics
    )

    test_dataset = DatasetWrapper(
        data_dir=data_dir,
        dataset_file=test_file,
        tokenizer=tokenizer,
        labels=labels,
        model_type=config.model_type,
        max_seq_length=128,
        mode=Split.test,
    )

    logger.info("Run prediction")
    st = time.time()
    predictions, label_ids, metrics = trainer.predict(test_dataset)
    time_diff = time.time() - st
    metrics['infer_time'] = time_diff
    preds_list, _, preds_proba_list = token_classification_metrics.align_predictions_with_proba(predictions,
                                                                                                label_ids)

    # Save predictions
    logger.info("Save predictions")
    if trainer.is_world_process_zero():
        os.makedirs(output_dir, exist_ok=True)
        output_test_results_file = os.path.join(output_dir, "test_results.txt")
        with open(output_test_results_file, "w") as writer:
            for key, value in metrics.items():
                logger.info("  {} = {}".format(key, value))
                writer.write("{} = {}\n".format(key, value))
            logger.info("Test results saved at location: {}".format(output_test_results_file))
        output_test_predictions_file = os.path.join(output_dir, "test_predictions.txt")
        with open(output_test_predictions_file, "w") as writer:
            with open(os.path.join(data_dir, test_file), "r") as f:
                write_predictions_to_file(writer, f, preds_list, preds_proba_list)
                logger.info("Test predictions saved at location: {}".format(output_test_predictions_file))

    return
