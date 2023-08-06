# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding=utf-8
"""Tests for dataset_concat."""

from absl.testing import absltest
from rlds import rlds_types
from rlds.transformations import dataset_concat
from rlds.transformations import transformations_testlib
import tensorflow as tf


class DatasetConcatTest(transformations_testlib.TransformationsTest):

  def setUp(self):
    super().setUp()
    self.steps = {
        rlds_types.OBSERVATION: {
            'field0': [[0, 0], [0, 1], [0, 2]],
            'field1': [[1, 0], [1, 1], [1, 2]]
        },
        rlds_types.ACTION: ([0, 10, 20], [10, 11, 21], [20, 21, 22]),
        rlds_types.REWARD: [0.0, 1.0, 2.0],
        rlds_types.IS_TERMINAL: [False, False, True],
        rlds_types.IS_FIRST: [True, False, False],
    }

  def test_zeros_from_nested_spec(self):
    ds = tf.data.Dataset.from_tensor_slices(self.steps)
    zero_step = dataset_concat.zeros_from_spec(ds.element_spec)
    expected_result = tf.nest.map_structure(tf.zeros_like, next(iter(ds)))
    self.expect_equal_step(zero_step, expected_result)

  def test_zeros_from_batched_step(self):
    ds = tf.data.Dataset.from_tensor_slices(self.steps)
    batched_ds = ds.batch(2)
    zero_step = dataset_concat.zeros_from_spec(batched_ds.element_spec)
    expected_result = tf.nest.map_structure(tf.zeros_like,
                                            next(iter(ds.batch(1))))
    self.expect_equal_step(zero_step, expected_result)

  def test_zeros_dataset_like(self):
    ds = tf.data.Dataset.from_tensor_slices(self.steps)
    zero_ds = dataset_concat.zero_dataset_like(ds)

    num_elements = zero_ds.reduce(0, lambda x, y: x + 1)
    self.assertEqual(num_elements, 1)

    zero_step = tf.data.experimental.get_single_element(zero_ds)
    expected_result = tf.nest.map_structure(tf.zeros_like, next(iter(ds)))

    self.expect_equal_step(zero_step, expected_result)

  def test_concatenate_empty_step(self):
    ds = tf.data.Dataset.from_tensor_slices(self.steps)

    concatenated = dataset_concat.concatenate(
        dataset_concat.zero_dataset_like(ds), ds)

    expected = dataset_concat.zero_dataset_like(ds).concatenate(ds)

    self.expect_equal_datasets(concatenated, expected)

  def test_concatenate_extra_fields(self):
    steps1 = {
        rlds_types.OBSERVATION: [1, 2, 3],
        rlds_types.ACTION: [2, 3, 4],
    }

    steps2 = {
        rlds_types.REWARD: [1., 1., 1.],
        rlds_types.IS_TERMINAL: [False, False, True]
    }

    joined_steps = {
        rlds_types.OBSERVATION: [1, 2, 3, 0, 0, 0],
        rlds_types.ACTION: [2, 3, 4, 0, 0, 0],
        rlds_types.REWARD: [0., 0., 0., 1., 1., 1.],
        rlds_types.IS_TERMINAL: [False, False, False, False, False, True],
    }

    ds1 = tf.data.Dataset.from_tensor_slices(steps1)
    ds2 = tf.data.Dataset.from_tensor_slices(steps2)
    joined = tf.data.Dataset.from_tensor_slices(joined_steps)
    concatenated = dataset_concat.concatenate(ds1, ds2)

    self.expect_equal_datasets(concatenated, joined)

  def test_concatenate_extra_fields_with_intersection(self):
    steps1 = {
        rlds_types.OBSERVATION: [1, 2, 3],
        rlds_types.ACTION: [2, 3, 4],
        'extra_data': [4, 5, 6],
    }

    steps2 = {
        rlds_types.REWARD: [1., 1., 1.],
        rlds_types.IS_TERMINAL: [False, False, True],
        'extra_data': [7, 8, 9],
    }

    joined_steps = {
        rlds_types.OBSERVATION: [1, 2, 3, 0, 0, 0],
        rlds_types.ACTION: [2, 3, 4, 0, 0, 0],
        rlds_types.REWARD: [0., 0., 0., 1., 1., 1.],
        rlds_types.IS_TERMINAL: [False, False, False, False, False, True],
        'extra_data': [4, 5, 6, 7, 8, 9],
    }

    ds1 = tf.data.Dataset.from_tensor_slices(steps1)
    ds2 = tf.data.Dataset.from_tensor_slices(steps2)
    joined = tf.data.Dataset.from_tensor_slices(joined_steps)
    concatenated = dataset_concat.concatenate(ds1, ds2)

    self.expect_equal_datasets(concatenated, joined)

  def test_concat_if_terminal_tfdata(self):
    dataset = tf.data.Dataset.from_tensor_slices(self.steps)

    steps_with_absorbing = dataset_concat.concat_if_terminal(
        dataset,
        dataset_concat.zero_dataset_like(dataset),
        optimization_batch_size=0)

    self.expect_equal_datasets(steps_with_absorbing.take(3), dataset)

    self.expect_equal_datasets(
        steps_with_absorbing.skip(3).take(1),
        dataset_concat.zero_dataset_like(dataset))

  def test_add_concat_if_terminal_batched(self):
    dataset = tf.data.Dataset.from_tensor_slices(self.steps)

    steps_with_absorbing = dataset_concat.concat_if_terminal(
        dataset,
        dataset_concat.zero_dataset_like(dataset))

    self.expect_equal_datasets(steps_with_absorbing.take(3), dataset)

    self.expect_equal_datasets(
        steps_with_absorbing.skip(3).take(1),
        dataset_concat.zero_dataset_like(dataset))


if __name__ == '__main__':
  absltest.main()
