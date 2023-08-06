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
"""Utils to normalize a field in an RLDS dataset."""

from typing import Any, Callable, Dict, Tuple

import numpy as np
from rlds import rlds_types
from rlds.transformations import dataset_concat
from rlds.transformations import flexible_batch
from rlds.transformations import nested_ops
import tensorflow as tf


# TODO(sabela): optimize by removing the need to use ifs and for loops.
def _map_single_step_to_data(step, get_fields):
  """Maps a step into count and data using the result of get_fields."""
  fields, mask = get_fields(step)
  mapped_step = {
      'count': dict(),
      'data': dict()
  }
  for k in fields:
    if mask[k]:
      mapped_step['data'][k] = fields[k]
      mapped_step['count'][k] = 1
    else:
      mapped_step['data'][k] = tf.nest.map_structure(tf.zeros_like, fields[k])
      mapped_step['count'][k] = 0
  return mapped_step


# TODO(sabela): optimize by removing the need to use ifs and for loops.
def _map_single_step_for_std(step, mean):
  """Maps a step into (data-mean)**2."""
  result = dict()
  for k in step['data']:
    if step['count'][k] != 0:
      result[k] = tf.nest.map_structure(
          lambda x, y: abs(tf.cast(x, tf.float64) - y)**2, step['data'][k],
          mean[k])
    else:
      # Here, step['data'][k] is expected to contain zeros, so we only cast it
      # to float64 so it has the same type as above.
      result[k] = tf.nest.map_structure(lambda x: tf.cast(x, tf.float64),
                                        step['data'][k])
  return result


def mean_and_std(
    episodes_dataset: tf.data.Dataset,
    get_step_fields: Callable[[rlds_types.Step], Tuple[Dict[str, Any],
                                                       Dict[str, bool]]],
    optimization_batch_size=flexible_batch.DEFAULT_BATCH) -> Tuple[Any, Any]:
  """Calculates the mean and std of a set of fields accross the dataset.

  Args:
    episodes_dataset: dataset of episodes.
    get_step_fields: function applied to each step and returns a dictionary with
      the data for which we will calculate the stats, as well as a set with the
      keys of the fields that have valid data in this step. These fields are
      expected to have a numeric type.
    optimization_batch_size: if >1, each episode will be batched into a single
      batch and loaded in memory. The batch size must be an upper bound of the
      episode length. It fails otherwise.

  Returns:
    Tuple with the mean and std as float64. It maintains the same shape and
    dtype of the output of `get_step_fields`.
  """
  data_for_mean = nested_ops.map_nested_steps(
      episodes_dataset,
      lambda step: _map_single_step_to_data(step, get_step_fields))
  # We fetch the first element of the dataset in order to get the shape of
  # the nested dataset
  data_for_mean_episode = next(iter(data_for_mean))
  zero_field = dataset_concat.zeros_from_spec(
      data_for_mean_episode[rlds_types.STEPS].element_spec)
  result = nested_ops.sum_nested_steps(data_for_mean, zero_field,
                                       optimization_batch_size)
  result = tf.nest.map_structure(lambda x: tf.cast(x, tf.float64), result)
  mean = dict()
  for k in result['count']:
    count = result['count'][k]

    mean[k] = tf.nest.map_structure(lambda x: x/count, result['data'][k])


  data_for_std = nested_ops.map_nested_steps(
      data_for_mean, lambda step: _map_single_step_for_std(step, mean))
  result_for_std = nested_ops.sum_nested_steps(
      data_for_std,
      tf.nest.map_structure(lambda x: tf.cast(x, tf.float64),
                            zero_field['data']), optimization_batch_size)

  std = dict()
  for k in result['count']:
    std[k] = tf.nest.map_structure(
        lambda x: np.sqrt(x / (result['count'][k] - 1)), result_for_std[k])
  return mean, std
