"""Dictionary related utility functions."""

__author__ = "730554887"

from csv import DictReader

DATA_DIRECTORY = "../../data"
DATA_FILE_PATH = f"{DATA_DIRECTORY}/nc_durham_2015_march_21_to_26.csv"

# Define your functions below


def read_csv_rows(filename: str) -> list[dict[str, str]]:
    """Read the rows of a csv into a 'table'."""
    result: list[dict[str, str]] = []
    file_handle = open(filename, "r", encoding="utf8")
    csv_reader = DictReader(file_handle)
    for row in csv_reader:
        result.append(row)
    file_handle.close()
    return result


def column_values(table: list[dict[str, str]], column: str) -> list[str]:
    """Produce a list[str] of all values in a single column."""
    result: list[str] = []
    for row in table:
        item: str = row[column]
        result.append(item)
    return result


def columnar(row_table: list[dict[str, str]]) -> dict[str, list[str]]:
    """Transform a row-oriented table to a column oriented table."""
    result: dict[str, list[str]] = {}

    first_row: dict[str, str] = row_table[0]
    for column in first_row:
        result[column] = column_values(row_table, column)
    return result


def head(column_table: dict[str, list[str]], numbers: int) -> dict[str, list[str]]:
    """Produced a column based table with the first N rows of data."""
    result: dict[str, list[str]] = {}
    i: int = 0
    for row in column_table:
        values: list[str] = []
        i = 0
        while i < numbers:
            values.append(column_table[row][i])
            i += 1
        result[row] = values
    return result


def select(column_table: dict[str, list[str]], column_names: list[str]) -> dict[str, list[str]]:
    """Produce a table with only a subset of original columns."""
    result: dict[str, list[str]] = {}
    for items in column_names:
        result[items] = column_table[items]
    return result


def concat(column_table_1: dict[str, list[str]], column_table_2: dict[str, list[str]]) -> dict[str, list[str]]:
    """Produce a table with two column-based tables combined."""
    result: dict[str, list[str]] = {}
    for row in column_table_1:
        result[row] = column_table_1[row]
    for row in column_table_2:
        if row in result:
            result[row] += column_table_2[row]
        else:
            result[row] = column_table_2[row]
    return result


def count(values: list[str]) -> dict[str, int]:
    """Counts frequencies of items."""
    result: dict[str, int] = {}
    for item in values:
        if item in result:
            result[item] += 1
        else:
            result[item] = 1
    return result