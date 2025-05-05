from typing import Optional
from loguru import logger

from . import BaseAgent, run_agent


class YoutubeLoaderAgent(BaseAgent):
    """Load YouTube videos using YoutubeLoader."""

    def process_input(self, _ch: str, _kind: str, value: any, metadata: Optional[dict[str, any]]):
        from langchain_community.document_loaders import YoutubeLoader

        if value.startswith("https://www.youtube.com/"):
            loader = YoutubeLoader.from_youtube_url(value, add_video_info=False)
            documents = loader.load()
            if not documents:
                logger.error("No documents found")
                return
            document = documents[0]

            doc_dict = {
                "metadata": document.metadata,
                "page_content": document.page_content,
            }
            self.write_out("document", "document", doc_dict, metadata)
            self.write_out("content", "text", document.page_content, metadata)


def main():
    run_agent(YoutubeLoaderAgent)


if __name__ == "__main__":
    main()
