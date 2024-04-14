# Import things that are needed generically
from langchain.tools import BaseTool, StructuredTool, tool

__all__ = ["WebSearch"]


class WebSearch(BaseTool):
    def __init__(self):
        raise NotImplementedError("Will be implemented in next version")

    def _run(self):
        pass
