from __future__ import annotations

import json
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union


TEMP_JOB_CONTENT = """
### これは仕事に関する情報です:

## この仕事の給与:
{salary}

## 勤務地:
{locations}

## 選考プロセス:
{select_process}

## 詳細情報:
{supplement}
"""


class JsonParser(BaseParser):
    """
    A service class that processes job description JSON content
    to extract specific job and company information.

    Attributes:
        jd_content (Optional[Dict]): A dictionary to store the
        jd content. Defaults to None.
    """
    jd_content: Optional[Dict] = None  # Declare jd_content as an attribute with default value

    def _get_job_dict(self, jd_content: dict) -> dict:
        """
        Extract specific job-related information from the given
        job description content.

        Args:
            jd_content (dict): The job description content containing various job-related information.

        Returns:
            dict: A dictionary containing the position name, job name, and job type.
        """
        job_dict_infor = {
            'positionName': jd_content.get('positionName', ''),
            'jobName': jd_content.get('jobName', ''),
            'jobType': jd_content.get('jobType', ''),
        }
        return job_dict_infor

    def _get_company_content(self, jd_content: dict) -> str:
        """
        Generate a string containing company information from the job description content.

        Args:
            jd_content (dict): The job description content containing company information.

        Returns:
            str: A string formatted with the company information.
        """
        company_info = self._convert_to_string(jd_content.get('corporate', ''))
        return '### 会社情報について: \n' + company_info

    def _get_job_content(self, jd_content: dict) -> str:
        """
        Generate a detailed job description string using additional job content.

        Args:
            jd_content (dict): The job description content containing detailed job information.

        Returns:
            str: A formatted string containing salary, locations, selection process,
            and supplementary information.
        """
        salary, locations, select_process = self._addition_job_content(jd_content)
        supplement = jd_content['content']['markdownFreeText']
        jd_content_str = TEMP_JOB_CONTENT.format(
            salary=salary, locations=locations,
            select_process=select_process, supplement=supplement,
        )
        return jd_content_str

    def _addition_job_content(self, jd_content: dict) -> Tuple[str, str, str]:
        """
        Extract additional job content, including salary, locations, and selection process.

        Args:
            jd_content (dict): The job description content containing additional job-related information.

        Returns:
            salary, locations, select_process: salary, locations, and selection process of job as strings.
        """
        jd_content_value = jd_content.get('content', '')
        if jd_content_value:
            salary = self._convert_to_string(jd_content_value.get('salary', ''))
            locations = self._convert_to_string(jd_content_value.get('locations', ''))
            locationSupplement = self._convert_to_string(jd_content_value.get('locationSupplement', ''))
            locations += f'\n# locationSupplement:\n{locationSupplement}'
            select_process = self._convert_to_string(jd_content_value.get('descriptions', ''))
        return salary, locations, select_process

    def _convert_to_string(self, content: Union[str, dict, list]) -> str:
        """
        Convert the input content to string.

        Args:
            content (Union[str, dict, list]): The input content to be converted.

        Returns:
            str: The converted content as a string.
        """
        def _convert_dict_to_string(content):
            if isinstance(content, dict):
                return ', '.join([f'{k}: {v}' for k, v in content.items()])
            else:
                return str(content)
        if isinstance(content, list):
            return '\n'.join([_convert_dict_to_string(item) for item in content])
        else:
            return _convert_dict_to_string(content)

    def read(self, inputs: ParserInput) -> ReadFileOutput:
        """
        Load the input JSON content into the dict.

        Args:
            inputs (ParserInput): An instance of ParserInput.

        Returns:
            dict: The dictionary content of JD.
        """
        input_dict =  json.loads(inputs.file_content)
        return ReadFileOutput(file_content=input_dict)

    def process(self, inputs: ParserInput) -> ParserOutput:
        """
        Process the input JSON content to extract job-related and company-related information.

        Args:
            input (JsonParserInput): An instance of JsonParserInput containing the job description content.

        Returns:
            JsonParserOutPut: An instance of JsonParserOutPut containing
            extracted job dictionary, job content, and company content.
        """
        list_content = []
        try:
            self.jd_content = self.read(inputs).file_content
        except Exception as e:
            logger.exception(
                f'Error occurred while read json file: {str(e)}',
                extra={'inputs': inputs},
            )
            raise e

        try:
            job_dict = self._get_job_dict(self.jd_content)
            list_content.append(self._convert_to_string(job_dict))
        except Exception as e:
            logger.exception(
                f'Error occurred while extracting job dict: {str(e)}',
                extra={'jd_content': self.jd_content},
            )
            raise e

        try:
            job_content = self._get_job_content(self.jd_content)
            list_content.append(job_content)
        except Exception as e:
            logger.exception(
                f'Error occurred while generating job content: {str(e)}',
                extra={'jd_content': self.jd_content},
            )
            raise e

        try:
            company_content = self._get_company_content(self.jd_content)
            list_content.append(company_content)
        except Exception as e:
            logger.exception(
                f'Error occurred while extracting company content: {str(e)}',
                extra={'jd_content': self.jd_content},
            )
            raise e

        return ParserOutput(
            list_content=['\n'.join(list_content)],
        )

    
