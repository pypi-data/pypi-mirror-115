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
"""Module with utils to manipulate nested datasets."""

from typing import Any, Callable, Dict

from rlds import rlds_types
from rlds.transformations import batched_helpers
from rlds.transformations import flexible_batch
import tensorflow as tf


def _get_episode_metadata(episode: rlds_types.Episode) -> Dict[str, Any]:
  return {k: episode[k] for k in episode if k != rlds_types.STEPS}


def _map_episode(
    episode: rlds_types.Episode,
    transform_step: Callable[[rlds_types.Step], Any],
    in_place: bool) -> rlds_types.Episode:
  """Applies a transformation to all the steps of an episode.

  Args:
    episode: single episode.
    transform_step: Function that takes one step and applies a transformation.
      The return type is not necessarily a step.
    in_place: Whether the operation is done in place on the original episode.

  Returns:
    An episodes where all the steps are transformed according to the
    transformation function and stored in the given episode_key.
  """
  steps = episode[rlds_types.STEPS].map(transform_step)
  if in_place:
    episode[rlds_types.STEPS] = steps
    return episode
  else:
    return rlds_types.build_episode(steps=steps,
                                    metadata=_get_episode_metadata(episode))


def map_nested_steps(
    episodes_dataset: tf.data.Dataset,
    transform_step: Callable[[rlds_types.Step], Any]) -> tf.data.Dataset:
  """Applies a transformation to all the steps of a dataset.

  Args:
    episodes_dataset: Dataset of episodes.
    transform_step: Function that takes one step and applies a transformation.
      The return type is not necessarily a step.

  Returns:
    A dataset of episodes where all the steps are transformed according to the
    transformation function.
  """
  # Note that doing the operation in place does not modify the input dataset.
  return episodes_dataset.map(
      lambda e: _map_episode(e, transform_step, in_place=True))


def _apply_episode(
    episode: rlds_types.Episode,
    transform_step_dataset: Callable[[tf.data.Dataset], Any],
    in_place: bool) -> rlds_types.Episode:
  """Applies a transformation to the steps dataset of an episode.


  Args:
    episode: single episode.
    transform_step_dataset: Function that takes a dataset of steps and applies
      a transformation.
    in_place: Whether the operation is done in place on the original episode.

  Returns:
    An episode where the dataset of steps is transformed according to the
    transformation function.
  """
  steps = episode[rlds_types.STEPS].apply(transform_step_dataset)
  if in_place:
    episode[rlds_types.STEPS] = steps
    return episode
  else:
    return rlds_types.build_episode(steps=steps,
                                    metadata=_get_episode_metadata(episode))


def apply_nested_steps(
    episodes_dataset: tf.data.Dataset,
    transform_step_dataset: Callable[[tf.data.Dataset], Any]
    ) -> tf.data.Dataset:
  """Applies for each episode a transformation on the dataset of steps.

  Args:
    episodes_dataset: Dataset of episodes.
    transform_step_dataset: A function that takes a dataset of steps and applies
      a transformation.

  Returns:
    A dataset of episodes where all the nested dataset of steps are transformed
    according to the transformation function.
  """
  return episodes_dataset.map(
      lambda e: _apply_episode(e, transform_step_dataset, in_place=True))


def _sum_episode(initial_value: Any, steps: tf.data.Dataset) -> Any:
  """Accumulates all the steps of an episode.

  Args:
    initial_value: initial value for the accumulation.
    steps: steps dataset.

  Returns:
    Result of accumulating all of the steps. It has the same shape and dtype as
    `initial_value`.
  """

  return steps.reduce(
      initial_value, lambda initial_value, step: tf.nest.map_structure(
          tf.add, initial_value, step))



def _sum_episode_batched(initial_value, steps, batch_size):
  """Accumulates all the steps of an episode using a batch optimization.

  It assumes that the full episode fits in memory and that batch_size is larger
  (or equal) than the episode length.

  Args:
    initial_value: initial value for the accumulation.
    steps: dataset of steps.
    batch_size: size to batch the episode. It has to be larger (or equal) than
      the episode length.

  Returns:
    Result of accumulating all of the steps. It has the same shape and dtype as
    `initial_value`.
  """

  def _accumulate_batched_data(batched_episode):
    return tf.nest.map_structure(lambda x: tf.reduce_sum(x, axis=0),
                                 batched_episode)

  total_sum = batched_helpers.batched_reduce_full_dataset(
      steps, _accumulate_batched_data, batch_size)

  return tf.nest.map_structure(tf.math.add, initial_value, total_sum)


