<a href="https://github.com/Dansk-Data-Science-Community/finetuners"><img src="melting_face.jpeg" width="250" align="right" /></a>
# Finetuners: Reduce cognitive load when finetuning transformers 🥴

Catchy intro describing the value proposition of the finetuners package.

## Installation

```
pip install finetuners
```


## Example


```python
import pathlib

from finetuners import (
    FinetunerArguments,
    FinetunerForTextClassification,
    FinetunersDataset,
)

# load dataset
dataset = FinetunersDataset.from_path(
    pathlib.Path(__file__).parents[1].joinpath("datasets", "angry-tweets")
)

# define arguments
args = FinetunerArguments(
    model_name="awesome_model",
    pretrained_model_name_or_path="Maltehb/danish-bert-botxo",
    training_args={
        "output_dir": "./runs/",
        "learning_rate": 5e-5,
    },
)

# init finetuner
finetuner = FinetunerForTextClassification(
    dataset=dataset,
    args=args,
)


finetuner.finetune()

```
