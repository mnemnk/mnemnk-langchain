from typing import override

from loguru import logger

from . import AgentContext, AgentData, BaseAgent, run_agent


class WebBaseLoaderAgent(BaseAgent):
    """Load web pages using WebBaseLoader."""

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        from langchain_community.document_loaders import WebBaseLoader

        if data.value.startswith("http://") or data.value.startswith("https://"):
            loader = WebBaseLoader(web_path=data.value)
            documents = loader.load()
            if not documents:
                logger.error("No documents found")
                return
            document = documents[0]

            doc_dict = {
                "metadata": document.metadata,
                "page_content": document.page_content,
            }
            self.write_out(ctx, "document", AgentData("document", doc_dict))
            self.write_out(ctx, "content", AgentData("text", document.page_content))


def main():
    run_agent(WebBaseLoaderAgent)


if __name__ == "__main__":
    main()
