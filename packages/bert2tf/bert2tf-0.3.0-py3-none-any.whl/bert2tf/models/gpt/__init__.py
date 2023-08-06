import numpy as np

from ..auto_regressive import AutoRegressive
from ..bert import BertMLMHead, BertModel, BertEmbedding, BertEncoder


class OpenAIGPTModel(BertModel):
    def __init__(self, name='gpt', *args, **kwargs):
        super().__init__(with_pooler=False, name=name, *args, **kwargs)

    def create_embedding_layer(self, config):
        embeddings = OpenAIGPTEmbedding(config.vocab_size, config.hidden_size, config.initializer_range,
                                        config.hidden_dropout_prob, config.max_position_embeddings,
                                        name='embeddings')
        return embeddings

    def create_encoder_layer(self, config):
        encoder = OpenAIGPTEncoder(config.hidden_size, config.num_attention_heads, config.num_hidden_layers,
                                   config.attention_probs_dropout_prob, config.initializer_range,
                                   config.hidden_dropout_prob, config.hidden_act, config.intermediate_size,
                                   name='transformer')
        return encoder


class OpenAIGPTPretraingModel(OpenAIGPTModel):
    def call(self, inputs, **kwargs):
        hidden_states = super().call(inputs, **kwargs)
        prediction_scores = self.embeddings(hidden_states, mode='linear')

        return prediction_scores


class OpenAIGPTAutoRegressiveModel(OpenAIGPTPretraingModel, AutoRegressive):
    """OpenAI GPT auto regressive models"""

    def __init__(self, end_id, start_id=None, top_k=4, top_p=None, num_samples=1, min_ends=1, min_len=16, max_len=128,
                 *args, **kwargs):
        """

        :param end_id: full stop or exclamation point id etc in vocab
        :param start_id:  first token of whole generate sentences
        :param top_k: generate from top k probability
        :param top_p: sample from over top probability and sum of probability
        :param num_samples: how many samples should we sample, used for beam search
        :param min_ends: related to end id, should the models stops at how many end id were generated
        :param min_len: the minimum length of generate sentence
        :param max_len: max length of sample sentence
        """
        super().__init__(*args, **kwargs)
        self.end_id = end_id
        self.start_id = start_id
        self.top_k = top_k
        self.min_ends = min_ends
        self.min_len = min_len
        self.max_len = max_len
        self.top_p = top_p
        self.num_samples = num_samples

    def next_token_scores(self, inputs, output_ids, **kwargs):
        input_ids, segment_ids = inputs
        curr_segment_ids = np.zeros_like(output_ids) + input_ids[0, -1]
        input_ids = np.concatenate([input_ids, output_ids], 1)
        segment_ids = np.concatenate([segment_ids, curr_segment_ids], 1)
        scores = self.call([input_ids, None, segment_ids], **kwargs)[:, -1]

        return scores


class HuaweiGPTModel(BertModel):
    """Huawei GPT models"""

    def __init__(self, *args, **kwargs):
        super().__init__(with_pooler=False, *args, **kwargs)

    def call(self, inputs, **kwargs):
        if isinstance(inputs, (list, tuple)) and len(inputs) > 2:
            inputs = list(inputs)
            inputs.insert(2, None)  # set segment ids to None

        return super().call(inputs, **kwargs)

    def create_embedding_layer(self, config):
        embeddings = HuaweiGPTEmbedding(config.vocab_size, config.hidden_size, config.initializer_range,
                                        config.hidden_dropout_prob, config.max_position_embeddings, name='embeddings')
        return embeddings

    def create_encoder_layer(self, config):
        encoder = HuaweiGPTEncoder(config.hidden_size, config.num_attention_heads, config.num_hidden_layers,
                                   config.attention_probs_dropout_prob, config.initializer_range,
                                   config.hidden_dropout_prob, config.hidden_act, config.intermediate_size,
                                   name='encoder')
        return encoder


class HuaweiGPTPreTrainingModel(HuaweiGPTModel):
    """
    GPT pre training models from huawei, it has same structure with bert, but it uses masked self attention as self attention.
    it is used for pre training
    """

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.mlm = BertMLMHead(self.config.vocab_size, self.config.hidden_size, self.config.initializer_range,
                               self.config.hidden_act, self.embeddings, name='cls')

    def call(self, inputs, **kwargs):
        hidden_states = super().call(inputs, **kwargs)
        prediction_scores = self.mlm(hidden_states)
        return prediction_scores


class HuaweiGPTAutoRegressiveModel(HuaweiGPTPreTrainingModel, AutoRegressive):
    """
    GPT auto regressive models from huawei, it has same structure with bert, but it uses masked self attention as self attention.
    it is used for generate text
    """

    def __init__(self, end_id, start_id=None, top_k=4, top_p=None, num_samples=1, min_ends=1, min_len=16, max_len=128,
                 *args, **kwargs):
        """

        :param end_id: full stop or exclamation point id etc in vocab
        :param start_id:  first token of whole generate sentences
        :param top_k: generate from top k probability
        :param top_p: sample from over top probability and sum of probability
        :param num_samples: how many samples should we sample, used for beam search
        :param min_ends: related to end id, should the models stops at how many end id were generated
        :param min_len: the minimum length of generate sentence
        :param max_len: max length of sample sentence
        """
        super().__init__(*args, **kwargs)
        self.end_id = end_id
        self.start_id = start_id
        self.top_k = top_k
        self.min_ends = min_ends
        self.min_len = min_len
        self.max_len = max_len
        self.top_p = top_p
        self.num_samples = num_samples

    def next_token_scores(self, inputs, output_ids):
        inputs = np.concatenate([inputs[0], output_ids], 1)
        return self.call(inputs)[:, -1]


class OpenAIGPTEmbedding(BertEmbedding):
    """OpenAI GPT Embedding"""

    def __init__(self, *args, **kwargs):
        super().__init__(use_token_type_embedd=False, share_word_embedding=True, *args, **kwargs)

    def call(self, inputs, **kwargs):
        return super().call(inputs, do_ln=False, **kwargs)


class HuaweiGPTEmbedding(BertEmbedding):
    """Huawei GPT Embedding"""

    def __init__(self, *args, **kwargs):
        super().__init__(use_token_type_embedd=False, *args, **kwargs)


class HuaweiGPTEncoder(BertEncoder):
    """
    Encoder for Huawei GPT
    """

    def __init__(self, *args, **kwargs):
        super().__init__(masked=True, *args, **kwargs)


class OpenAIGPTEncoder(HuaweiGPTEncoder):
    """
        Encoder for OpenAI GPT
        """
