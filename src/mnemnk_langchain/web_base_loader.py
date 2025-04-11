from loguru import logger

from . import BaseAgent, run_agent


class WebBaseLoaderAgent(BaseAgent):
    """Load web pages using WebBaseLoader."""

    def process_input(self, _ch: str, _kind: str, value: any):
        from langchain_community.document_loaders import WebBaseLoader

        if value.startswith("http://") or value.startswith("https://"):
            loader = WebBaseLoader(web_path=value)
            documents = loader.load()
            if not documents:
                logger.error("No documents found")
                return
            document = documents[0]

            doc_dict = {
                "metadata": document.metadata,
                "page_content": document.page_content,
            }
            self.write_out("document", "document", doc_dict)
            self.write_out("content", "text", document.page_content)


def main():
    run_agent(WebBaseLoaderAgent)


if __name__ == "__main__":
    main()
