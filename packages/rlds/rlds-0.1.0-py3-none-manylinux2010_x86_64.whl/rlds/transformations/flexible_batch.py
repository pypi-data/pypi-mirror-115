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
"""Library functions for flexible batching."""

from typing import Any, Dict, Optional, Tuple, Union

from rlds import rlds_types
import tensorflow as tf

# DEFAULT_BATCH is defined to a large number so most datasets will be batched
# into a single element when using this as a batch size.
DEFAULT_BATCH = 1000000000


def _windowed_to_batched_dataset(
    nested_dataset: Union[Dict[str, Any], Tuple[Any], tf.data.Dataset],
    batch_size: int) -> Union[Dict[str, Any], Tuple[Any], Any]:
  """Converts a nested windowed dataset into a batch.

  Args:
    nested_dataset: nested dataset that has been generated with a window
      transformation.
    batch_size: desired batch size (it has to correspond to the size used for
      the window transformation).

  Returns:
    Batch that respects the nested structure of the given dataset.

  """
  return tf.nest.map_structure(
      lambda ds: tf.data.experimental.get_single_element(
          ds.batch(batch_size)),
      nested_dataset)


def batch(dataset: tf.data.Dataset,
          size: int,
          shift: Optional[int] = None,
          stride: int = 1,
          drop_remainder: bool = False) -> tf.data.Dataset:
  """Batches dataset elements using tf.data.Dataset window interface.

  It is equivalent to tf.data.Dataset.window but flattens the nested datasets.

  Args:
    dataset: dataset to be batched.
    size: number of elements per batch.
    shift: increment to compute the index to start the next batch (shift=1 means
      that we create a batch for each element in the input dataset). Must be
      positive.
    stride: increment to compute the index to select the next element of each
      batch (stride=1 means that we include consecutive elements in the batch).
      Must be positive.
    drop_remainder: whether the last batches should be dropped if their size is
      smaller than size.

  Returns:
    A dataset where each element has been batched according to the
    configuration parameters.

  Examples:

  If dataset ds contains (1, 2, 3, 4):

   * batch(ds, size=2, shift=1, stride=1, False)->([1, 2], [2, 3], [3, 4], [4])
   * batch(ds, size=2, shift=1, stride=1, True) -> ([1, 2], [2, 3], [3, 4])
   * batch(ds, size=2, shift=2, stride=1, False)->([1, 2], [3, 4])
   * batch(ds, size=2, shift=1, stride=2, False)->([1, 3], [2, 4], [3], [4])

  """
  if not shift and stride == 1:
    return dataset.batch(batch_size=size, drop_remainder=drop_remainder)
  windowed = dataset.window(
      size=size, shift=shift, stride=stride, drop_remainder=drop_remainder)
  return windowed.map(
      lambda windowed_ds: _windowed_to_batched_dataset(windowed_ds, size))


def batch_episode(episode: rlds_types.Episode,
                  size: int = DEFAULT_BATCH,
                  shift: Optional[int] = None,
                  stride: int = 1,
                  drop_remainder: bool = False) -> Dict[str, Any]:
  """Batches the steps of an episode.

  Args:
    episode: The episode whose steps will be batched.
    size: Size of the batch. By default we use a large batch size so many
      episodes will have only one batch element.
    shift: increment to compute the index to start the next batch (shift=1 means
      that we create a batch for each element in the input dataset). Must be
      positive.
    stride: increment to compute the index to select the next element of each
      batch (stride=1 means that we include consecutive elements in the batch).
      Must be positive.
    drop_remainder: whether the last batches should be dropped if their size is
      smaller than size.

  Returns:
    An episode with the steps batched.
  """
  episode[rlds_types.STEPS] = batch(
      episode[rlds_types.STEPS],
      size=size,
      shift=shift,
      stride=stride,
      drop_remainder=drop_remainder)
  return episode


def unbatch_episode(episode: rlds_types.BatchedEpisode) -> rlds_types.Episode:
  """Reverts the batching of the steps of an episode.

  Note that if there was not batching applied in the first place, it will just
  remove the first dimension of the steps (if possible).

  It will not un-do the effects of shift/stride applied when batching.

  Args:
    episode: The episode whose steps have to be unbatched.

  Returns:
    An episode with the steps un-batched.
  """
  episode[rlds_types.STEPS] = episode[rlds_types.STEPS].unbatch()
  return episode