def sum_nested_steps(
    episodes_dataset: tf.data.Dataset,
    initial_value: Any,
    optimization_batch_size: int = flexible_batch.DEFAULT_BATCH) -> Any:
  """Accumulates the values of all steps in a dataset of episodes.

  It expects all fields in the steps to have dtypes that support `tf.add`.

  Args:
    episodes_dataset: dataset of episodes. Each of them contains a nested
      dataset with the key `rlds_types.STEPS`. The nested dataset contains
      fields that can be aggregated.
    initial_value: value with the same shape and dtype of a step that will be
      used as initial value for the aggregation.
    optimization_batch_size:  if >1, each episode will be batched into a single
      batch and loaded in memory. The batch size must be an upper bound of the
      episode length (for any episode in the dataset). It fails otherwise.

  Returns:
    Aggregation of all the values of the steps. It has the same shape and dtype
    as the `initial_value`.

  """

  if optimization_batch_size <= 1:
    # use a pure tf.data pipeline
    return episodes_dataset.reduce(
        initial_value,
        lambda accum, e: _sum_episode(accum, e[rlds_types.STEPS]))
  else:
    # reduce episodes with batched pipelines
    return episodes_dataset.reduce(
        initial_value, lambda accumulated, episode: _sum_episode_batched(
            accumulated, episode[rlds_types.STEPS], optimization_batch_size))



def sum_dataset(
    steps_dataset: tf.data.Dataset,
    initial_value: Any,
    optimization_batch_size: int = flexible_batch.DEFAULT_BATCH) -> Any:
  """Accumulates the values of all steps in a dataset.

  It expects all fields in the steps to have dtypes that support `tf.add`.

  Args:
    steps_dataset: dataset of steps. Each of the steps is a dictionary
    initial_value: value with the same shape and dtype of a step that will be
      used as initial value for the aggregation.
    optimization_batch_size:  if >1, each episode will be batched into a single
      batch and loaded in memory. The batch size must be an upper bound of the
      episode length. It fails otherwise.

  Returns:
    Aggregation of all the values of the steps. It has the same shape and dtype
    as the `initial_value`.

  """

  if optimization_batch_size <= 1:
    # use a pure tf.data pipeline
    return steps_dataset.reduce(
        initial_value, lambda initial_value, step: tf.nest.map_structure(
            tf.add, initial_value, step))
  else:
    # reduce episodes with batched pipelines
    return _sum_episode_batched(initial_value, steps_dataset,
                                optimization_batch_size)



def _check_final_step_batched(steps, condition, batch_size):
  """Checks if the final step fullfills the given condition.

  It assumes that the full episode fits in memory and that batch_size is larger
  (or equal) than the episode length.

  Args:
    steps: dataset of steps.
    condition: condition to apply to the final item of the dataset.
    batch_size: size to batch the episode. It has to be larger (or equal) than
      the episode length.

  Returns:
     True if the last step fullfills the condition, False otherwise.
  """

  def _apply_condition(batched_episode):
    last_step = tf.nest.map_structure(lambda x: x[-1], batched_episode)
    return condition(last_step)

  total_sum = batched_helpers.batched_reduce_full_dataset(
      steps, _apply_condition, batch_size)

  return total_sum


def check_final_step(
    steps_dataset: tf.data.Dataset,
    condition: Callable[[rlds_types.Step], bool],
    optimization_batch_size: int = flexible_batch.DEFAULT_BATCH) -> Any:
  """Checks if the final step fullfills the given condition.

  Args:
    steps_dataset: dataset of steps. Each of the steps is a dictionary
    condition: condition to apply to the final item of the dataset.
    optimization_batch_size:  if >1, each episode will be batched into a single
      batch and loaded in memory.The batch size must be an upper bound of the
      episode length. It fails otherwise.

  Returns:
    True if the last step fullfills the condition, False otherwise.
  """

  if optimization_batch_size <= 1:
    # use a pure tf.data pipeline
    return steps_dataset.reduce(False,
                                lambda initial_value, step: condition(step))
  else:
    # reduce episodes with batched pipelines
    return _check_final_step_batched(steps_dataset, condition,
                                     optimization_batch_size)



def episode_length(
    steps_dataset: tf.data.Dataset,
    optimization_batch_size: int = flexible_batch.DEFAULT_BATCH) -> int:
  """Obtains the episode length.

  Args:
    steps_dataset: dataset of steps.
    optimization_batch_size:  if >1, each episode will be batched into a single
      batch and loaded in memory. The batch size must be an upper bound of the
      episode length. It fails otherwise.

  Returns:
    Number of steps in an episode.
  """

  if optimization_batch_size <= 1:
    return steps_dataset.reduce(0, lambda count, step: count + 1)

  def _episode_length(batched_data):
    return tf.shape(tf.nest.flatten(batched_data)[0])[0]

  return batched_helpers.batched_reduce_full_dataset(steps_dataset,
                                                     _episode_length,
                                                     optimization_batch_size)
