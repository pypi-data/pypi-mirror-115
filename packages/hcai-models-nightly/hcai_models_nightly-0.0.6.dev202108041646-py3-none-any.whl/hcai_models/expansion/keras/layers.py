import tensorflow as tf
from tensorflow.python.util.tf_export import keras_export
from tensorflow.python.keras.engine import base_preprocessing_layer
from tensorflow.python.keras.engine.base_preprocessing_layer import PreprocessingLayer
from tensorflow.python.keras.engine.input_spec import InputSpec
from tensorflow.python.framework import tensor_shape
from tensorflow.python.keras.layers.preprocessing.image_preprocessing import (
    get_interpolation,
)
from tensorflow.python.framework import ops
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import image_ops
#from keras.preprocessing.image import smart_resize
import numpy as np

@keras_export("keras.layers.experimental.preprocessing.SmartResizing")
class SmartResizing(PreprocessingLayer):
    """Image resizing layer. Wrapping the smart preprocssing functionality into a layer to embedd in models.
    See https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/smart_resize for details.
    """

    def __init__(self, height, width, interpolation="bilinear", **kwargs):
        self.target_height = height
        self.target_width = width
        self.interpolation = interpolation
        #self._interpolation_method = get_interpolation(interpolation)
        self.input_spec = InputSpec(ndim=4)
        super(SmartResizing, self).__init__(**kwargs)
        base_preprocessing_layer.keras_kpl_gauge.get_cell("Resizing").set(True)

    def call(self, inputs, **kwargs):

        def smart_resize(x, size, interpolation='bilinear'):
            if len(size) != 2:
                raise ValueError('Expected `size` to be a tuple of 2 integers, '
                                 'but got: %s' % (size,))
            img = ops.convert_to_tensor_v2_with_dispatch(x)
            if img.shape.rank is not None:
                if img.shape.rank != 3:
                    raise ValueError(
                        'Expected an image array with shape `(height, width, channels)`, but '
                        'got input with incorrect rank, of shape %s' % (img.shape,))
            shape = array_ops.shape(img)
            height, width = shape[0], shape[1]
            target_height, target_width = size

            crop_height = math_ops.cast(
                math_ops.cast(width * target_height, 'float32') / target_width, 'int32')
            crop_width = math_ops.cast(
                math_ops.cast(height * target_width, 'float32') / target_height, 'int32')

            # Set back to input height / width if crop_height / crop_width is not smaller.
            crop_height = math_ops.minimum(height, crop_height)
            crop_width = math_ops.minimum(width, crop_width)

            crop_box_hstart = math_ops.cast(
                math_ops.cast(height - crop_height, 'float32') / 2, 'int32')
            crop_box_wstart = math_ops.cast(
                math_ops.cast(width - crop_width, 'float32') / 2, 'int32')

            crop_box_start = array_ops.stack([crop_box_hstart, crop_box_wstart, 0])
            crop_box_size = array_ops.stack([crop_height, crop_width, -1])

            img = array_ops.slice(img, crop_box_start, crop_box_size)
            img = image_ops.resize_images_v2(
                images=img,
                size=size,
                method=interpolation)
            if isinstance(x, np.ndarray):
                return img.numpy()
            return img



        outputs = tf.map_fn(lambda x: smart_resize(x, size=(self.target_height, self.target_width), interpolation=self.interpolation ), inputs)

        outputs.set_shape( (inputs.shape[0], self.target_height, self.target_width, inputs.shape[-1]) )

        return outputs
