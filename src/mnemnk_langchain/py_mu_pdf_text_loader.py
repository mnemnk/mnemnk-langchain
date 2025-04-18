from . import BaseAgent, run_agent


class PyMuPDFTextLoaderAgent(BaseAgent):
    """Load PDF file using PyMuPDF."""

    def process_input(self, _ch: str, _kind: str, value: any):
        import fitz # PyMuPDF

        pdf = fitz.open(value)
        for page in pdf:
            text = page.get_text()
            doc_dict = {
                "metadata": {"page_number": page.number},
                "page_content": text,
            }
            self.write_out("document", "document", doc_dict)
            self.write_out("content", "text", text)


def main():
    run_agent(PyMuPDFTextLoaderAgent)


if __name__ == "__main__":
    main()
