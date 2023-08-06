from abc import ABC, abstractmethod

import pandas as pd

from .args import FinetunerArguments


class AbstractFinetuner(ABC):
    """Abstract finetuner class."""

    def __init__(self, dataset: pd.DataFrame, args: FinetunerArguments) -> None:
        """Initialize finetuner.

        Args:
            dataset (pd.DataFrame): Pandas dataframe with valid finetuners schema.
            args (FinetunerArguments): Arguments for finetuner.
        """
        super().__init__()
        self.dataset = dataset
        self.args = args

    @abstractmethod
    def finetune(self) -> None:
        """Run finetuning."""
