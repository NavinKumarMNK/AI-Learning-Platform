import re
from bs4 import BeautifulSoup
from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader
from langchain.docstore.document import Document
from PyPDF2 import PdfReader, PdfWriter
from typing import Dict, List
from meglib.ml.errors import PDFError


class PDFLoader:
    # (regex ,to_string)
    FILTER_CONTENT = (
        (re.compile(r"\d.{1,3}\b(?:\w\s{0,5}){1,}\d+"), ""),
        (re.compile(r"[A-Z]{3,}"), ""),
        (re.compile(r"\.\s{1,}"), ""),
    )
    MIN_SNIPPET_LEN = 20

    def __init__(self):
        pass

    def _parse_content(self, data):
        soup = BeautifulSoup(data.page_content, "html.parser")
        content_divs = soup.find_all("div")
        return content_divs

    def _extract_snippets(self, content_divs):
        current_font_size = None
        current_text = ""
        snippets = []
        page_number = 0

        for div in content_divs:
            span = div.find("span")
            anchor = div.find("a")

            if anchor:
                anchor_name = anchor.get("name")
                if anchor_name is not None:
                    try:
                        page_number = int(anchor.text.split(" ")[-1])
                    except ValueError:
                        page_number = -1

            if not span:
                continue

            style = span.get("style")
            if not style:
                continue

            font_size = re.findall("font-size:(\d+)px", style)
            if not font_size:
                continue

            font_size = int(font_size[0])
            if not current_font_size:
                current_font_size = font_size

            if font_size == current_font_size:
                current_text += div.text
            else:
                snippets.append([current_text, current_font_size, page_number])
                current_font_size = font_size
                current_text = div.text

        snippets.append([current_text, current_font_size, page_number])
        return snippets

    def _create_semantic_snippets(self, snippets, data):
        current_index = -1
        semantic_snippets = []
        previous_page_number = 1

        for snippet in snippets:
            text, font_size, page_number = snippet
            text = text.replace("-\n", "")
            text = text.replace(".\n", "<new-line>")
            text = text.replace("\n", " ")
            text = text.replace("<new-line>", ".\n")

            # if current snippet's font size > previous section's heading => it is a new heading
            if (
                not semantic_snippets
                or font_size > semantic_snippets[current_index].metadata["heading_font"]
            ):
                metadata = {
                    "heading": text,
                    "content_font": 0,
                    "heading_font": font_size,
                    "pages": None,
                }
                metadata.update(data.metadata)
                semantic_snippets.append(Document(page_content="", metadata=metadata))
                current_index += 1
                continue

            # if current snippet's font size <= previous section's content => content belongs to the same section
            if (
                not semantic_snippets[current_index].metadata["content_font"]
                or font_size
                <= semantic_snippets[current_index].metadata["content_font"]
            ):
                semantic_snippets[current_index].page_content += text
                semantic_snippets[current_index].metadata["content_font"] = max(
                    font_size, semantic_snippets[current_index].metadata["content_font"]
                )
                semantic_snippets[current_index].metadata["pages"] = list(
                    range(previous_page_number, page_number + 1)
                )
                continue

            # if current snippet's font size > previous section's content but less than previous section's heading than also make a new
            # section (e.g. title of a PDF will have the highest font size but we don't want it to subsume all sections)
            metadata = {
                "heading": text,
                "content_font": 0,
                "heading_font": font_size,
                "pages": list(range(previous_page_number, page_number + 1)),
            }
            previous_page_number = page_number
            metadata.update(data.metadata)
            semantic_snippets.append(Document(page_content="", metadata=metadata))
            current_index += 1

        return semantic_snippets

    def _extract_pages(self, input_pdf, output_pdf, start_page, end_page):
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        # Add pages to the writer
        for page_number in range(start_page - 1, end_page):
            page = reader.pages[page_number]
            writer.add_page(page)

        # Write the pages to a new file
        with open(output_pdf, "wb") as output_file:
            writer.write(output_file)

    def _filter_semantic_snippets(self, extracted_snippets):
        filtered_snippets = []
        for snippet in extracted_snippets:
            if len(snippet.page_content) > self.MIN_SNIPPET_LEN:
                for regex_pattern, string in self.FILTER_CONTENT:
                    snippet.page_content = re.sub(
                        regex_pattern, string, snippet.page_content
                    )
                filtered_snippets.append(snippet)

        return filtered_snippets

    def parse_document(self, path: str, meta_data: Dict) -> List[Document]:
        """Parses the PDF document and extracts semantic snippets.

        This method loads the PDF document from the given path, extracts the pages within the specified range,
        parses the content of the pages, extracts snippets based on font size and page number, groups the snippets
        into semantic sections, and filters the sections based on predefined criteria.

        Parameters
        ----------
        path : str
            The system path to the PDF document to be parsed.
        meta_data : dict
            A dictionary containing metadata for the document. It should include 'start_page' and 'end_page' keys
            specifying the range of pages to be extracted from the document.

        Returns
        -------
        Documents: list | None
            A list of filtered semantic snippets extracted from the document. Each snippet is a Document object
            containing the text of the snippet and its associated metadata.
        """
        try:
            self._extract_pages(
                path, path + "extra", meta_data["start_page"], meta_data["end_page"]
            )
        except IndexError:
            raise PDFError("Page Number not exists in the PDF Document")

        self.loader = PDFMinerPDFasHTMLLoader(path + "extra")
        data = self.loader.load()[0]

        content_divs = self._parse_content(data)
        extracted_snippets = self._extract_snippets(content_divs)
        semantic_snippets = self._create_semantic_snippets(extracted_snippets, data)
        filtered_snippets = self._filter_semantic_snippets(semantic_snippets)

        return filtered_snippets


# test
if __name__ == "__main__":
    obj = PDFLoader()
    import os

    root_path = os.environ.get("ROOT_PATH", None)
    if not root_path:
        raise KeyError("There is no ROOT_PATH attribute in the env variables")

    file_path = os.path.join(root_path, "temp", "pdf_loader_test.pdf")
    docs = obj.parse_document(
        file_path,
        {"start_page": 14, "end_page": 29},
    )
