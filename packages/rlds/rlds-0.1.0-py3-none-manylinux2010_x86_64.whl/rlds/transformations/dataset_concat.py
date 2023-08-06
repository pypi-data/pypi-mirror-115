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
"""Library functions for concatenation of two datasets."""

from typing import Any, Mapping, Tuple

from rlds import rlds_types
from rlds.transformations import flexible_batch
from rlds.transformations import nested_ops
import tensorflow as tf


def _zeros_shape(element_shape: tf.TensorShape) -> Tuple[Any, ...]:
  if not element_shape:
    return ()
  return tuple([1 if dim is None else dim for dim in element_shape])


def zeros_from_spec(spec: tf.TensorSpec) -> rlds_types.Step:
  """Builds a tensor of zeros with the given spec.

  If the spec has been obtained from a batch of steps where the first
  dimension is `None`, it will create a zero step with a batch dimension of 1.

  Args:
    spec: TensorSpec that specifies the shape and types of the output.

  Returns:
    tensor with `spec` as TensorSpec, and with all the fields initialized to
    zeros.
  """
  return tf.nest.map_structure(
      lambda t: tf.zeros(_zeros_shape(t.shape), t.dtype), spec)


def zero_dataset_like(ds: tf.data.Dataset) -> tf.data.Dataset:
  """Creates a one element dataset with the spec of ds containing zeros.

  Args:
    ds: Dataset of steps.

  Returns:
    Dataset of one element that has the same `element_spec` as `ds`.
  """
  return tf.data.Dataset.from_tensors(zeros_from_spec(ds.element_spec))


def _add_empty_values(step: rlds_types.Step,
                      spec: Mapping[str, tf.TensorSpec]) -> rlds_types.Step:
  """Adds zero elements to step for the keys in spec not present in step.

  Args:
    step: Dictionary representing a Step.
    spec: Tensor spec.

  Returns:
    Dictionary containing all the k:v paris from step, and k:zeros for those
    elements in the spec that are not yet part of step.
  """
  for k in spec:
    if k not in step:
      step[k] = zeros_from_spec(spec[k])
  return step


def concatenate(steps1: tf.data.Dataset,
                steps2: tf.data.Dataset) -> tf.data.Dataset:
  """Concatenates the two datasets.

  If one of the datasets contains fields that are not present in the other
  dataset, those fields are added to the other dataset initialized to zeros.

  It assumest that the elements in the datasets are dictionaries.

  Args:
    steps1: First dataset.
    steps2: Second dataset.

  Returns:
    Dataset of steps1 and steps2.
  """

  spec_step1 = steps1.element_spec
  spec_step2 = steps2.element_spec
  steps1 = steps1.map(lambda step: _add_empty_values(step, spec_step2))
  steps2 = steps2.map(lambda step: _add_empty_values(step, spec_step1))
  return steps1.concatenate(steps2)


def concat_if_terminal(
    steps: tf.data.Dataset,
    extra_steps_ds: tf.data.Dataset,
    optimization_batch_size: int = flexible_batch.DEFAULT_BATCH
) -> tf.data.Dataset:
  """Concats the datasets if the steps end in terminal and applies a map.

  Provides the skeleton to add absorbing states to an episode.

  Args:
    steps: dataset of steps. Each step is expected to contain `IS_TERMINAL`.
    extra_steps_ds: dataset of step(s) containing an absorbing state and that
      will be added at the end of the dataset of steps if it ends in
      `IS_TERMINAL = True`.
    optimization_batch_size: if >1, each episode will be batched into a single
      batch and loaded in memory. The batch size must be an upper bound of the
      episode length. It fails otherwise.

  Returns:
    An dataset with the extra steps only if the original dataset ends in a
    terminal state and the origianl steps are transformed by `map_step_fn`.
  """
  ends_in_terminal = nested_ops.check_final_step(
      steps,
      lambda step: step[rlds_types.IS_TERMINAL],
      optimization_batch_size=optimization_batch_size)
  if ends_in_terminal:
    steps = concatenate(steps, extra_steps_ds)
  else:
    # We concatenate with he empty dataset because otherwise the type of the
    # dataset is different in the if/else branches.
    steps = concatenate(steps, steps.take(0))
  return steps
