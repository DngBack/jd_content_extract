from __future__ import annotations

from typing import Dict
from typing import List
from typing import Tuple

import numpy as np
from domain.parsers.excel.models.excel import Cell
from domain.parsers.excel.models.excel import Table
from domain.parsers.excel.models.excel import TableMetadata
from domain.parsers.excel.utils import cal_num_row_col
from domain.parsers.excel.utils import coor_str_to_coor_list
from domain.parsers.excel.utils import create_cell_obj
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.worksheet.worksheet import Worksheet
from pandas.core.frame import DataFrame
from shared.base import BaseModel
from shared.base import BaseService
from shared.logging import get_logger
from skimage.measure import label
from skimage.measure import regionprops
from xlsxwriter.utility import xl_col_to_name

logger = get_logger(__name__)


class TableExtractorInput(BaseModel):
    file: Tuple[DataFrame, Worksheet, str]


class TableExtractorOutput(BaseModel):
    file: List[Table]


class TableExtractor():
    def process(self, input_data: TableExtractorInput) -> TableExtractorOutput:
        """Extract table data from input file

        Args:
            input_data (TableExtractorInput): input data of TableExtractor

        Returns:
            TableExtractorOutput: output data of TableExtractor
        """
        file = input_data.file
        self.__df, self.__sheet, _ = file
        tables = self.__extract_table_data()
        return tables

    def __create_default_cell(self, coord: str) -> Cell:
        """Create default cell

        Args:
            coord (str): coordinate string of Cell

        Returns:
            Cell: return Cell
        """
        return create_cell_obj(coord, '', '')

    def __extract_table_data(self) -> List[Table]:
        """Extract table data

        Returns:
            List[Table]: list of table data defined in Table pydantic model
        """
        table_meta_by_text = self.__find_tables_by_text()
        table_meta_by_border = self.__find_tables_by_border()

        index_text_not_valid = []

        for index, table_text in enumerate(table_meta_by_text):
            try:
                if any([
                    True if table_bor.coord.split(':')[0] in CellRange(table_text.coord) else False
                    for table_bor in table_meta_by_border
                ]):
                    index_text_not_valid.append(index)
            except Exception as e:
                logger.exception(f"""ERROR: error when find index of invalid table text, error: {e},
                                table_meta_by_text: {table_meta_by_text},
                                table_meta_by_border: {table_meta_by_border}""")
                continue

        metadata_list = table_meta_by_border + [
            table_meta_by_text[i] for i in range(len(table_meta_by_text))
            if i not in index_text_not_valid
        ]

        def __check_table_valid(num):
            return True if num[0] > 2 and num[1] > 2 else False

        metadata_list = [
            metadata for metadata in metadata_list
            if __check_table_valid(cal_num_row_col(metadata.coord))
        ]
        tables = [self.__extract_cell_data(table_metadata) for table_metadata in metadata_list]
        return tables

    def __extract_cell_data(self, table_metadata: TableMetadata) -> Table:
        """Extract Cells and merged cells in sheet to init Table data

        Args:
            table_metadata (TableMetadata): Metadata of table defined in TableMetadata pydantic model

        Returns:
            Table: table data defined in Table pydantic model
        """
        table_coord = table_metadata.coord
        cells, merged_cells = [], []
        for row_id, row in enumerate(self.__sheet.iter_rows()):
            coord_list = coor_str_to_coor_list(table_coord)
            if row_id in range(coord_list[0] + 1, coord_list[2] + 1):
                cell_row = []
                for cell in row[coord_list[1]:coord_list[3]]:
                    try:
                        cell_row.append(self.__create_cell_data(cell, is_repeat=True))
                    except Exception as e:
                        logger.exception(f'ERROR: error when creating cell data, error: {e}, cell: {cell}')
                        continue
                cells.append(cell_row)

        merged_cells = self.__extract_merged_cells(table_coord)

        if len(cells) == 0:
            cells = [[self.__create_default_cell('A1')]]
        if len(merged_cells) == 0:
            merged_cells = [self.__create_default_cell('A1:A2')]

        return Table(
            cells=cells,
            merged_cells=merged_cells,
            table_metadata=table_metadata,
        )

    def __create_cell_data(self, cell: Cell, is_repeat=True) -> Cell:
        """Create single cell data

        Args:
            cell (Cell): Cell data defined in Cell pydantic model
            is_repeat (bool, optional): This boolean indicates whether none cells
            in merged cells will be duplicated content or not. Defaults to True.

        Returns:
            Cell: Cell data defined in Cell pydantic model
        """
        content = cell.value
        coord = cell.coordinate
        color = cell.fill.start_color.rgb
        try:
            for merged_cell in self.__sheet.merged_cells.ranges:
                if not content or cell.coordinate in merged_cell:
                    content = merged_cell.start_cell.value if is_repeat else None
                    color = merged_cell.start_cell.fill.start_color.rgb

            return create_cell_obj(coord, content, color)
        except Exception as e:
            logger.exception(f'ERROR: error when create cell data, error: {e}')

    def __extract_merged_cells(self, table_coord: str) -> List[Cell]:
        """Extract merged cells

        Args:
            table_coord (str): coordinate of table represented in string. i.e: "A1:D10"

        Returns:
            List[Cell]: List of cell data defined in Cell pydantic model
        """
        merged_cells = []
        for cell in self.__sheet.merged_cells.ranges:
            try:
                if cell.coord in CellRange(table_coord):
                    coord, value = cell.coord, cell.start_cell.value
                    color = cell.start_cell.fill.start_color.rgb
                    merged_cells.append(create_cell_obj(coord, value, color))
            except Exception as e:
                logger.exception(f'ERROR when creating create_cell_obj, error: {e}, cell: {cell}')
                continue
        return merged_cells

    def __init_table_metadata(self, larr: np.ndarray) -> List[TableMetadata]:
        """Init table metadata

        Args:
            larr (np.ndarray): Larr numpy of sheet data

        Returns:
            List[TableMetadata]: List of TableMetadata defined in TableMetadata pydantic model
        """
        table_metadata_list = []
        for s in regionprops(larr):
            try:
                coord = s.bbox
                start_col, start_row = xl_col_to_name(coord[1]), coord[0] + 1
                end_col, end_row = xl_col_to_name(coord[3] - 1), coord[2]
                coord_str = f'{start_col}{start_row}:{end_col}{end_row}'
                table_metadata_list.append(TableMetadata(coord=coord_str))
            except Exception as e:
                logger.exception(f'ERROR when creating table metadata, error: {e}')
                continue
        return table_metadata_list

    def __find_tables_by_text(self) -> List[TableMetadata]:
        """Find table based on cell content

        Returns:
            List[TableMetadata]: List of TableMetadata defined in TableMetadata pydantic model
        """
        larr = label(np.array(self.__df.notnull()).astype('int'))
        table_metadata_list = self.__init_table_metadata(larr)
        return table_metadata_list

    def __find_tables_by_border(self) -> List[TableMetadata]:
        """Find table based on cell border

        Returns:
            List[TableMetadata]: List of TableMetadata defined in TableMetadata pydantic model
        """

        all_data = []
        for row in self.__sheet.iter_rows():
            try:
                row_list = []
                for cell in row:
                    if any([
                        getattr(cell.border, border)
                        for border in ['left', 'right', 'bottom', 'top']
                    ]):
                        row_list.append(1)
                    else:
                        row_list.append(0)
                all_data.append(row_list)
            except Exception as e:
                logger.exception(f"""ERROR: error when larr of border, error: {e},
                                 row={row}""")
                continue

        larr = label(np.array(all_data).astype('int'))
        table_metadata_list = self.__init_table_metadata(larr)
        return table_metadata_list
