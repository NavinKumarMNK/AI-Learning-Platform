from langchain.docstore.document import Document
from typing import List


__all__ = ["DocumentProcessor"]


class DocumentProcessor:
    def __init__(self):
        pass

    def split_by_char(self, document: Document, char="\n") -> List[Document]:
        """Splits a document into smaller documents at each occurrence of a specified character.

        Parameters
        ----------
        document : Document
            The document to be split.
        char : str, optional
            The character at which to split the document, by default "\n".

        Returns
        -------
        List[Document]
            A list of split documents.
        """
        return [
            Document(page_content=content, metadata=document.metadata)
            for content in document.page_content.split(char)
        ]

    def recursive_split_overlap(
        self, document: Document, min_size: int, overlap: int
    ) -> List[Document]:
        """Recursively splits a document into smaller documents, with a specified minimum size and overlap.

        Parameters
        ----------
        document : Document
            The document to be split.
        min_size : int
            The minimum size for each split document.
        overlap : int
            The size of the overlap between consecutive split documents.

        Returns
        -------
        list[Document]
            A list of split documents.
        """

        content = document.page_content
        metadata = document.metadata
        if len(content) <= min_size:
            return [document]

        split_point = min_size
        while split_point < len(content) and content[split_point] not in ["\n", "."]:
            split_point += 1

        if split_point == len(content):
            split_point = min_size

        if split_point + overlap >= len(content):
            return [document]

        first_half = Document(content[: split_point + overlap], metadata=metadata)
        second_half = Document(content[split_point:], metadata=metadata)
        return self.recursive_split_overlap(
            first_half, min_size, overlap
        ) + self.recursive_split_overlap(second_half, min_size, overlap)


if __name__ == "__main__":
    obj = DocumentProcessor()
    docs = Document("""# Title of the Document

## Introduction
The introduction provides an overview of the topic at hand. It should be engaging and informative.

## Section 1: Topic A
This section delves into the first topic. It should provide detailed information and can be broken down into sub-sections as needed.

### Subsection 1.1
Details about a specific aspect of Topic A.

### Subsection 1.2
Details about another aspect of Topic A.

## Section 2: Topic B
This section covers the second topic. Like the first section, it should provide detailed information and can have sub-sections.

### Subsection 2.1
Details about a specific aspect of Topic B.

### Subsection 2.2
Details about another aspect of Topic B.

## Conclusion
The conclusion wraps up the document, summarizing the main points and providing final thoughts.

## References
If any external sources were used in the creation of the document, they should be listed here.""")

    _docs = obj.recursive_split_overlap(document=docs, min_size=200, overlap=50)
    print(len(_docs), _docs[0])

    _docs = obj.split_by_char(document=docs, char="\n")
    print(len(_docs), _docs[0])
