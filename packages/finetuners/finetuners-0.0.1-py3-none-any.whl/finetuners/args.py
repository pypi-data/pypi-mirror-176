from dataclasses import dataclass
from typing import Union

from transformers import TrainingArguments


@dataclass
class FinetunerArguments:

    model_name: str
    pretrained_model_name_or_path: str
    training_args: Union[dict, TrainingArguments]

    def __post_init__(self):
        if isinstance(self.training_args, dict):
            self.training_args = TrainingArguments(**self.training_args)
