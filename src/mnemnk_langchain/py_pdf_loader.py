from typing import override

from . import AgentContext, AgentData, BaseAgent, run_agent


class PyPDFLoaderAgent(BaseAgent):
    """Load PDF file using PyPDFLoader."""

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(data.value)
        out_texts = []
        out_doc_dicts = []
        for page in loader.lazy_load():
            doc_dict = {
                "metadata": page.metadata,
                "page_content": page.page_content,
            }
            out_texts.append(page.page_content)
            out_doc_dicts.append(doc_dict)
        self.write_out(ctx, "documents", AgentData("document", out_doc_dicts))
        self.write_out(ctx, "contents", AgentData("text", out_texts))


def main():
    run_agent(PyPDFLoaderAgent)


if __name__ == "__main__":
    main()
