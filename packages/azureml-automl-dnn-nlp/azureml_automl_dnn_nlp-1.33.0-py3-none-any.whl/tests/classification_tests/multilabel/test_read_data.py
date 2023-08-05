import pytest
import unittest
from unittest.mock import MagicMock, patch

from azureml.automl.dnn.nlp.classification.common.constants import DatasetLiterals
from azureml.automl.dnn.nlp.classification.io.read.pytorch_dataset_wrapper import PyTorchDatasetWrapper
from azureml.automl.dnn.nlp.classification.io.read.dataloader import (
    convert_dataset_format,
    get_vectorizer,
    dataset_loader
)
from ...mocks import aml_dataset_mock
try:
    import torch
    has_torch = True
except ImportError:
    has_torch = False


@pytest.mark.usefixtures('MultilabelDatasetTester')
@pytest.mark.parametrize('multiple_text_column', [False])
class TestPyTorchDatasetWrappert:
    @unittest.skipIf(not has_torch, "torch not installed")
    def test_pytorch_dataset_wrapper(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        vectorizer = get_vectorizer(input_df, input_df, label_column_name)
        num_label_cols = len(vectorizer.get_feature_names())
        assert num_label_cols == 6
        training_df = convert_dataset_format(input_df, vectorizer, label_column_name)
        training_df['list'] = training_df[training_df.columns[1:]].values.tolist()
        training_df = training_df[[DatasetLiterals.TEXT_COLUMN, 'list']].copy()
        training_set = PyTorchDatasetWrapper(training_df)
        assert len(training_set) == 5
        assert all(item in ['ids', 'mask', 'token_type_ids', 'targets'] for item in training_set[1])
        assert all(torch.is_tensor(value) for key, value in training_set[1].items())

    @unittest.skipIf(not has_torch, "torch not installed")
    def test_convert_dataset_format(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        pre_conv_col_list = [DatasetLiterals.TEXT_COLUMN, label_column_name]
        assert input_df.columns.to_list() == pre_conv_col_list
        vectorizer = get_vectorizer(input_df, input_df, label_column_name)
        num_label_cols = len(vectorizer.get_feature_names())
        training_df = convert_dataset_format(input_df, vectorizer, label_column_name)
        assert num_label_cols == 6
        post_conv_col_list = [DatasetLiterals.TEXT_COLUMN, 'list']
        assert training_df.columns.to_list() == post_conv_col_list

    @unittest.skipIf(not has_torch, "torch not installed")
    def test_get_vectorizer(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        # Test both cases, with and without validation data
        for valid_df in [input_df, None]:
            vectorizer = get_vectorizer(input_df, valid_df, label_column_name)
            num_label_cols = len(vectorizer.get_feature_names())
            assert num_label_cols == 6
            assert set(vectorizer.get_feature_names()) == set(['A', 'a', '1', '2', 'label5', 'label6'])

    @patch("azureml.core.Dataset.get_by_id")
    def test_dataset_loader(self, get_by_id_mock, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        mock_aml_dataset = aml_dataset_mock(input_df)
        get_by_id_mock.return_value = mock_aml_dataset
        dataset_id = "mock_id"
        validation_dataset_id = "mock_validation_id"
        aml_workspace_mock = MagicMock()
        training_set, validation_set, num_label_cols = dataset_loader(dataset_id, validation_dataset_id,
                                                                      label_column_name, aml_workspace_mock)
        assert num_label_cols == 6
        for output_set in [training_set, validation_set]:
            assert type(output_set) == PyTorchDatasetWrapper
            assert len(output_set) == 5
            assert all(set(output_set[i].keys()) ==
                       set(['ids', 'mask', 'token_type_ids', 'targets']) for i in range(len(output_set)))


@pytest.mark.usefixtures('MultilabelDatasetTester')
@pytest.mark.parametrize('multiple_text_column', [True])
class TestPyTorchDatasetWrapperMultipleColumnst:
    @unittest.skipIf(not has_torch, "torch not installed")
    def test_pytorch_dataset_wrapper(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        vectorizer = get_vectorizer(input_df, input_df, label_column_name)
        num_label_cols = len(vectorizer.get_feature_names())
        assert num_label_cols == 6
        training_df = convert_dataset_format(input_df, vectorizer, label_column_name)
        training_df['list'] = training_df[training_df.columns[1:]].values.tolist()
        training_df = training_df[[DatasetLiterals.TEXT_COLUMN, 'list']].copy()
        training_set = PyTorchDatasetWrapper(training_df)
        assert len(training_set) == 5
        assert all(item in ['ids', 'mask', 'token_type_ids', 'targets'] for item in training_set[1])
        assert all(torch.is_tensor(value) for key, value in training_set[1].items())

    @unittest.skipIf(not has_torch, "torch not installed")
    def test_convert_dataset_format(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        vectorizer = get_vectorizer(input_df, input_df, label_column_name)
        num_label_cols = len(vectorizer.get_feature_names())
        training_df = convert_dataset_format(input_df, vectorizer, label_column_name)
        assert num_label_cols == 6
        post_conv_col_list = [DatasetLiterals.TEXT_COLUMN, 'list']
        assert training_df.columns.to_list() == post_conv_col_list

    @unittest.skipIf(not has_torch, "torch not installed")
    def test_get_vectorizer(self, MultilabelDatasetTester):
        input_df = MultilabelDatasetTester.get_data().copy()
        label_column_name = "labels_col"
        # Test both cases, with and without validation data
        for valid_df in [input_df, None]:
            vectorizer = get_vectorizer(input_df, valid_df, label_column_name)
            num_label_cols = len(vectorizer.get_feature_names())
            assert num_label_cols == 6
            assert set(vectorizer.get_feature_names()) == set(['A', 'a', '1', '2', 'label5', 'label6'])
