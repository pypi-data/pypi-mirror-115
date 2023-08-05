# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
#
# For PyTorchDatasetWrapper:
#
# MIT License
#
# Copyright (c) 2020 Abhishek Kumar Mishra
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""PyTorchDatasetWrapper class for text tasks"""

from datasets import Dataset as HfDataset
import logging
import torch
from torch.utils.data import Dataset as PyTorchDataset
from transformers import BertTokenizer, AutoTokenizer
from typing import Any, List, Union

from azureml.automl.dnn.nlp.classification.common.constants import (
    DatasetLiterals,
    ModelNames,
    MultiClassParameters,
    MultiLabelParameters
)
from azureml.automl.dnn.nlp.classification.multiclass.utils import preprocess_function

logger = logging.getLogger(__name__)


class PyTorchDatasetWrapper(PyTorchDataset):
    """Class for obtaining dataset to be passed into model."""

    def __init__(self, dataframe):
        """Init function definition."""
        self.tokenizer = BertTokenizer.from_pretrained(ModelNames.BERT_BASE_UNCASED)
        self.data = dataframe
        self.comment_text = dataframe.text
        self.targets = self.data.list
        self.max_len = MultiLabelParameters.MAX_LEN

    def __len__(self):
        """Len function definition."""
        return len(self.comment_text)

    def __getitem__(self, index):
        """Getitem function definition."""
        comment_text = str(self.comment_text[index])
        comment_text = " ".join(comment_text.split())

        inputs = self.tokenizer.encode_plus(
            comment_text,
            None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            return_token_type_ids=True,
            truncation=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs["token_type_ids"]

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long),
            'targets': torch.tensor(self.targets[index], dtype=torch.float)
        }


class PyTorchMulticlassDatasetWrapper(PyTorchDataset):
    """
    Class for obtaining dataset to be passed into model for multi-class classification.
    This is based on the datasets.Dataset package from HuggingFace.
    """

    def __init__(self, hf_dataset: HfDataset, label_list: List[Any],
                 label_column_name: Union[str, None] = None,
                 infer_data: bool = False):
        """Init function definition."""
        self.label_to_id = {v: i for i, v in enumerate(label_list)}
        self.tokenizer = AutoTokenizer.from_pretrained(ModelNames.BERT_BASE_CASED, use_fast=True)

        # Padding strategy
        pad_to_max_length = MultiClassParameters.PAD_TO_MAX_LENGTH
        if pad_to_max_length:
            self.padding = MultiClassParameters.MAX_LEN_PADDING
        else:
            self.padding = False

        self.max_seq_length = MultiClassParameters.MAX_SEQ_LENGTH
        if self.max_seq_length > self.tokenizer.model_max_length:
            logger.warn(
                f"The max_seq_length passed ({self.max_seq_length}) is larger than the maximum length for the"
                f"model ({self.tokenizer.model_max_length}). Using max_seq_length={self.tokenizer.model_max_length}."
            )
        self.max_seq_length = min(self.max_seq_length, self.tokenizer.model_max_length)
        # To be used for pre-processing the data
        self.fn_kwargs = {'tokenizer': self.tokenizer, 'padding': self.padding,
                          'max_seq_length': self.max_seq_length, 'label_to_id': self.label_to_id,
                          'label_column_name': label_column_name}
        self.data = hf_dataset.map(preprocess_function, batched=True, fn_kwargs=self.fn_kwargs)

        column_names = [DatasetLiterals.INPUT_IDS, DatasetLiterals.TOKEN_TYPE_IDS, DatasetLiterals.ATTENTION_MASK]
        if not infer_data:
            column_names.append(DatasetLiterals.LABEL_COLUMN)
        #  Setting PyTorch format for datasets.Dataset object to wrap it in a torch.utils.data.DataLoader
        self.data.set_format(type='torch', columns=column_names)

    def __len__(self):
        """Len function definition."""
        return len(self.data)

    def __getitem__(self, index):
        """Getitem function definition."""
        return self.data[index]
