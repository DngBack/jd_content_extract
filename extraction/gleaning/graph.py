from typing import Any

import tiktoken

from .prompts import (
    LOOP_PROMPT, # LOOP Prompt for gleaning
    CONTINUE_PROMPT, # Prompt for continue 
    GRAPH_EXTRACTION_PROMPT # Graph extraction prompt 
)

# from graphrag.llm import CompletionLLM#
# A lot of defaut prompt
DEFAULT_TUPLE_DELIMITER = "<|>"
DEFAULT_RECORD_DELIMITER = "##"
DEFAULT_COMPLETION_DELIMITER = "<|COMPLETE|>"


class GraphExtractor:
    """Unipartite graph extractor class definition."""

    _join_descriptions: bool
    _tuple_delimiter_key: str
    _record_delimiter_key: str
    _entity_types_key: str
    _input_text_key: str
    _completion_delimiter_key: str
    _entity_name_key: str
    _input_descriptions_key: str
    _extraction_prompt: str
    _summarization_prompt: str
    _loop_args: dict[str, Any]
    _max_gleanings: int

    def __init__(
        self,
        llm_invoker: Any,
        tuple_delimiter_key: str | None = None,
        record_delimiter_key: str | None = None,
        input_text_key: str | None = None,
        entity_types_key: str | None = None,
        completion_delimiter_key: str | None = None,
        prompt: str | None = None,
        join_descriptions=True,
        encoding_model: str | None = None,
        max_gleanings: int | None = None,
        entity_types: list[str] = None,
    ):
        """Init method definition."""
        # TODO: streamline construction
        self._llm = llm_invoker
        self._join_descriptions = join_descriptions
        self._input_text_key = input_text_key or "input_text"
        self._tuple_delimiter_key = tuple_delimiter_key or "tuple_delimiter"
        self._record_delimiter_key = record_delimiter_key or "record_delimiter"
        self._completion_delimiter_key = (
            completion_delimiter_key or "completion_delimiter"
        )
        self._entity_types_key = entity_types_key or "entity_types"
        self._extraction_prompt = prompt or GRAPH_EXTRACTION_PROMPT
        self._max_gleanings = (
            max_gleanings
            if max_gleanings is not None
            else 1
        )
        self.entity_types = entity_types

        # Construct the looping arguments
        encoding = tiktoken.get_encoding(encoding_model or "cl100k_base")
        yes = encoding.encode("YES")
        no = encoding.encode("NO")
        self._loop_args = {"logit_bias": {yes[0]: 100, no[0]: 100}, "max_tokens": 1}

    def __call__(
        self, texts: list[str], model: str) -> dict:
        """Call method definition."""
        all_records: dict[int, str] = {}
        source_doc_map: dict[int, str] = {}

        # Wire defaults into the prompt variables
        prompt_variables = {
            self._tuple_delimiter_key: DEFAULT_TUPLE_DELIMITER,
            self._record_delimiter_key: DEFAULT_RECORD_DELIMITER,
            self._completion_delimiter_key: DEFAULT_COMPLETION_DELIMITER,
            self._entity_types_key: self.entity_types,
        }

        for doc_index, text in enumerate(texts):
            # Invoke the entity extraction
            print(doc_index)
            result = self._process_document(text, model, prompt_variables)
            source_doc_map[doc_index] = text
            all_records[doc_index] = result
        return all_records

    def _process_document(
        self, text: str, model: str, prompt_variables: dict[str, str]
    ) -> str:
        extract_prompt = GRAPH_EXTRACTION_PROMPT.format(
            input_text=text,
            tuple_delimiter=prompt_variables["tuple_delimiter"],
            record_delimiter=prompt_variables["record_delimiter"],
            completion_delimiter=prompt_variables["completion_delimiter"],
            entity_types=prompt_variables["entity_types"],
        )
        messages = [
            {
                'role': 'user',
                'content': [
                    {
                        'text': extract_prompt,
                    }
                ],
            },
        ]
        response = self._llm.converse(
            modelId=model,
            messages=messages,
            inferenceConfig={"maxTokens": 4096, "temperature": 0.0, "topP": 1.0},
        )

        response_text = response["output"]["message"]["content"][0]["text"]
        results = response_text

        # Repeat to ensure we maximize entity count
        for i in range(self._max_gleanings):
            messages = [
                {
                    'role': 'user',
                    'content': [
                        {
                            'text': CONTINUE_PROMPT
                        }
                    ],
                },
            ]
            system = [
                {
                    'text': f'{extract_prompt}\n{response_text}',
                },
            ]
            glean_response = self._llm.converse(
                modelId=model,
                messages=messages,
                system=system,
                inferenceConfig={"maxTokens": 4096, "temperature": 0.0, "topP": 1.0},
            )

            glean_response = glean_response["output"]["message"]["content"][0]["text"]
            results += glean_response

            # if this is the final glean, don't bother updating the continuation flag
            if i >= self._max_gleanings - 1:
                break

            continuation = self._llm(
                LOOP_PROMPT,
                name=f"extract-loopcheck-{i}",
                history=glean_response.history or [],
                model_parameters=self._loop_args,
            )
            if continuation.output != "YES":
                break
        print("Extract entities successfully")       
        return results
