from datasets import Dataset
import pytest
import unittest
from unittest.mock import MagicMock, patch
from azureml.automl.dnn.nlp.classification.common.constants import DatasetLiterals, MultiClassParameters
from azureml.automl.dnn.nlp.classification.io.read.dataloader import _concat_text_and_preserve_label, dataset_loader
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchMulticlassDatasetWrapper
from ...mocks import aml_dataset_mock
try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False


@pytest.mark.usefixtures('MulticlassDatasetTester')
class TestTextClassificationDataLoadTests:
    """Tests for Text Classification data loader."""
    @pytest.mark.parametrize('multiple_text_column', [False])
    @pytest.mark.parametrize('include_label_col', [True, False])
    def test_concat_text_and_preserve_label(self, MulticlassDatasetTester, include_label_col):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        if include_label_col:
            # One text column, along with label column (training scenario)
            assert input_df.shape == (5, 2)
            output_df = _concat_text_and_preserve_label(input_df, label_column_name)
            assert output_df.shape == (5, 2)
            assert set(output_df.columns) == set([label_column_name, DatasetLiterals.TEXT_COLUMN])
        else:
            # One text column, no label column (inference scenario)
            assert input_df.shape == (5, 1)
            output_df = _concat_text_and_preserve_label(input_df, label_column_name)
            assert output_df.shape == (5, 1)
            assert set(output_df.columns) == set([DatasetLiterals.TEXT_COLUMN])

    @pytest.mark.parametrize('multiple_text_column', [True])
    @pytest.mark.parametrize('include_label_col', [True, False])
    def test_concat_text_and_preserve_label_multiple_text_cols(self, MulticlassDatasetTester, include_label_col):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        if include_label_col:
            # Two text columns, along with label column (training scenario)
            assert input_df.shape == (5, 3)
            output_df = _concat_text_and_preserve_label(input_df, label_column_name)
            assert output_df.shape == (5, 2)
            assert set(output_df.columns) == set([label_column_name, DatasetLiterals.TEXT_COLUMN])
        else:
            # Two text columns, no label column (inference scenario)
            assert input_df.shape == (5, 2)
            output_df = _concat_text_and_preserve_label(input_df, label_column_name)
            assert output_df.shape == (5, 1)
            assert set(output_df.columns) == set([DatasetLiterals.TEXT_COLUMN])

    @unittest.skipIf(not has_torch, "torch not installed")
    @pytest.mark.parametrize('multiple_text_column', [False])
    @pytest.mark.parametrize('include_label_col', [True])
    def test_pytorch_multiclass_dataset_wrapper(self, MulticlassDatasetTester):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        assert input_df.shape == (5, 2)
        output_dataset = Dataset.from_pandas(_concat_text_and_preserve_label(input_df, label_column_name))
        assert type(output_dataset) == Dataset
        label_list = output_dataset.unique(label_column_name)
        output_set = PyTorchMulticlassDatasetWrapper(output_dataset, label_list, label_column_name)
        assert type(output_set) == PyTorchMulticlassDatasetWrapper
        assert set(output_dataset.column_names) == set([label_column_name, DatasetLiterals.TEXT_COLUMN])
        assert len(output_set) == 5
        assert all(output_set_curr.keys() == set([DatasetLiterals.LABEL_COLUMN,
                                                  DatasetLiterals.INPUT_IDS,
                                                  DatasetLiterals.TOKEN_TYPE_IDS,
                                                  DatasetLiterals.ATTENTION_MASK]) for output_set_curr in output_set)
        for output_set_curr in output_set:
            for key_name in output_set_curr.keys():
                assert type(output_set_curr[key_name]) == torch.Tensor
                if key_name != DatasetLiterals.LABEL_COLUMN:
                    assert len(output_set_curr[key_name]) == MultiClassParameters.MAX_SEQ_LENGTH

    @pytest.mark.parametrize('multiple_text_column', [True, False])
    @pytest.mark.parametrize('include_label_col', [True])
    @patch("azureml.core.Dataset.get_by_id")
    def test_dataset_loader(self, get_by_id_mock, MulticlassDatasetTester):
        input_df = MulticlassDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        mock_aml_dataset = aml_dataset_mock(input_df)
        get_by_id_mock.return_value = mock_aml_dataset
        dataset_id = "mock_id"
        validation_dataset_id = "mock_validation_id"
        aml_workspace_mock = MagicMock()
        training_set, validation_set, label_list = dataset_loader(dataset_id, validation_dataset_id,
                                                                  label_column_name, aml_workspace_mock,
                                                                  is_multiclass_training=True)
        # The returned label_list is sorted, although the original labels weren't
        assert label_list != input_df[label_column_name].unique().tolist()
        assert label_list == sorted(input_df[label_column_name].unique())
        for output_set in [training_set, validation_set]:
            assert type(output_set) == PyTorchMulticlassDatasetWrapper
            assert len(output_set) == 5
            assert all(output_set_curr.keys() ==
                       set([DatasetLiterals.LABEL_COLUMN, DatasetLiterals.INPUT_IDS, DatasetLiterals.TOKEN_TYPE_IDS,
                            DatasetLiterals.ATTENTION_MASK]) for output_set_curr in output_set)
