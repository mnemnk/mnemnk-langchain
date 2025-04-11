from typing import Any
from . import BaseAgent, run_agent

class PyPDFLoaderAgent(BaseAgent):
    """Load PDF file using PyPDFLoader."""

    def process_input(self, _ch: str, _kind: str, value: Any):
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(value)
        for page in loader.lazy_load():
            doc_dict = {
                "metadata": page.metadata,
                "page_content": page.page_content,
            }
            self.write_out("document", "document", doc_dict)
            self.write_out("content", "text", page.page_content)

def main():
    run_agent(PyPDFLoaderAgent)


if __name__ == "__main__":
    main()
