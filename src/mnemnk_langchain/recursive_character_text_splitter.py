from typing import Any, Optional, override

from langchain_text_splitters import RecursiveCharacterTextSplitter

from . import AgentContext, AgentData, BaseAgent, run_agent


class RecursiveCharacterTextSplitterAgent(BaseAgent):
    """Agent that splits text into chunks using RecursiveCharacterTextSplitter."""

    DEFAULT_CONFIG = {
        "model_name": "gpt-3.5-turbo",
        "chunk_size": 4000,
        "chunk_overlap": 20,
    }

    def __init__(self, config=None):
        """Initialize the RecursiveCharacterTextSplitterAgent with configuration."""
        super().__init__(config)
        self.process_config(self.config)

    @override
    def process_config(self, _new_config: Optional[dict[str, Any]]):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=self.config["model_name"],
            chunk_size=self.config["chunk_size"],
            chunk_overlap=self.config["chunk_overlap"],
        )

    @override
    def process_input(self, ctx: AgentContext, data: AgentData):
        texts = self.text_splitter.split_text(data.value)
        self.write_out(ctx, "texts", AgentData("text", texts))


def main():
    run_agent(RecursiveCharacterTextSplitterAgent)


if __name__ == "__main__":
    main()
