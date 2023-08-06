import json
import pathlib
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict

import pandas as pd
import pandera as pa
from datasets.arrow_dataset import Batch
from transformers import AutoTokenizer
from transformers.tokenization_utils_base import BatchEncoding

from datasets import Dataset, DatasetDict

from .schemas import identify_schema


@dataclass
class FinetunersDataset:
    """Class for holding dataset and label2id dictionary."""

    df: pd.DataFrame
    label2id: Dict[str, int] = None
    schema: pa.SchemaModel = field(init=False)
    id2label: Dict[int, str] = field(init=False)
    huggingface_dataset: DatasetDict = field(init=False)

    def __post_init__(self):

        self.huggingface_dataset = convert_huggingface_dataset(self.df)
        if self.label2id is None:
            self.label2id = self.schema.make_label2id(self.df)

        self.id2label = toggle_label2id(label2id=self.label2id)

    @cached_property
    def schema(self) -> pa.SchemaModel:
        return identify_schema(df=self.df)

    @classmethod
    def from_path(cls, path: str):
        path = pathlib.Path(path)
        path_df = path.joinpath("dataset.json")
        path_label2id = path.joinpath("label2id.json")
        df = pd.read_json(path_df)
        if path_label2id.is_file():
            with open(path_label2id, "r") as fp:
                label2id = json.load(fp)
        else:
            label2id = None
        return cls(df=df, label2id=label2id)

    def tokenize(self, tokenizer: AutoTokenizer) -> None:

        # TODO: Needs custom tokenization routine for each task type
        def tokenize(batch: Batch):
            tokenized_batch = tokenizer(
                batch["text"],
                padding="max_length",
                truncation=True,
            )
            return tokenized_batch

        self.huggingface_dataset.map(tokenize, batched=True)


# ---------------------------------------------------------------------------- #
#                               Utility Functions                              #
# ---------------------------------------------------------------------------- #


def toggle_label2id(label2id: Dict[str, int]) -> Dict[int, str]:
    return dict(
        list(
            zip(
                list(label2id.values()),
                list(label2id.keys()),
            ),
        )
    )


def convert_huggingface_dataset(df: pd.DataFrame) -> DatasetDict:
    # TODO: why can't i make this a staticmethod?
    # TODO: retrieve label col name from schema somehow?
    huggingface_dataset = DatasetDict()

    for split in ["train", "val", "test"]:

        huggingface_dataset[split] = Dataset.from_pandas(
            df.loc[df["split"] == split].drop(columns=["split"]),
            preserve_index=False,
        )

    return huggingface_dataset
