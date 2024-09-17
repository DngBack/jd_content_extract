from __future__ import annotations

from enum import Enum
from typing import Dict

from domain.parsers.excel.models.excel import SheetFile
from infra.llm import AzureOpenAIBaseService
from infra.llm import AzureOpenAIInput
from infra.llm import CompletionMessage
from infra.llm import MessageRole
from shared.base import BaseModel
from shared.base import BaseService
from shared.logging import get_logger

from .prompts import OUTPUT_FORMAT
from .prompts import SYSTEM_MESSAGE
from .prompts import USER_MESSAGE

logger = get_logger(__name__)


class HeaderPrompt(str, Enum):
    HEADER_PROMPT = """
    You will analyze the content of each table row with given header information in the input table and convert it into a natural paragraph
    """
    HEADLESS_PROMPT = """
    The table is headless, you just analyze the content of each table row in the input table and convert it into a natural paragraph
    """


class SummarizationInput(BaseModel):
    file: SheetFile


class SummarizationOutput(BaseModel):
    file: str


class SummarizationExtractor:
    def __init__(self, llm_model: AzureOpenAIBaseService):
        self.llm_model = llm_model

    def process(self, input_data: SummarizationInput) -> SummarizationOutput:
        """Extract Summarization of sheet file

        Args:
            input_data (SummarizationInput): input data of SummarizationExtractor

        Returns:
            SummarizationOutput: output data of SummarizationExtractor
        """

        file = input_data.file
        summarization = self.__summarize(file)
        return summarization

    def __summarize(self, sheet_data: SheetFile) -> str:
        """Summarize all table in a sheet

        Args:
            input_data: ExcelFile object
        Returns:
            output_data: string summarization content
        """

        tables = sheet_data.tables
        total_answer = f'Sheetname: {sheet_data.sheetname} \n'
        for index_table in range(len(tables)):
            try:
                total_answer = f'Table {index_table + 1}: \n'
                input_data = {}
                input_data['header'] = tables[index_table].table_metadata.header
                cells = tables[index_table].cells
                for index_batch in range(len(cells)):
                    cell_list = cells[index_batch]
                    input_data['table_rows'] = [
                        {
                            key: getattr(cell, key) for key in cell.model_fields.keys()
                            if key != 'color'
                        } for cell in cell_list
                    ]
                    if tables[index_table].table_metadata.header:
                        header_prompt = HeaderPrompt.HEADER_PROMPT.value
                    else:
                        header_prompt = HeaderPrompt.HEADLESS_PROMPT.value

                    system_prompt = SYSTEM_MESSAGE
                    user_prompt = USER_MESSAGE.format(input_data=input_data, output_format=OUTPUT_FORMAT, header_prompt=header_prompt)

                    system_message = CompletionMessage(role=MessageRole.SYSTEM, content=system_prompt)
                    user_message = CompletionMessage(role=MessageRole.USER, content=user_prompt)
                    azure_input = AzureOpenAIInput(message=[system_message, user_message], json_mode=True)
                    answer = self.llm_model.process(azure_input)
                    azure_output = answer.response
                    total_answer += ' ' + azure_output['content']

                total_answer += '\n\n'
            except Exception as e:
                logger.exception(f'ERROR: error when summarize table file, error: {e}')
                continue

        total_answer += '. '.join([
                        cell.content for cell in sheet_data.paragraph
                        if type(cell.content) is str
        ])
        return total_answer
