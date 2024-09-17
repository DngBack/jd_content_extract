from __future__ import annotations

import re
import string
from typing import Any

import pandas as pd
from domain.parsers.excel.models.excel import Cell
from shared.logging import get_logger

logger = get_logger(__name__)


def find_only_alpha(str: str) -> list[str]:
    """Find only alphabet substring

    Args:
        str (str): string input

    Returns:
        list[str]: return list of alphabet substring
    """
    return re.findall('[a-zA-Z]+', str)


def find_only_number(str: str) -> list[str]:
    """Find only number substring

    Args:
        str (str): string input

    Returns:
        list[str]: return list of number substring
    """
    return re.findall(r'\d+', str)


def col2num(col: str) -> int:
    """Convert Col string in excel to number

    Args:
        col (str): Coordinate column of cell. i.e: A

    Returns:
        int: Number value of this col
    """
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c) - ord('A') + 1)
    return num


def cal_num_row_col(coord: str) -> list[int]:
    """Calculate number of row and column in table

    Args:
        coord (str): String coordinate of table. i.e: "A1: H10"

    Returns:
        list[int]: Number of row and column of table
    """
    try:
        start_col, end_col = find_only_alpha(coord)
        start_row, end_row = find_only_number(coord)
        num_col = col2num(end_col) - col2num(start_col) + 1
        num_row = int(end_row) - int(start_row) + 1
        return [num_row, num_col]
    except Exception as e:
        logger.exception(f"""CRITICAL ERROR: error when find
                         number of row and table, error: {e}""")
        raise e


def coor_str_to_coor_list(coord: str) -> list[int]:
    """Convert string coordinate to list int coordinate

    Args:
        coord (str): String coordinate of table. i.e: "A1: H10"

    Returns:
        list[int]: Coordinate of tabel represented in list int
    """
    try:
        start_col, end_col = find_only_alpha(coord)
        start_row, end_row = find_only_number(coord)
        start_col, end_col = col2num(start_col), col2num(end_col) + 1
        start_row, end_row = int(start_row) - 1, int(end_row)
        return [start_row, start_col, end_row, end_col]
    except Exception as e:
        logger.exception(f"""CRITICAL ERROR: error when convert
                         string coordinate to list int coordinate, error: {e}""")
        raise e


def create_cell_obj(coord: str, content: Any, color: str | None) -> Cell:
    """Create cell obj

    Args:
        coord (str): String coordinate cell. i.e: "A1"
        content (Any): value of cell
        color (str | None): color of cell

    Returns:
        Cell: Cell data defined in Cell pydantic model
    """

    if content is not None:
        content = str(content)
    return Cell(coord=coord, content=content, color=color)
