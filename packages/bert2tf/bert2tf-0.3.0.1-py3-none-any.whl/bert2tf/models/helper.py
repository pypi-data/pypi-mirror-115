import tensorflow as tf


def gelu(x):
    """ Gaussian Error Linear Unit.
    Original Implementation of the gelu activation function in Google Bert repo when initially created.
        For information: OpenAI GPT's gelu is slightly different (and gives slightly different results):
        0.5 * x * (1 + torch.tanh(math.sqrt(2 / math.pi) * (x + 0.044715 * torch.pow(x, 3))))
        Also see https://arxiv.org/abs/1606.08415
    """
    cdf = 0.5 * (1.0 + tf.math.erf(x / tf.math.sqrt(2.0)))
    return x * cdf


def gelu_new(x):
    """Gaussian Error Linear Unit.
    This is a smoother version of the RELU.
    Original paper: https://arxiv.org/abs/1606.08415
    Args:
        x: float Tensor to perform activation.
    Returns:
        `x` with the GELU activation applied.
    """
    cdf = 0.5 * (1.0 + tf.tanh((np.sqrt(2 / np.pi) * (x + 0.044715 * tf.pow(x, 3)))))
    return x * cdf


def swish(x):
    return x * tf.sigmoid(x)


ACT2FN = {
    'gelu': tf.keras.layers.Activation(gelu),
    'relu': tf.keras.activations.relu,
    'swish': tf.keras.layers.Activation(swish),
    'gelu_new': tf.keras.layers.Activation(gelu_new),
}


def get_initializer(initializer_range=0.02):
    """Creates a `tf.initializers.truncated_normal` with the given range.
    Args:
        initializer_range: float, initializer range for stddev.
    Returns:
        TruncatedNormal initializer with stddev = `initializer_range`.
    """
    return tf.keras.initializers.TruncatedNormal(stddev=initializer_range)


def shape_list(x):
    """Deal with dynamic shape in tensorflow cleanly."""
    static = x.shape.as_list()
    dynamic = tf.shape(x)
    return [dynamic[i] if s is None else s for i, s in enumerate(static)]


def get_weights_dict_from_h5(file_path):
    """Get weights from h5 file
    it will return a dict, key is weight's name, value is weight's value
    """
    import h5py
    from tensorflow.python.keras.saving.hdf5_format import load_attributes_from_hdf5_group
    import numpy as np
    with h5py.File(file_path) as f:
        weights_dict = {}
        for name, group in f.items():
            weight_names = load_attributes_from_hdf5_group(group, 'weight_names')
            weights = {weight_name[:-2]: np.asarray(group[weight_name]) for weight_name in weight_names}
            if weights is not None:
                weights_dict.update(weights)

        return weights_dict
