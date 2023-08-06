from collections import defaultdict

import numpy as np
import pandas as pd
import torch

from recsys.datasets.utils import dataframe_schema


class InteractionsDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        interactions,
        user_features,
        item_features,
        user_id="user_id",
        item_id="item_id",
        interaction_id="interaction",
        sample_negatives=0,
        target_column=None,
    ):

        self.user_id = user_id
        self.item_id = item_id
        self.interaction_id = interaction_id

        # Check proper dataframe columns order
        # Call assert subfunction to chekc user is first, item second and interaction third
        # Assert in both user and item dfs too

        self.interactions = interactions[[user_id, item_id, interaction_id]]

        self.user_features = dict(
            zip(
                user_features[self.user_id],
                user_features.drop(self.user_id, axis=1).to_numpy(dtype=int),
            )
        )
        self.item_features = dict(
            zip(
                item_features[self.item_id],
                item_features.drop(self.item_id, axis=1).to_numpy(dtype=int),
            )
        )

        if target_column and sample_negatives:
            # TODO WRITE THIS LOGIC
            assert 1 == 0  # Error because logic wont work

        # Create a nice way of loading context + item features into a single
        # dataset. Generate schema that models read from and are able to create
        self.n_users = user_features[self.user_id].max() + 1
        self.n_items = item_features[self.item_id].max() + 1

        self.interactions_pd_schema = dataframe_schema(self.interactions)
        self.user_pd_schema = dataframe_schema(user_features.drop(self.user_id, axis=1))
        self.item_pd_schema = dataframe_schema(item_features.drop(self.item_id, axis=1))

        if self.interactions[self.interaction_id].isin([0, 1]).all():
            self.target_type = "binary"
        else:
            self.target_type = "continuous"

        self.interactions = interactions.values
        self.sample_negatives = sample_negatives
        if self.sample_negatives > 0:
            self.unique_items = item_features[self.item_id].unique()
        # To do add custom target column

    def __len__(self):
        return len(self.interactions)

    def _sample_negative(self):
        # TODO make this not sample already interacted items
        return np.random.choice(self.unique_items)

    def __getitem__(self, idx):
        interaction = self.interactions[idx]

        user, item, target = interaction[0], interaction[1], interaction[2]
        if self.sample_negatives > 0:
            negative_dice = np.random.randint(1, self.sample_negatives + 1)
            if negative_dice > 1:
                item = self._sample_negative()
                target = 0

        user_features = self.user_features[user]
        item_features = self.item_features[item]

        return (
            np.array([user, item, target]),
            user_features,
            item_features,
        )

    def __castdtypes(self, data):
        """Ensure needed dtypes for the data_Schema"""

    @property
    def data_schema(self):
        return {
            "interactions": [self.n_users, self.n_items],
            "user_features": self.user_pd_schema,
            "item_features": self.item_pd_schema,
            "objetive": self.target_type,
        }

    @staticmethod
    def collate_fn(batch_output):
        return batch_output


