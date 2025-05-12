from typing import override

from loguru import logger

from . import AgentContext, AgentData, BaseAgent, run_agent


class YoutubeLoaderAgent(BaseAgent):
    """Load YouTube videos using YoutubeLoader."""

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        from langchain_community.document_loaders import YoutubeLoader

        if data.value.startswith("https://www.youtube.com/"):
            language = self.config.get("language", "en").split(",")
            translation = self.config.get("translation")
            if translation == "":
                translation = None

            loader = YoutubeLoader.from_youtube_url(
                data.value,
                add_video_info=False,
                language=language,
                translation=translation,
            )

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
    run_agent(YoutubeLoaderAgent)


if __name__ == "__main__":
    main()
