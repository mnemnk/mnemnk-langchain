from typing import override

from . import AgentContext, AgentData, BaseAgent, run_agent


class PyMuPDFTextLoaderAgent(BaseAgent):
    """Load PDF file using PyMuPDF."""

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        import fitz  # PyMuPDF

        pdf = fitz.open(data.value)
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
        self.write_out(ctx, "documents", AgentData("document", out_doc_dicts))
        self.write_out(ctx, "contents", AgentData("text", out_texts))


def main():
    run_agent(PyMuPDFTextLoaderAgent)


if __name__ == "__main__":
    main()
