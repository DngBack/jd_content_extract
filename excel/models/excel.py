from __future__ import annotations

from typing import Any
from typing import List

from shared.base import BaseModel


class Cell(BaseModel):
    coord: str
    content: Any = None
    color: str | None = None


class Header(BaseModel):
    horizontal: List[Cell]
    vertical: List[Cell]


class TableMetadata(BaseModel):
    coord: str
    header: Header | None = None


class Table(BaseModel):
    table_metadata: TableMetadata
    cells: List[List[Cell]]
    merged_cells: List[Cell]


class SheetFile(BaseModel):
    sheetname: str
    tables: List[Table]
    paragraph: List[Cell]
    images: List[Cell]
