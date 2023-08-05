import numpy as np

import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.utils import conv_utils
from tensorflow.python.framework import tensor_shape
from tensorflow.python.keras import constraints, initializers, regularizers

from quple.interface.tfq.layers import PQC
from quple.interface.tfq.tf_utils import get_output_shape

class QConv2DEx(PQC):
    def __init__(self, kernel_circuit,
                 data_circuit,
                 operators,
                 kernel_size,
                 filters=1,
                 strides=1,
                 padding='same',
                 trainable=True,
                 kernel_initializer=tf.keras.initializers.RandomUniform(0, 2 * np.pi),
                 kernel_regularizer=None,
                 kernel_constraint=None,
                 parameter_sharing=True,
                 name=None, **kwargs):
        super(QConv2D, self).__init__(kernel_circuit, 
                                      data_circuit, 
                                      operators,
                                      trainable=trainable, 
                                      name=name,
                                      **kwargs)
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        self.filters = filters
        self.rank = 2
        self.kernel_size = conv_utils.normalize_tuple(kernel_size, self.rank, 'kernel_size')
        self.strides = conv_utils.normalize_tuple(strides, self.rank, 'strides')
        self.padding = conv_utils.normalize_padding(padding)
        self.parameter_sharing = parameter_sharing
        self._validate_init()
        self._input_resolver = self._get_input_resolver()
        
    def _validate_init(self):
        if not all(self.kernel_size):
            raise ValueError('The argument `kernel_size` cannot contain 0(s). '
                           'Received: %s' % (self.kernel_size,))

        if not all(self.strides):
            raise ValueError('The argument `strides` cannot contains 0(s). '
                           'Received: %s' % (self.strides,))
            
        kernel_size = self.kernel_size[0]*self.kernel_size[1]
        if self._n_qubit != kernel_size:
            raise ValueError(f"The kernel size (={kernel_size}) must match the number of "
                             f"data qubits (={self._n_qubit})")
            
    def build(self, input_shape):
        """Keras build function."""
        assert len(input_shape) in [3, 4]
        if len(input_shape) == 3:
            self.input_rows = input_shape[1]
            self.input_cols = input_shape[2]
            self.input_channels = 1
        else:
            self.input_rows = input_shape[1]
            self.input_cols = input_shape[2]
            self.input_channels = input_shape[3]
        output_shape = get_output_shape(input_shape[1:3], self.kernel_size, self.strides, self.padding)
        self.output_rows = output_shape[0]
        self.output_cols = output_shape[1]
        
        if self.parameter_sharing:
            kernel_shape = tf.TensorShape([self.filters, self.input_channels, self._symbols.shape[0]])
        else:
            kernel_shape = tf.TensorShape([self.filters, self.input_channels, 
                                           self.output_rows,
                                           self.output_cols,
                                           self._symbols.shape[0]])

        self.kernel = self.add_weight(
            name='kernel',
            shape=kernel_shape,
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint,
            trainable=True,
            dtype=self.dtype)
        
        super().build(input_shape)
            
    def init_weights(self):
        pass
        
    def _get_input_resolver(self):
        kernel_size = (1, 1) + self.kernel_size + (1,)
        strides = (1, 1) + self.strides + (1,)
        padding = self.padding.upper()
        batchsize = lambda x: tf.gather(tf.shape(x), 0)
        # planes = number of channels
        planes = lambda x: tf.gather(tf.shape(x), 3)
        rows = lambda x: tf.gather(tf.shape(x), 1)
        cols = lambda x: tf.gather(tf.shape(x), 2)
        depth = 1
        # change to (batchsize, depth, rows, cols)
        transposed_input = lambda x: tf.transpose(x, [0,3,1,2])
        reshaped_input = lambda x: tf.reshape(transposed_input(x), 
                                              shape=(batchsize(x), planes(x), rows(x), cols(x), depth))
        input_patches = lambda x: tf.extract_volume_patches(reshaped_input(x),
            ksizes=kernel_size, strides=strides, padding=padding)
        resolved_input = lambda x: self._data_circuit_resolver(input_patches(x))
        return resolved_input
        
    def call(self, inputs):
        """Keras call function."""
        batchsize = tf.gather(tf.shape(inputs), 0)
        if tf.rank(inputs) == 3:
            rows = tf.gather(tf.shape(inputs), 1)
            cols = tf.gather(tf.shape(inputs), 2)
            reshaped_inputs = tf.reshape(inputs, [batchsize, rows, cols, 1])
            resolved_inputs_ = self._input_resolver(reshaped_inputs)
        else:
            resolved_inputs_ = self._input_resolver(inputs)
        depth = tf.gather(tf.shape(resolved_inputs_), 1)
        rows = tf.gather(tf.shape(resolved_inputs_), 2)
        cols = tf.gather(tf.shape(resolved_inputs_), 3)
        # change to (depth, batchsize, rows, cols, symbols)
        resolved_inputs = tf.transpose(resolved_inputs_, [1, 0, 2, 3, 4])
        # total number of circuit = filters*depth*batchsize*rows*cols
        circuit_size = tf.reduce_prod([self.filters, batchsize, depth, rows, cols])
        # tile inputs to (filters, depth, batchsize, rows, cols, symbols)
        tiled_up_inputs_ = tf.tile([resolved_inputs], [self.filters, 1, 1, 1, 1, 1])
        # reshape inputs to (circuit_size, symbols)
        tiled_up_inputs = tf.reshape(tiled_up_inputs_, (circuit_size, tf.shape(tiled_up_inputs_)[-1]))
        if self.parameter_sharing:
            # tile size for weights = batchsize*rows*cols
            tile_size = tf.reduce_prod([batchsize, rows, cols])
            tiled_up_weights__ = tf.tile([self.kernel], [tile_size, 1, 1, 1])
            # change to (filters, depth, batchsize*rows*cols, weight_symbols)
            tiled_up_weights_ = tf.transpose(tiled_up_weights__, [1, 2, 0, 3])
        else:
            # tile size for weights = batchsize
            # weight now has shape (batchsize, filters, depth, rows, cols, weight_symbols)
            tiled_up_weights__ = tf.tile([self.kernel], [batchsize, 1, 1, 1, 1, 1])
            # change to (filters, depth, batchsize, rows, cols, weight_symbols)
            tiled_up_weights_ = tf.transpose(tiled_up_weights__, [1, 2, 0, 3, 4, 5])
        # reshape to (circuit_size, weight_symbols)
        tiled_up_weights = tf.reshape(tiled_up_weights_, (circuit_size, tf.shape(tiled_up_weights_)[-1]))
        from pdb import set_trace
        set_trace()
        tiled_up_parameters = tf.concat([tiled_up_inputs, tiled_up_weights], 1)
        tiled_up_data_circuit = tf.tile(self._data_circuit, [circuit_size])
        tiled_up_model = tf.tile(self._model_circuit, [circuit_size])
        model_appended = self._append_layer(tiled_up_data_circuit, append=tiled_up_model)
        tiled_up_operators = tf.tile(self._operators, [circuit_size, 1])
        # this is disabled to make autograph compilation easier.
        # pylint: disable=no-else-return
        if self._analytic:
            result = self._executor(model_appended,
                                   symbol_names=self._all_symbols,
                                   symbol_values=tiled_up_parameters,
                                   operators=tiled_up_operators)
        else:
            tiled_up_repetitions = tf.tile(self._repetitions,
                                           [circuit_batch_dim, 1])
            result =  self._executor(model_appended,
                                    symbol_names=self._all_symbols,
                                    symbol_values=tiled_up_parameters,
                                    operators=tiled_up_operators,
                                    repetitions=tiled_up_repetitions)
        reshaped_output = tf.reshape(result, 
                          (self.filters, self.input_channels, batchsize, self.output_rows, self.output_cols))
        summed_output = tf.reduce_sum(reshaped_output, axis=1)
        final_output = tf.transpose(summed_output, [1, 2, 3, 0])
        return tf.reshape(final_output, (batchsize, self.output_rows, self.output_cols, self.filters))
        # pylint: enable=no-else-return