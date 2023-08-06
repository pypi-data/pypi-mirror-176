from typing import List

import pandas as pd
import pandera as pa
from pandera.typing import Object, Series

from .exceptions import MultipleValidSchemasException, NoValidSchemasException

# TODO: make label2id dict and df match validator
# TODO: add label column name to schemas

# ---------------------------------------------------------------------------- #
#                              Text Classification                             #
# ---------------------------------------------------------------------------- #


class MultiClassTextClassificationSchema(pa.SchemaModel):
    """Dataframe schem for expressing and validating multi class text classification datasets."""

    text: Series[str] = pa.Field()
    label: Series[str] = pa.Field()
    split: Series[str] = pa.Field(isin=["train", "val", "test"])

    @classmethod
    def make_label2id(cls, df: pd.DataFrame):
        unique_labels = sorted(df["label"].unique().tolist())
        label2id = {}
        for idx, label in enumerate(unique_labels):
            label2id[label] = idx
        return label2id


class MultiLabelTextClassificationSchema(pa.SchemaModel):
    """Dataframe schem for expressing and validating multi label text classification datasets."""

    text: Series[str] = pa.Field()
    labels: Series[Object] = pa.Field()
    split: Series[str] = pa.Field(isin=["train", "val", "test"])

    @pa.check("labels")
    def check_labels_type(cls, series: Series[Object]) -> Series[bool]:
        return check_list_of_str(series)

    @classmethod
    def make_label2id(cls, df: pd.DataFrame):
        raise NotImplementedError


# ---------------------------------------------------------------------------- #
#                             Token Classification                             #
# ---------------------------------------------------------------------------- #


class MultiClassTokenClassificationSchema(pa.SchemaModel):
    """Dataframe schem for expressing and validating multi class token classification datasets."""

    tokens: Series[Object] = pa.Field()
    labels: Series[Object] = pa.Field()
    split: Series[str] = pa.Field(isin=["train", "val", "test"])

    @pa.check("tokens")
    def check_tokens_type(cls, series: Series[Object]) -> Series[bool]:
        return check_list_of_str(series)

    @pa.check("labels")
    def check_labels_type(cls, series: Series[Object]) -> Series[bool]:
        return check_list_of_str(series)

    @classmethod
    def make_label2id(cls, df: pd.DataFrame):
        raise NotImplementedError


ALL_SCHEMAS = [
    MultiClassTextClassificationSchema,
    MultiLabelTextClassificationSchema,
    MultiClassTokenClassificationSchema,
]

# ---------------------------------------------------------------------------- #
#                                Check Functions                               #
# ---------------------------------------------------------------------------- #


def check_list(col: Series[Object]) -> Series[bool]:
    return col.apply(lambda x: isinstance(x, list))


def check_list_of_str(col: Series[Object]) -> Series[bool]:
    return check_list(col) & col.apply(lambda x: all([isinstance(e, str) for e in x]))


# ---------------------------------------------------------------------------- #
#                      Dataframe Schema Utility Functions                      #
# ---------------------------------------------------------------------------- #


def identify_schema(df: pd.DataFrame) -> pa.SchemaModel:
    """Identify valid finetuners schema for a given pandas dataframe.

    Args:
        df (pd.DataFrame): Dataframe to identify schema of.

    Raises:
        MultipleValidSchemasException: Raised if multiple schemas are valid.
        NoValidSchemasException: Raised if no schemas are valid.

    Returns:
        pa.SchemaModel: Valid schema model.
    """

    # find valid schemas
    valid_schemas = []
    for schema in ALL_SCHEMAS:
        try:
            schema.validate(df, lazy=True)
            valid_schemas.append(schema)
        except:
            pass

    if len(valid_schemas) == 1:
        return valid_schemas.pop()
    elif len(valid_schemas) > 1:
        raise MultipleValidSchemasException
    else:
        raise NoValidSchemasException
