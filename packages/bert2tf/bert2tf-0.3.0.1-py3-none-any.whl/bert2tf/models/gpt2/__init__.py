import numpy as np
import tensorflow as tf

from .. import PreTrainModel
from ..embedding import BaseEmbedding
from ..helper import get_initializer, shape_list
from ..transformer import MaskedMultiHeadSelfAttention


def gelu(x):
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


class OpenAIGPT2Model(PreTrainModel):  # todo need to fix or perfect
    """GPT2 models from OpenAI"""

    def __init__(self, config, seq_len=4, **kwargs):
        super().__init__(config, **kwargs)
        self.seq_len = seq_len
        self.main = OpenAIGPT2MainLayer(config, name='transformer')

    def get_dummy_inputs(self):
        input_ids = tf.keras.Input(shape=(self.seq_len,), name='input_ids', dtype=tf.int32)

        return input_ids

    def h5_mapping(self, name_to_variable, init_variables):
        weight_value_tuples = []
        for name, value in init_variables.items():
            sub_names = list(name.split('/'))
            name = '/'.join(sub_names[1:])
            if f'{self.name}/{name}' in name_to_variable:
                weight_value_tuples.append([name_to_variable[f'{self.name}/{name}'], value])

        return weight_value_tuples

    def call(self, inputs, **kwargs):
        result = self.main(inputs)
        return result


class OpenAIGPT2MainLayer(tf.keras.layers.Layer):
    """
    GPT2 OpenAI main layer
    """

    def __init__(self, config, *inputs, **kwargs):
        super().__init__(*inputs, **kwargs)

        self.num_hidden_layers = config.n_layer
        self.vocab_size = config.vocab_size
        self.n_embd = config.n_embd

        self.type_embed = BaseEmbedding(
            config.vocab_size, config.n_embd, initializer_range=config.initializer_range, name='wte',
            word_embedding_name='weight'
        )

        self.position_embed = tf.keras.layers.Embedding(
            config.n_positions,
            config.n_embd,
            embeddings_initializer=get_initializer(config.initializer_range),
            name='wpe',
        )

        self.dropout = tf.keras.layers.Dropout(config.embd_pdrop)
        self.blocks = [GPT2OpenAIBlock(config, name=f'h_._{idx}') for idx in range(config.n_layer)]
        self.ln_f = tf.keras.layers.LayerNormalization(epsilon=config.layer_norm_epsilon, name='ln_f')

    def call(self, inputs, token_type_ids=None, position_ids=None, attention_mask=None, **kwargs):
        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            token_type_ids = inputs[1] if len(inputs) > 1 else token_type_ids
            position_ids = inputs[2] if len(inputs) > 2 else position_ids
            attention_mask = inputs[3] if len(inputs) > 3 else attention_mask
        else:
            input_ids = inputs

        input_shape = shape_list(input_ids)
        if position_ids is None:
            position_ids = tf.range(input_shape[-1], dtype=tf.int32)[tf.newaxis, :]

        input_ids = tf.reshape(input_ids, [-1, input_shape[-1]])
        position_ids = tf.reshape(position_ids, [-1, input_shape[-1]])

        inputs_embeds = self.type_embed(input_ids, mode='embedding')
        position_embeds = self.position_embed(position_ids)
        if token_type_ids is not None:
            token_type_ids = tf.reshape(token_type_ids, [-1, shape_list(token_type_ids)[-1]])
            token_type_embeds = self.type_embed(token_type_ids, mode='embedding')
        else:
            token_type_embeds = 0

        hidden_states = inputs_embeds + position_embeds + token_type_embeds
        hidden_states = self.dropout(hidden_states, kwargs['training'])

        for block in self.blocks:
            hidden_states = block([hidden_states, attention_mask])

        hidden_states = self.ln_f(hidden_states)

        output_shape = input_shape + [shape_list(hidden_states)[-1]]
        outputs = tf.reshape(hidden_states, output_shape)

        return outputs


class GPT2OpenAIBlock(tf.keras.layers.Layer):
    """
    GPT2 OpenAI block, like bert layer
    """

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)

        self.ln_1 = tf.keras.layers.LayerNormalization(name='ln_1')
        self.attn = GPT2OpenAIAttention(config, name='attn')
        self.ln_2 = tf.keras.layers.LayerNormalization(name='ln_2')
        self.mlp = GPT2OpenAIMLP(config, name='mlp')

    def call(self, inputs):
        attention_inputs, attention_mask = inputs
        attention_inputs = self.ln_1(attention_inputs)
        attention_outputs, attention_probs = self.attn([attention_inputs, attention_mask])

        resident = attention_inputs + attention_outputs
        ln_resident = self.ln_2(resident)
        mlp_outputs = self.mlp(ln_resident)
        resident = resident + mlp_outputs

        return resident


class GPT2OpenAIMLP(tf.keras.layers.Layer):
    """
    GPT2 OpenAI linear mapping
    """

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.c_fc = Conv1D(config.n_embd * 4, config.n_embd, initializer_range=config.initializer_range, name='c_fc')
        self.c_proj = Conv1D(config.n_embd, config.n_embd * 4, initializer_range=config.initializer_range,
                             name='c_proj')
        self.act = gelu
        self.dropout = tf.keras.layers.Dropout(config.resid_pdrop)

    def call(self, inputs, **kwargs):
        outputs = self.act(self.c_fc(inputs))
        outputs = self.c_proj(outputs)
        outputs = self.dropout(outputs, kwargs['training'])
        return outputs


class GPT2OpenAIAttention(MaskedMultiHeadSelfAttention):
    """
    GPT2 OpenAI attention layer
    """

    def __init__(self, config, **kwargs):
        super().__init__(hidden_size=config.n_embd, num_attention_heads=config.n_head,
                         initializer_range=config.initializer_range, attention_probs_dropout_prob=config.attn_pdrop,
                         **kwargs)

        self.c_attn = Conv1D(config.n_embd * 3, config.n_embd, initializer_range=config.initializer_range,
                             name='c_attn')
        self.c_proj = Conv1D(config.n_embd, config.n_embd, initializer_range=config.initializer_range, name='c_proj')
        self.resid_dropout = tf.keras.layers.Dropout(config.resid_pdrop)

    def call(self, query):
        input_tensor, attention_mask = query
        input_tensor = self.c_attn(input_tensor)
        query, key, value = tf.split(input_tensor, 3, axis=2)
        context_outputs, attention_probs = super().call(query=query, key=key, value=value,
                                                        attention_mask=attention_mask)
        outputs = self.c_proj(context_outputs)
        outputs = self.resid_dropout(outputs)

        return outputs, attention_probs

    def create_denses(self):
        return None, None, None


class Conv1D(tf.keras.layers.Layer):
    def __init__(self, nf, nx, initializer_range, **kwargs):
        super().__init__(**kwargs)
        self.nf = nf
        self.nx = nx
        self.initializer_range = initializer_range

    def build(self, input_shape):
        self.weight = self.add_weight(
            'weight', shape=[self.nx, self.nf], initializer=get_initializer(self.initializer_range)
        )
        self.bias = self.add_weight('bias', shape=[1, self.nf], initializer=tf.zeros_initializer())

        super().build(input_shape)

    def call(self, inputs):
        bz, sl = shape_list(inputs)[:2]

        inputs = tf.reshape(inputs, [-1, self.nx])
        outputs = tf.matmul(inputs, self.weight) + self.bias

        outputs = tf.reshape(outputs, [bz, sl, self.nf])

        return outputs
