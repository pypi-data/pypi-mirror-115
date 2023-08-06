"""str SQL utilities."""
import functools
from typing import Dict, List, Optional

from wpdatautil.textwrap import indent4


class SqlQuery:
    """SQL query helper to apply transformations to input columns, returning the output columns and query."""

    def __init__(self, inputs: List[str], *, transformations: Dict[str, Optional[str]], template: str) -> None:
        """Return a SQL query object.

        :param inputs: Input column names.
        :param transformations: Applicable transformations to input columns. If a column is to be transformed, its name is the key and its value is the transformation.
                                In the value, {col} is replaced with the respective column name. If the value is None, the column is skipped.
        :param template: SQL query to format. In it, {selections} is formatted with the actual selections.

        Example: SqlQuery(['c1', 'c2', 'c3'],
                  transformations={'c2': None, 'c3': '{col} * 2', 'c4': 'count(*)'},
                  template="SELECT {selections}
                            FROM t")
        """
        self._inputs, self._transformations, self._template = inputs, transformations, template

    @functools.cached_property
    def selections(self) -> Dict[str, str]:
        """Return the output column selections.

        Example: {'c1': 'c1', 'c3': 'c3 * 2', 'c4': 'count(*)'}
        """
        return sql_column_selections(self._inputs, transformations=self._transformations)

    @functools.cached_property
    def outputs(self) -> List[str]:
        """Return the output column names.

        Example: ['c1', 'c3', 'c4']
        """
        return list(self.selections)

    @functools.cached_property
    def query(self) -> str:
        """Return the formatted query.

        Example:
        -------
            SELECT
                c1,
                c3 * 2 AS c3,
                count(*) AS c4
            FROM t

        """
        return self._template.format(selections=sql_column_selections_str(self.selections))


def sql_column_selections(inputs: List[str], *, transformations: Dict[str, Optional[str]]) -> Dict[str, str]:
    """Return a mapping of SQL SELECT clauses given the input columns after applying the given transformations.

    Example: sql_column_selections(['c1', 'c2', 'c3'], transformations={'c2': None, 'c3': '{col} * 2', 'c4': 'count(*)'}) -> {'c1': 'c1', 'c3': 'c3 * 2', 'c4': 'count(*)'}

    :param inputs: Input column names.
    :param transformations: Applicable transformations. If a column is to be transformed, its name is the key and its value is the transformation.
                            In the value, {col} is replaced with the respective column name. If the value is None, the column is skipped.
    """
    outputs = inputs + [c for c in transformations if c not in inputs]
    del inputs
    selections = {}

    for column_name in outputs:
        if column_name in transformations:
            transformed_column = transformations[column_name]
            if transformed_column is None:
                continue  # Skip column.
            transformed_column = transformed_column.format(col=column_name)
            selections[column_name] = transformed_column
        else:
            selections[column_name] = column_name

    return selections


def sql_column_selections_str(inputs: Dict[str, str]) -> str:
    """Return a string representation of a mapping of SQL SELECT clauses.

    Example: {'c1': 'c1', 'c2': 'c2 * 2'} -> 'c1, c2 * 2 AS c2'
    """
    selections = ", ".join(k if k == v else f"\n{v} AS {k}" for k, v in inputs.items())
    if "\n" in selections:
        selections = "\n" + indent4(selections, levels=1)
    return selections
