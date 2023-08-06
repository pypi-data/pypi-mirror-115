from ..bert import BertModel, BertMLMHead


class RobertaModel(BertModel):
    """
    Roberta, it has same structure with bert
    """


class RobertaPreTrainingModel(RobertaModel):
    """
    Roberta Pre Training Model, it exclude nsp task
    """

    def __init__(self, config, **kwargs):
        super(RobertaPreTrainingModel, self).__init__(config, with_pooler=False, **kwargs)
        self.mlm = BertMLMHead(self.config.vocab_size, self.config.hidden_size, self.config.initializer_range,
                               self.config.hidden_act, self.embeddings, name='cls')

    def call(self, inputs, **kwargs):
        hidden_states = super(RobertaPreTrainingModel, self).call(inputs)
        prediction_scores = self.mlm(hidden_states)

        return prediction_scores
