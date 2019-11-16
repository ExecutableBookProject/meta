from abc import ABC, abstractmethod
import copy
from typing import List, Union

import panflute as pf


class BaseChunk(ABC):
    @classmethod
    @abstractmethod
    def declare_options(self) -> dict:
        """Return a JSON schema of chunk options."""
        return {}

    @classmethod
    @abstractmethod
    def declare_formats(self) -> Union[None, List[str]]:
        """Return a list of supported output types.
        
        None indicates that it supports all outputs
        """
        return []

    def __init__(self, *, output_fmt: str, doc_metadata: dict):
        """Initiate an instance."""
        if output_fmt not in self.declare_formats():
            raise TypeError(
                f"{self.__class__.__name__} is not compatible with '{output_fmt}' outputs"
            )
        self.output_fmt = output_fmt
        self.doc_metadata = copy.deepcopy(doc_metadata)

    @abstractmethod
    def process_chunk(self, *, text: str, options: dict) -> Union[pf.Block, None]:
        """Process the chunk, and return a pandoc block level element."""
        return None

    def clean_up(self):
        """Called after all chunks in a document have been processed."""
        pass
