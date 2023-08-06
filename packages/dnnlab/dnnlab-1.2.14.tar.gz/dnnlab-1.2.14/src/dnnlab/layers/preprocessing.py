# Copyright 2020 Tobias Höfer
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
# =============================================================================
"""A Preprocessor packages (on-device) the input pipeline specific preprocessing.
The key benefit to appending a Preprocessor Layer to a model is that it makes
your model portable. When all data preprocessing is part of the model, other
people can load and use your model without having to be aware of how each
feature is expected to be encoded & normalized. Your inference model will be
able to process raw images or raw structured data, and will not require users of
the model to be aware of the details of e.g. the tokenization scheme used for
text, the indexing scheme used for categorical features, whether image pixel
values are normalized to [-1, +1] or to [0, 1], etc. This is especially powerful
if you're exporting your model to another runtime, such as TensorFlow.js: you
won't have to reimplement your preprocessing pipeline in JavaScript.

If you initially put your preprocessing layers in your tf.data pipeline, you can
export an inference model that packages the preprocessing. Simply instantiate
a new model that chains your preprocessing layers and your training model.

Crucially, these layers are non-trainable. Their state is not set during
training; it must be set before training, a step called "adaptation".
"""
import tensorflow as tf
from tensorflow.keras.layers.experimental import preprocessing


class Preprocessor(tf.keras.layers.Layer):
    """Packages the input specific image preprocessing. Used in conjunction with
    a Model to make it portable to other runtimes and make it on-device.
    With Keras preprocessing layers, you can build and export models that are
    truly end-to-end: models that accept raw images or raw structured data as
    input; models that handle feature normalization or feature value indexing on
    their own."""
    def __init__(self, size, scale=1. / 127.5, offset=-1):
        """ Defaults to bilinear resizing and [-1, 1] scale."""
        super(Preprocessor, self).__init__()
        self.size = size
        self.scale = scale
        self.offset = offset

    def call(self, input):
        x = preprocessing.Resizing(self.size)(input)
        x = preprocessing.Rescaling(self.scale, self.offset)
        return x
