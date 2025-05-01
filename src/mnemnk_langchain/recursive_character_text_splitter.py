from typing import Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter

from . import BaseAgent, run_agent


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
    
    def process_config(self, _new_config: Optional[dict[str, any]]):
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=self.config["model_name"],
            chunk_size=self.config["chunk_size"],
            chunk_overlap=self.config["chunk_overlap"],
        )
    
    def process_input(self, _ch: str, _kind: str, value: any):
        texts = self.text_splitter.split_text(value)
        self.write_out("texts", "text", texts)
    

def main():
    run_agent(RecursiveCharacterTextSplitterAgent)


if __name__ == "__main__":
    main()
