from langchain.docstore.document import Document
from typing import List


class DocumentProcessor:
    def __init__(self):
        pass

    def process_split(
        self,
        docs: List[Document],
        type="recursive-text-split",
    ):
        pass


if __name__ == "__main__":
    obj = DocumentProcessor()
    docs = [Document("")]
    docs = obj.process_split(docs)
    print(docs)
