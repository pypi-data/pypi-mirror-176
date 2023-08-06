import torch

from recsys.models.retrieval import DeepRetriever
from recsys.models.scoring import NCF
from recsys.test.fixtures import (  # NOQA
    dummy_interaction_dataset,
    dummy_interactions,
    dummy_item_features,
    dummy_seq2seq_dataset,
    dummy_user_features,
)


def test_deepretriever(dummy_interaction_dataset):
    model = DeepRetriever(dummy_interaction_dataset.data_schema)
    model.fit(dataset=dummy_interaction_dataset)

    pair = torch.tensor([[1, 2]])
    user = torch.tensor([[0, 1, 0, 1]])
    item = torch.tensor([[0, 0]])

    model(pair, user, item)


def test_ncf(dummy_interaction_dataset):
    model = NCF(dummy_interaction_dataset.data_schema)
    model.fit(dataset=dummy_interaction_dataset)

    pair = torch.tensor([[1, 2]])
    user = torch.tensor([[0, 1, 0, 1]])
    item = torch.tensor([[0, 0]])

    model(pair, user, item)
