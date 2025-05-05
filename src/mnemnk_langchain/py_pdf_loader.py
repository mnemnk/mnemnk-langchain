from typing import Any, Optional
from . import BaseAgent, run_agent

class PyPDFLoaderAgent(BaseAgent):
    """Load PDF file using PyPDFLoader."""

    def process_input(self, _ch: str, _kind: str, value: Any, metadata: Optional[dict[str, Any]]):
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(value)
        out_texts = []
        out_doc_dicts = []
        for page in loader.lazy_load():
            doc_dict = {
                "metadata": page.metadata,
                "page_content": page.page_content,
            }
            out_texts.append(page.page_content)
            out_doc_dicts.append(doc_dict)
        self.write_out("documents", "document", out_doc_dicts, metadata)
        self.write_out("contents", "text", out_texts, metadata)

def main():
    run_agent(PyPDFLoaderAgent)


if __name__ == "__main__":
    main()
