from . import BaseAgent, run_agent


class PyMuPDFTextLoaderAgent(BaseAgent):
    """Load PDF file using PyMuPDF."""

    def process_input(self, _ch: str, _kind: str, value: any):
        import fitz # PyMuPDF

        pdf = fitz.open(value)
        out_texts = []
        out_doc_dicts = []
        for page in pdf:
            text = page.get_text()
            out_texts.append(text)
            doc_dict = {
                "metadata": {"page_number": page.number},
                "page_content": text,
            }
            out_doc_dicts.append(doc_dict)
        self.write_out("documents", "document", out_doc_dicts)
        self.write_out("contents", "text", out_texts)


def main():
    run_agent(PyMuPDFTextLoaderAgent)


if __name__ == "__main__":
    main()
