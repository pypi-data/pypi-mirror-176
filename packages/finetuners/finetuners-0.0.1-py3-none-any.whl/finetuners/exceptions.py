# TODO: make more informative exceptions 😅


class MultipleValidSchemasException(Exception):
    """Exception raised when multiple schemas are valid given a dataframe."""


class NoValidSchemasException(Exception):
    """Exception raised when no schemas are valid given a dataframe."""


class NotValidSchemaException(Exception):
    """Exception raised when schema is not valid in a given context."""
