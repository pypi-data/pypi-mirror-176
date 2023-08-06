from functools import cached_property

import pandas as pd
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    logging,
)

from .abstract import AbstractFinetuner
from .args import FinetunerArguments
from .dataset import FinetunersDataset
from .exceptions import NotValidSchemaException
from .schemas import (
    MultiClassTextClassificationSchema,
    MultiLabelTextClassificationSchema,
)

logging.set_verbosity_error()


class FinetunerForTextClassification(AbstractFinetuner):
    """Finetuner for text classification."""

    def __init__(
        self,
        dataset: FinetunersDataset,
        args: FinetunerArguments,
    ) -> None:
        super().__init__(dataset, args)

    @cached_property
    def tokenizer(self) -> AutoTokenizer:
        return AutoTokenizer.from_pretrained(self.args.pretrained_model_name_or_path)

    @cached_property
    def model(self) -> AutoTokenizer:
        return AutoModelForSequenceClassification.from_pretrained(
            self.args.pretrained_model_name_or_path,
            num_labels=len(self.dataset.label2id),
            id2label=self.dataset.id2label,
            label2id=self.dataset.label2id,
        )

    def finetune(self) -> None:
        """Run finetuning"""

        self.dataset.tokenize(tokenizer=self.tokenizer)

        # # init trainer
        self.trainer = Trainer(
            model=self.model,
            args=self.args.training_args,
            tokenizer=self.tokenizer,
            train_dataset=self.dataset.huggingface_dataset["train"],
            eval_dataset=self.dataset.huggingface_dataset["val"],
        )

        # try:
        #     self.trainer.train()
        # finally:
        #     self.model = self.trainer.model


class FinetunerForTokenClassification(AbstractFinetuner):
    def __init__(self, dataset: pd.DataFrame, args: FinetunerArguments) -> None:
        super().__init__(dataset, args)

    def finetune(self) -> None:
        raise NotImplementedError()
