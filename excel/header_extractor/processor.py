from __future__ import annotations

from typing import List

from domain.parsers.common.models import TableIR
from domain.parsers.common.table_processor import BFHeader
from domain.parsers.common.table_processor import HeaderExtractor as HeaderExtractorIR
from domain.parsers.common.table_processor import OrientationDetector
from domain.parsers.common.table_processor import TableChunker
from infra.llm import AzureOpenAIBaseService
from shared.base import BaseModel
from shared.logging import get_logger
from shared.settings import Settings

logger = get_logger(__name__)


class HeaderExtractorInput(BaseModel):
    file: List[TableIR]


class HeaderExtractorOutput(BaseModel):
    file: List[TableIR]


class HeaderExtractor:
    def __init__(self, settings: Settings, llm_model: AzureOpenAIBaseService):
        """Initialize property of header extractor

        Args:
            settings (Settings): setting
            llm_model (AzureOpenAIBaseService): llm model
        """
        self.settings = settings
        self.llm_model = llm_model

    @property
    def orientation_detector(self) -> OrientationDetector:
        """Get orientation detector module

        Returns:
            OrientationDetector: return OrientationDetector object
        """
        return OrientationDetector(table_setting=self.settings.table)

    @property
    def table_chunker(self) -> TableChunker:
        """Get table chunker module

        Returns:
            TableChunker: return TableChunker object
        """
        return TableChunker(
            table_settings=self.settings.table,
            gpt4o_settings=self.settings.gpt4o,
        )

    @property
    def header_extractor(self) -> HeaderExtractorIR:
        """Get header extractor module

        Returns:
            HeaderExtractor: return HeaderExtractor object
        """
        return HeaderExtractorIR(
            table_setting=self.settings.table,
            llm_model=self.llm_model,
        )

    @property
    def brute_force_header(self) -> BFHeader:
        """Get brute force header extractor module

        Returns:
            BFHeader: return BFHeader object
        """
        return BFHeader()

    def process(self, input_data: HeaderExtractorInput) -> HeaderExtractorOutput:
        """Extract Header and Chunking

        Args:
            input_data (HeaderExtractorInput): list of TableIR

        Returns:
            HeaderExtractorOutput: list of TableIR after processing
        """
        tables = input_data.file
        processed_tables = []
        for table in tables:
            table = self.orientation_detector.process(table)
            table = self.table_chunker.process(table)
            table = self.header_extractor.process(table)
            table = self.brute_force_header.process(table)
            processed_tables.append(table)

        return processed_tables
