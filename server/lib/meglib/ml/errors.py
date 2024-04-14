__all__ = ["PDFError", "APIError"]


class PDFError(Exception):
    """Raised when the error is related to PDF processing"""

    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return f"PDFError: {self.message}"


class APIError(Exception):
    """Raised when the error is related to API fetch"""

    def __init__(self, message):
        self.message = message

    def __str__(self) -> str:
        return f"APIError: {self.message}"