class Seq2SeqDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        sequences: pd.DataFrame,
        item_features: pd.DataFrame,
        max_item_id: int,
        sequence_id: str = "sequence",
        item_id: str = "item_id",
        mode: str = "train",
        max_length: int = 20,
        mask_token: int = 1,
        pad_token: int = 0,
        mask_prob: float = 0.15,
        random_seq_start: bool = False,
    ):
        self.max_item_id = max_item_id
        self.sequence_id = sequence_id
        self.item_id = item_id
        self.mode = mode
        self.max_length = max_length
        self.mask_token = mask_token
        self.pad_token = pad_token
        self.mask_prob = mask_prob
        self.random_seq_start = random_seq_start

        self.sequences = sequences[[sequence_id]]
        self.context_features = sequences.loc[:, sequences.columns != sequence_id]

        self.item_features = dict(
            zip(
                item_features[self.item_id],
                item_features.drop(self.item_id, axis=1).values,
            )
        )

        self.item_features = defaultdict(
            lambda: np.array(
                [0 for feature in item_features.drop(self.item_id, axis=1)]
            ),
            self.item_features,
        )

        # Create a nice way of loading context + item features into a single
        # dataset. Generate schema that models read from and are able to create
        self.n_items = item_features[self.item_id].max() + 1

        # Add context
        self.item_pd_schema = dataframe_schema(item_features.drop(self.item_id, axis=1))

        self.sequences = self.sequences.values
        self.context_features = self.context_features.values
        # To do add custom target column

    def __len__(self):
        return len(self.sequences)

    def _maskSequence(
        self,
        sequence,
    ):
        """Masks a sequence according to the masking parameters"""
        tokens = []
        labels = []
        for s in sequence:
            prob = np.random.random()
            if prob < self.mask_prob:
                prob /= self.mask_prob
                if prob < 0.8:
                    tokens.append(self.mask_token)
                elif prob < 0.9:
                    tokens.append(
                        np.random.randint(low=2, high=self.max_item_id, size=1)[0]
                    )
                else:
                    tokens.append(s)

                labels.append(s)
            else:
                tokens.append(s)
                labels.append(self.pad_token)

        return tokens, labels

    def __getitem__(self, index):
        seq = self.sequences[index][0]
        if self.mode == "train":
            seq = seq[:-1]  # Remove the latest one we will use for validation
            if not self.random_seq_start or len(seq) < self.max_length + 1:
                seq = seq[-self.max_length :]
            # randomize the sequene within the full sequence, only if
            # max_length<len(tokens)
            else:
                idx = np.random.randint(self.max_length, len(seq))
                seq = seq[:idx][-self.max_length :]

            mask_len = self.max_length - len(seq)

            tokens, labels = self._maskSequence(seq)

            tokens = [self.pad_token] * mask_len + tokens
            labels = [self.pad_token] * mask_len + labels

            features = [self.item_features[item_id] for item_id in tokens]

            return (
                torch.LongTensor(tokens),
                torch.LongTensor(labels),
                torch.LongTensor(features),
            )

        elif self.mode == "validate":
            mask_len = self.max_length - len(seq)

            tokens = np.copy(seq).tolist()[-self.max_length :]
            labels = np.copy(seq).tolist()[-self.max_length :]

            tokens = [self.pad_token] * mask_len + tokens[:-1] + [self.mask_token]
            labels = [self.pad_token] * mask_len + labels

            features = [self.item_features[item_id] for item_id in tokens]

            return (
                torch.LongTensor(self.vocab(tokens)),
                torch.LongTensor(self.vocab(labels)),
                torch.LongTensor(features),
            )

        elif (
            self.mode == "inference"
        ):  # Prediction data requires user column. TODO: exception if no user data?
            # tokens = np.copy(seq).tolist()
            # if self.max_length == len(seq):
            #     tokens = tokens[1:]
            # elif len(seq) > self.max_length:
            #     error_msg = f"sequence length {len(seq)} was longer than expected {self.max_length}"
            #     raise ValueError(error_msg)
            # else:
            #     pad_len = self.max_length - len(seq) - 1
            #     tokens = [self.mask_token] * pad_len + tokens
            # tokens += [self.mask_token]
            # user = self.user_data[index]

            # return torch.LongTensor(self.vocab(tokens)), user
            pass

    @property
    def data_schema(self):
        return {
            "n_items": self.n_items,
            "item_features": self.item_pd_schema,
            "max_length": self.max_length,
        }


class SparseInteractionsDataset(torch.utils.data.Dataset):
    pass


class SequenceDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        sequences: pd.DataFrame,
        item_features: pd.DataFrame,
        max_item_id: int,
        sequence_id: str = "sequence",
        item_id: str = "item_id",
        mode: str = "train",
        max_length: int = 20,
        random_seq_start: bool = False,
        min_length: int = 1,
    ):
        self.max_item_id = max_item_id
        self.sequence_id = sequence_id
        self.item_id = item_id
        self.mode = mode
        self.random_seq_start = random_seq_start
        self.min_length = min_length

        self.sequences = sequences[[sequence_id]]
        self.context_features = sequences.loc[:, sequences.columns != sequence_id]

        self.item_features = dict(
            zip(
                item_features[self.item_id],
                item_features.drop(self.item_id, axis=1).values,
            )
        )

        self.item_features = defaultdict(
            lambda: np.array(
                [0 for feature in item_features.drop(self.item_id, axis=1)]
            ),
            self.item_features,
        )
        self.n_items = item_features[self.item_id].max() + 1

        self.item_pd_schema = dataframe_schema(item_features.drop(self.item_id, axis=1))

        self.sequences = self.sequences.values
        self.context_features = self.context_features.values

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, index):
        seq = self.sequences[index][0]
        if self.mode == "train" or self.mode == "validate":

            if self.random_seq_start and not (len(seq) < self.min_length + 1):
                min_index = np.random.randint(0, len(seq) - self.min_length - 2)
                seq = seq[min_index : np.random.randint(min_index + 1, len(seq))]

            tokens = seq[:-1]
            label = seq[-1]

            features = [self.item_features[item_id] for item_id in tokens]

            return (
                torch.LongTensor(tokens),
                label,
                torch.LongTensor(features),
            )
        elif self.mode == "inference":
            pass

    @property
    def data_schema(self):
        return {
            "n_items": self.n_items,
            "item_features": self.item_pd_schema,
            "min_length": self.min_length,
            "max_length": self.max_length,
        }
